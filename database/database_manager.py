import json
from pathlib import Path
from threading import Lock
from database.models import Book, Order

class Database_Manager:
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(__file__).resolve().parents[1] / data_dir
        self.books_file = self.data_dir / "books.json"
        self.orders_file = self.data_dir / "orders.json"
        self.data_dir.mkdir(parents=True, exist_ok=True)

        self._lock = Lock()

    def load_books(self) -> list[Book]:
        with self._lock:
            with open(self.books_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Book(**b) for b in data]

    def save_books(self, books: list[Book]):
        with self._lock:
            data = [b.to_dict() for b in books]
            with open(self.books_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)

    def update_book_stock(self, book_id: int, delta: int):
        with self._lock:
            books = self.load_books()
            for book in books:
                if book.book_id == book_id:
                    if book.stock + delta < 0:
                        raise ValueError("Sô lượng update không hợp lệ")
                    book.stock += delta
                    break
            else:
                raise ValueError("Không thấy sách ")
            self.save_books(books)

    def load_orders(self) -> list[Order]:
        with self._lock:
            with open(self.orders_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return [Order(**o) for o in data]

    def add_order(self, order: Order) -> int:
        with self._lock:
            orders = self.load_orders()
            order.order_id = max([o.order_id for o in orders] + [0]) + 1
            orders.append(order)
            data = [o.to_dict() for o in orders]
            with open(self.orders_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return order.order_id
        

if __name__ == "__main__":
    db = Database_Manager()
    books = db.load_books()
    for b in books:
        print(b)
    orders = db.load_orders()
    for o in orders:
        print(o)