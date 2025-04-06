from faker import Faker
from . import db
from .models import User, Post
from werkzeug.security import generate_password_hash

def init_test_data():
    print("\n🔍 Initializing database...")
    
    # Create tables if they don't exist
    db.create_all()
    print("✅ Tables verified/created")
    
    if not User.query.first():
        fake = Faker()
        print("⚙️ Creating test users...")
        
        # Create 3 test users
        users = []
        for i in range(3):
            user = User(
                username=f"user_{i+1}",
                email=f"user{i+1}@example.com",
                created_at=db.func.now()
            )
            user.set_password("password123")
            users.append(user)
            db.session.add(user)
        
        db.session.commit()
        print(f"✅ Created {len(users)} test users")
        
        # Create test posts
        print("⚙️ Creating test posts...")
        posts = [
            Post(content="First test post!", user_id=users[0].id),
            Post(content="Hello world!", user_id=users[1].id),
            Post(content="Another test post", user_id=users[2].id)
        ]
        db.session.add_all(posts)
        db.session.commit()
        print(f"✅ Created {len(posts)} test posts")
    else:
        print("✅ Database already contains data")