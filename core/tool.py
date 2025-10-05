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
# 1️⃣ Interface chung cho Tool
# ===============================
class Tool(ABC):
    @abstractmethod
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Mọi tool đều phải có phương thức run"""
        pass

data_path = Path
# ===============================
# 2️⃣ Tool Tìm kiếm sách
# ===============================

class SearchBookTool:
    def __init__(self, db):
        self.db = db  # Nhận thể hiện Database

    def run(self, query: dict):
        title = query.get("title", "").lower()
        books = self.db.load_books()
        results = [b.to_dict() for b in books if title in b.title.lower()]

        if not results:
            return {"result": "❌ Không tìm thấy sách nào phù hợp."}
        return results


class OrderBookTool:
    def __init__(self, db):
        self.db = db

    def run(self, query: dict):
        title = query.get("title", "").lower()
        quantity = int(query.get("quantity", 1))
        customer = query.get("name", "Khách")
        address = query.get("address", "")
        phone = query.get("phone", "")

        books = self.db.load_books()
        found = None
        for b in books:
            if title in b.title.lower():
                found = b
                break

        if not found:
            return {"error": "❌ Không tìm thấy sách cần đặt."}
        if found.stock < quantity:
            return {"error": f"❌ Sách '{found.title}' chỉ còn {found.stock} quyển trong kho."}

        # Giảm tồn kho
        found.stock -= quantity
        self.db.save_books(books)

        # Tạo đơn hàng
        order = Order(
            customer_name=customer,
            phone=phone,
            address=address,
            books=[{"book_id": found.book_id, "quantity": quantity}],
            status="pending",
            created_at=datetime.utcnow().isoformat()
        )

        order_id = self.db.add_order(order)
        return {
            "order_id": order_id,
            "book_title": found.title,
            "quantity": quantity,
            "price_total": quantity * found.price,
            "message": f"✅ Đã tạo đơn hàng #{order_id} cho {quantity} quyển '{found.title}'"
        }


if __name__ == "__main__":
    
    from database.database_manager import Database_Manager
    db = Database_Manager()
    search_tool = SearchBookTool(db)
    order_tool = OrderBookTool(db)

    # Test SearchBookTool
    print(search_tool.run({"title": "Toán cao cấp"}))