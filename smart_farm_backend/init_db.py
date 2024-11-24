# init_db.py
from app.database import Base, engine, SessionLocal
from app.models import *  # Import all sensor/controller classes
from app.utils import hash_password

def init_database():
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    print("Checking if admin user exists...")
    db = SessionLocal()
    existing_admin = db.query(User).filter(User.username == "admin").first()
    
    if not existing_admin:
        print("Creating admin user...")
        new_user = User(
            username="admin",
            password=hash_password("securepassword")
        )
        db.add(new_user)
        try:
            db.commit()
            print("Admin user created successfully!")
        except Exception as e:
            print(f"Error creating admin user: {e}")
            db.rollback()
    else:
        print("Admin user already exists")
    
    db.close()

if __name__ == "__main__":
    init_database()