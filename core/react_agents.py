from typing import Dict
import re, json

class ReActAgent:
    def __init__(self, model, tools: Dict[str, any]):
        self.model = model
        self.tools = tools
        self.max_steps = 5

    def _parse_response(self, text: str) -> Dict:
        """Parse ReAct response thành từng phần"""
        text = text.replace('\n', ' ')
        thought_match = re.search(r"THINKING\s*:(.*?)(?=ACTION|OBSERVATION|FINAL|$)", text, re.IGNORECASE)
        action_match = re.search(r"ACTION\s*:(.*?)(?=THINK|OBSERVATION|FINAL|$)", text, re.IGNORECASE)
        observation_match = re.search(r"OBSERVATION\s*:(.*?)(?=THINK|ACTION|FINAL|$)", text, re.IGNORECASE)
        final_match = re.search(r"FINAL ANSWER\s*:(.*?)(?=THINK|ACTION|OBSERVATION|$)", text, re.IGNORECASE)

        action_data = {}
        if action_match:
            try:
                action_str = action_match.group(1).strip()
                json_match = re.search(r"\{.*\}", action_str)
                if json_match:
                    action_data = json.loads(json_match.group(0))
            except Exception as e:
                print("Error parsing action JSON:", e)

        return {
            "SUY NGHĨ": thought_match.group(1).strip() if thought_match else "",
            "HÀNH ĐỘNG": action_data,
            "QUAN SÁT": observation_match.group(1).strip() if observation_match else "",
            "TRẢ LỜI": final_match.group(1).strip() if final_match else ""
        }

    def run(self, prompt: str) -> str:
        """Thực hiện một vòng ReAct"""
        response = self.model.generate_reply(prompt=prompt, context=[])

        if any(keyword in response.upper() for keyword in ["THINKING:", "ACTION:", "OBSERVATION:", "FINAL ANSWER:"]):
            parsed = self._parse_response(response)

            if parsed["HÀNH ĐỘNG"]:
                tool_name = parsed["HÀNH ĐỘNG"].get("tool")
                tool_input = parsed["HÀNH ĐỘNG"].get("input")
                if tool_name in self.tools:
                    try:
                        result = self.tools[tool_name].run(tool_input)
                        parsed["QUAN SÁT"] = f"Kết quả từ tool {tool_name}: {result}"
                    except Exception as e:
                        parsed["QUAN SÁT"] = f"Lỗi khi gọi tool {tool_name}: {e}"
                else:
                    parsed["QUAN SÁT"] = f"⚠️ Công cụ {tool_name} không được hỗ trợ."

            return parsed.get("TRẢ LỜI", "Không có câu trả lời cuối.")
        else:
            return response

if __name__ == "__main__":
    from model_factory import ModelFactory
    from tool import SearchBookTool, OrderBookTool
    from database.database_manager import Database_Manager
    db = Database_Manager()
    config = {
        "Local_model": [
            {
                "model_id": "model1",
                "endpoint": "http://127.0.0.1:11434/api/generate",
                "model_name": "qwen3:1.7b",
                "max_tokens": 2048
            },
            {
                "model_id": "echo",
            }
        ]
    }
    tools = {
    "SearchBookTool": SearchBookTool(db),
    "OrderBookTool": OrderBookTool(db)
    }
    model = ModelFactory.create("model1", config)
    ReActAgent = ReActAgent(model=model, tools=tools)
    print(ReActAgent.run("Cho tôi mua 3 quyển sách Toán cao cấp."))