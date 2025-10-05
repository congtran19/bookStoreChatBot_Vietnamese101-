
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
        
        with open("core/prompt_react.txt", "r", encoding="utf-8") as f:
            react_prompt = f.read().strip()
        # Ghép react prompt vào đầu prompt
        full_prompt = react_prompt + "\n" + prompt
        if context:
            full_prompt = "\n".join(str(c) for c in context) + "\n"

        payload = {
            "model": self.model_name,
            "prompt": full_prompt,
            "stream": False
        }
        try:
            r = requests.post(self.endpoint, json=payload, headers=self.headers, timeout=30)
            r.raise_for_status()
            j = json.loads(r.text)

            # Ollama trả về {"model": "...", "created_at": "...", "response": "...", ...}
            if isinstance(j, dict) and "response" in j:
                return str(j["response"]).strip()

            # Các dạng khác
            if "reply" in j:
                return str(j["reply"])
            if "text" in j:
                return str(j["text"])
            if "choices" in j and isinstance(j["choices"], list) and j["choices"]:
                return str(j["choices"][0].get("text") or j["choices"][0].get("message", {}).get("content", ""))

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
    def create(model_id: str, config: dict):
        # Look up model in config using model_id from either API_model or Local_model
        local_models = {m.get("model_id"): m for m in config.get("Local_model", [])}

        if model_id in local_models:
            cfg = local_models[model_id]
            # if local config contains endpoint -> LocalHTTPModel else echo
            if cfg.get("endpoint"):
                return LocalHTTPModel(cfg)
            else:
                return SimpleEchoModel(cfg)
        # default
        return SimpleEchoModel({})

if __name__ == "__main__":
    # Test LocalHTTPModel
    config = {
        "Local_model": [
            {
                "model_id": "model1",
                "endpoint": "http://127.0.0.1:11434/api/generate",
                "model_name": "qwen3:1.7b",
                "max_tokens": 4096
            },
            {
                "model_id": "echo",
            }
        ]
    }
    model = ModelFactory.create("model1", config)
    print(model.generate_reply("Tôi muốn mua 2 quyển Học sâu cho người mới.", []))
    

