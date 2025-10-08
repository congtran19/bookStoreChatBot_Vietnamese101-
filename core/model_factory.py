from pathlib import Path
from abc import ABC, abstractmethod
from typing import List
import json
import requests
import os

class ModelInterface(ABC):
    @abstractmethod
    def generate_reply(self, prompt: str, context: List[str]) -> str:
        pass

class LocalHTTPModel(ModelInterface):
    def __init__(self, cfg):
        self.endpoint = cfg.get("endpoint")
        self.headers = cfg.get("headers", {})
        self.max_tokens = cfg.get("max_tokens", 2048)
        self.model_name = cfg.get("model_name", "local-model")

    def generate_reply(self, prompt: str, context: List[str]) -> str:
        if not self.endpoint:
            return f"LocalModel-Echo: {prompt}"
        
        # Luôn xác định đường dẫn tuyệt đối tới prompt_react.txt
        prompt_path = Path(__file__).resolve().parent / "prompt_react.txt"
        with open(prompt_path, "r", encoding="utf-8") as f:
            react_prompt = f.read().strip()

        # Ghép prompt ReAct
        full_prompt = react_prompt + "\n\n"
        if context:
            full_prompt += "\n---\n".join(context) + "\n---\n"
        full_prompt += prompt

        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False
        }

        try:
            r = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=50)
            r.raise_for_status()
            j = r.json()

            if "response" in j:
                return j["response"].strip()
            if "text" in j:
                return j["text"].strip()
            if "reply" in j:
                return j["reply"].strip()
            if "choices" in j and j["choices"]:
                return str(j["choices"][0].get("text") or j["choices"][0].get("message", {}).get("content", "")).strip()

            return str(j)
        except Exception as e:
            return f"[Local model call failed: {e}]"



class SimpleEchoModel(ModelInterface):
    def __init__(self, cfg=None):
        pass
    def generate_reply(self, prompt: str, context: List[str]) -> str:
        return f"Echo: {prompt}"

class ModelFactory:
    @staticmethod
    def create(model_id: str, config_path = Path(__file__).resolve().parents[1] /"config.json"):
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
        # Look up model in config using model_id from either API_model or Local_model
        local_models = {m.get("model_id"): m for m in config.get("Local_model", [])}

        if model_id in local_models:
            cfg = local_models.get(model_id)
            # if local config contains endpoint -> LocalHTTPModel else echo
            if cfg.get("endpoint"):
                return LocalHTTPModel(cfg)
            else:
                return SimpleEchoModel(cfg)
        # default
        return SimpleEchoModel({})

if __name__ == "__main__":
    model = ModelFactory.create("model1")
    while True:
        user_input = input("Bạn: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = model.generate_reply(user_input, [])
        print("Trợ lý:", response)

    

