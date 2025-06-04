#!/usr/bin/env python
from app.db.session import SessionLocal
from app.db.init_db import init_db

def main():
    db = SessionLocal()
    init_db(db)
    db.close()
    print("Database initialization completed.")

if __name__ == "__main__":
    main() 