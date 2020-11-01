from app import db

def create_db():
    db.create_all()
    print("Database created")
