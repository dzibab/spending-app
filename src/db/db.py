# db.py
from databases import Database

DATABASE_URL = "sqlite+aiosqlite:///./test.db"  # Path to your SQLite database file

database = Database(DATABASE_URL)
