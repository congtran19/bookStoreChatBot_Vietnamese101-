import json
from pathlib import Path
from datetime import datetime

class ChatEngine:
    def __init__(self, agent):
        self.agent = agent  
        self.history_dir_path = Path(__file__).resolve().parents[1] / "data/chat_history"
        self.history = []  # Lưu trong RAM
        self.session_file = self.history_dir_path / f"chat_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    def send_message(self, user_input: str):
        """Nhận tin nhắn từ user và phản hồi qua agent"""
        self.history.append({"role": "user", "content": user_input})

        response = self.agent.run(str(self.history[-5:]))

        self.history.append({"role": "assistant", "content": response})
        self._save_history()
        return response

    def _save_history(self):
        """Ghi lịch sử hội thoại ra file JSON"""
        with open(self.session_file, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def load_history(self, file_path: str):
        """Nạp lại hội thoại từ file cũ"""
        path = Path(file_path)
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                self.history = json.load(f)
            self.session_file = path
            print(f"🔄 Đã nạp lại lịch sử từ {path.name}")
        else:
            print("⚠️ Không tìm thấy file lịch sử!")

    def show_history(self):
        """Hiển thị hội thoại trong session hiện tại"""
        print("\n=== LỊCH SỬ HỘI THOẠI ===")
        for h in self.history:
            role = "🧍 Người dùng" if h["role"] == "user" else "🤖 Trợ lý"
            print(f"{role}: {h['content']}")
        print("==========================\n")


if __name__ == "__main__":
    from model_factory import ModelFactory
    from tool import SearchBookTool, OrderBookTool
    
    model = ModelFactory.create("model1", {
        "Local_model": [
            {
                "model_id": "model1",
                "endpoint": "http://127.0.0.1:11434/api/generate",
                "model_name": "qwen3:1.7b",
                "max_tokens": 2048
            }
        ]
    })
    from react_agents import ReActAgent
    agents = ReActAgent(model=model, tools={
        "SearchBookTool": SearchBookTool(None),
        "OrderBookTool": OrderBookTool(None)
    })
    ChatEngine = ChatEngine(agents)
    while True:
        user_input = input("Bạn: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = ChatEngine.send_message(user_input)
        print("Trợ lý:", response)