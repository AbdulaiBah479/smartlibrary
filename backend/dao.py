# backend/dao.py
from backend.db import get_connection
from datetime import date, timedelta
import bcrypt

# -------------------------
# Password helpers
# -------------------------
def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def check_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# -------------------------
# User functions
# -------------------------
def create_user(username: str, password: str, role_id: int = 2):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                hashed = hash_password(password)
                cur.execute(
                    "INSERT INTO users (username, password_hash, role_id) VALUES (%s,%s,%s) RETURNING id",
                    (username, hashed, role_id)
                )
                return cur.fetchone()[0]
    finally:
        conn.close()

def get_user_by_username(username: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, username, password_hash, role_id FROM users WHERE username=%s", (username,))
            return cur.fetchone()
    finally:
        conn.close()

# -------------------------
# Author & Book functions
# -------------------------
def add_author(name):
    conn = get_connection()
    cur = conn.cursor()
    sql = "INSERT INTO authors (name) VALUES (%s) RETURNING id;"
    cur.execute(sql, (name,))
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result[0]



def add_book(title, author_id, isbn, copies):
    conn = get_connection()
    cur = conn.cursor()
    sql = """
        INSERT INTO books (title, author_id, isbn, copies_total, copies_available)
        VALUES (%s, %s, %s, %s, %s) RETURNING id;
    """
    cur.execute(sql, (title, author_id, isbn, copies, copies))
    result = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return result[0]



def search_books(query: str):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            q = f"%{query}%"
            cur.execute("""
                SELECT b.id, b.title, a.name as author, b.copies_available
                FROM books b LEFT JOIN authors a ON a.id=b.author_id
                WHERE b.title ILIKE %s OR a.name ILIKE %s
                LIMIT 200
            """, (q, q))
            return cur.fetchall()
    finally:
        conn.close()

# -------------------------
# Member functions
# -------------------------
def create_member(user_id: int, full_name: str, membership_no: str):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("INSERT INTO members (user_id, full_name, membership_no) VALUES (%s,%s,%s) RETURNING id",
                            (user_id, full_name, membership_no))
                return cur.fetchone()[0]
    finally:
        conn.close()

def get_member_by_user_id(user_id: int):
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM members WHERE user_id=%s", (user_id,))
            return cur.fetchone()
    finally:
        conn.close()

# -------------------------
# Loan functions
# -------------------------
def count_active_loans(member_id: int) -> int:
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM loans WHERE member_id=%s AND returned_date IS NULL", (member_id,))
            return cur.fetchone()[0]
    finally:
        conn.close()

def borrow_book(member_id: int, book_id: int):
    if count_active_loans(member_id) >= 3:
        raise Exception("Member already has 3 active loans.")

    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT copies_available FROM books WHERE id=%s FOR UPDATE", (book_id,))
                r = cur.fetchone()
                if not r:
                    raise Exception("Book not found.")
                if r[0] <= 0:
                    raise Exception("No copies available.")
                cur.execute("UPDATE books SET copies_available = copies_available - 1 WHERE id=%s", (book_id,))
                due = date.today() + timedelta(days=7)
                cur.execute("INSERT INTO loans (member_id, book_id, borrow_date, due_date) VALUES (%s,%s,%s,%s) RETURNING id",
                            (member_id, book_id, date.today(), due))
                return cur.fetchone()[0]
    finally:
        conn.close()

def return_book(loan_id: int):
    conn = get_connection()
    try:
        with conn:
            with conn.cursor() as cur:
                cur.execute("SELECT book_id FROM loans WHERE id=%s AND returned_date IS NULL", (loan_id,))
                row = cur.fetchone()
                if not row:
                    raise Exception("Loan not found or already returned.")
                book_id = row[0]
                cur.execute("UPDATE loans SET returned_date=%s WHERE id=%s", (date.today(), loan_id))
                cur.execute("UPDATE books SET copies_available = copies_available + 1 WHERE id=%s", (book_id,))
                return True
    finally:
        conn.close()
