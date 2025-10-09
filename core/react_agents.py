import json
import re
from typing import Dict

class ReActAgent:
    def __init__(self, model, tools: Dict[str, any]):
        self.model = model
        self.tools = tools
        self.max_steps = 5

    def _extract_block(self, text: str, label: str) -> str:
        """Trích riêng nội dung giữa LABEL và block tiếp theo"""
        pattern = rf"{label}\s*:(.*?)(?=THINKING\s*:|ACTION\s*:|OBSERVATION\s*:|FINAL ANSWER\s*:|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip()
        return ""

    def _safe_json_parse(self, text: str) -> Dict:
        """Cố gắng parse JSON, nếu lỗi thì trả dict rỗng"""
        try:
            json_match = re.search(r"\{.*\}", text.strip(), re.DOTALL)
            if json_match:
                return json.loads(json_match.group(0))
        except json.JSONDecodeError as e:
            print(f"[JSON decode error]: {e}")
        return {}

    def _parse_response(self, text: str) -> Dict[str, any]:
        """Tách rõ 4 phần THINKING / ACTION / OBSERVATION / FINAL ANSWER"""
        text = text.strip()

        thought = self._extract_block(text, "THINKING")
        action_text = self._extract_block(text, "ACTION")
        observation = self._extract_block(text, "OBSERVATION")
        final = self._extract_block(text, "FINAL ANSWER")

        action_data = self._safe_json_parse(action_text)

        return {
            "SUY NGHĨ": thought,
            "HÀNH ĐỘNG": action_data,
            "QUAN SÁT": observation,
            "TRẢ LỜI": final
        }

    def run(self, prompt: str) -> str:
        
        response = self.model.generate_reply(prompt,[])
        parsed = self._parse_response(response)

        action = parsed["HÀNH ĐỘNG"]
        if action:
            tool_name = action.get("tool")
            tool_input = action.get("input", {})

            if tool_name in self.tools:
                try:
                    result = self.tools[tool_name].run(tool_input)
                    if result:
                        parsed["QUAN SÁT"] = result
                        observation = json.dumps(result, ensure_ascii=False)
                        response = self.model.generate_reply(prompt + f"\nOBSERVATION: {observation}", [])
                        parsed = self._parse_response(response)
                        result2 = parsed.get("TRẢ LỜI", "Không có câu trả lời cuối")
                        return result2
                except Exception as e:
                    observation = f"Lỗi khi gọi tool {tool_name}: {e}"
            else:
                observation = f"Công cụ {tool_name} không được hỗ trợ."


        return parsed.get("TRẢ LỜI", "Không có câu trả lời cuối")

if __name__ == "__main__":
    from model_factory import ModelFactory
    from tool import SearchBookTool, OrderBookTool
    from database.database_manager import Database_Manager
    db = Database_Manager()
    tools = {
    "SearchBookTool": SearchBookTool(db),
    "OrderBookTool": OrderBookTool(db)
    }
    model = ModelFactory.create("model1")
    ReActAgent = ReActAgent(model=model, tools=tools)
    print(ReActAgent.run("Cho tôi thông tin về cuốn Toán cao cấp"))