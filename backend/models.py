# backend/models.py
from dataclasses import dataclass
from datetime import date

@dataclass
class User:
    id: int
    username: str
    password_hash: str
    role_id: int

@dataclass
class Book:
    id: int
    title: str
    author_id: int
    isbn: str
    copies_total: int
    copies_available: int

@dataclass
class Member:
    id: int
    user_id: int
    full_name: str
    membership_no: str

@dataclass
class Loan:
    id: int
    member_id: int
    book_id: int
    borrow_date: date
    due_date: date
    returned_date: date | None
