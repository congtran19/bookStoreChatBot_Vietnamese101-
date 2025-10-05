from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Book:
    book_id: int
    title: str
    author: str
    price: int
    stock: int
    category: str

    def to_dict(self):
        return asdict(self)

@dataclass
class Order:
    order_id: int = 0
    customer_name: str = ""
    phone: str = ""
    address: str = ""
    books: list = None  # list of {"book_id": int, "quantity": int}
    status: str = "pending"
    created_at: str = ""

    def __post_init__(self):
        if self.books is None:
            self.books = []
        if not self.created_at:
            self.created_at = datetime.utcnow().isoformat()

    def to_dict(self):
        return asdict(self)