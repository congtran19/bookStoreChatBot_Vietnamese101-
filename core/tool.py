from abc import ABC, abstractmethod
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
from typing import Dict, Any, List
import json
import random

from datetime import datetime
from database.models import Order

# ===============================
# Interface chung cho Tool
# ===============================
class Tool(ABC):
    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mọi tool đều phải có phương thức run"""
        pass

data_path = Path
# ===============================
# Tool Tìm kiếm sách
# ===============================

class SearchBookTool:
    def __init__(self, db):
        self.db = db  # Nhận thể hiện Database

    def run(self, query: dict):
        title = query.get("title", "").lower()
        books = self.db.load_books()
        results = [b.to_dict() for b in books if title in b.title.lower()]
        if not results:
            return {"result": "Không tìm thấy sách nào phù hợp."}
        return results


from datetime import datetime
from database.models import Order

class OrderBookTool:
    """
    Tool: Đặt hàng sách
    input: {
        "customer_name": str,
        "phone": str,
        "address": str,
        "books": [{"book_id": int, "quantity": int}]
    }
    """
    def __init__(self, db):
        self.db = db
        self.name = "OrderBookTool"
        self.description = (
            "Tạo đơn hàng mới với thông tin khách hàng và danh sách sách muốn mua."
        )

    def run(self, query: dict):
        try:
            # Kiểm tra input hợp lệ
            if not isinstance(query, dict):
                return {"error": "Input phải là dictionary"}

            customer_name = query.get("customer_name", "").strip()
            phone = query.get("phone", "").strip()
            address = query.get("address", "").strip()
            books = query.get("books", [])

            if not customer_name or not phone or not address:
                return {"error": "Thiếu thông tin khách hàng"}
            if not isinstance(books, list) or not books:
                return {"error": "Danh sách sách không hợp lệ"}

            # Chuyển từ dict → Order object
            order = Order(
                customer_name=customer_name,
                phone=phone,
                address=address,
                books=books,
                status="pending",
                created_at=datetime.utcnow().isoformat()
            )

            # Ghi đơn hàng vào file
            order_id = self.db.add_order(order)

            return {
                "success": True,
                "message": f" Đơn hàng #{order_id} đã được tạo thành công.",
                "order_id": order_id,
                "customer": customer_name,
                "books": books
            }

        except Exception as e:
            return {"error": f"Lỗi khi tạo đơn hàng: {e}"}

if __name__ == "__main__":
    from database.database_manager import Database_Manager
    db = Database_Manager()
    tool = OrderBookTool(db)
    
    result = tool.run({
        "customer_name": "Nguyễn Văn A",
        "phone": "0123456789",
        "address": "123 Đường ABC",
        "books": [{"book_id": 1, "quantity": 2}]
    })
    
    print(result)

