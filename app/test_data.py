from faker import Faker
from . import db
from .models import User, Post
from werkzeug.security import generate_password_hash

def init_test_data():
    print("\n🔍 Initializing database...")

    db.create_all()
    print("✅ Tables verified/created")

    if not User.query.first():
        fake = Faker()
        print("⚙️ Creating test users...")

        users = []
        user_data = [
            {"username": "alice", "email": "alice@example.com", "name": "Alice Wonder", "is_logged_in": True},
            {"username": "bob", "email": "bob@example.com", "name": "Bob Builder", "is_logged_in": False},
            {"username": "charlie", "email": "charlie@example.com", "name": "Charlie Coder", "is_logged_in": False},
            {"username": "joseph", "email": "sm_jos@live.concordia.ca", "name": "Joseph Smith", "is_logged_in": True}
        ]

        for data in user_data:
            user = User(
                username=data["username"],
                email=data["email"],
                name=data["name"],
                is_logged_in=data["is_logged_in"],
                created_at=db.func.now()
            )
            user.set_password("password123")
            db.session.add(user)
            users.append(user)

        db.session.commit()
        print(f"✅ Created {len(users)} test users")

        print("⚙️ Creating test posts...")

        posts = [
            Post(
                title="My First Post!",
                description="Just joined this platform, excited to be here!",
                content="Hey everyone! I’m Alice and I can’t wait to share some cool ideas with you all 🎉",
                tags="introduction,hello,firstpost",
                user_id=users[0].id
            ),
            Post(
                title="Project Update 🚧",
                description="Progress on the garden shed is going strong!",
                content="Laid the foundation today and picked out the paint colors. Pics coming soon!",
                tags="DIY,projects,gardening",
                user_id=users[1].id
            ),
            Post(
                title="Python Tips for Beginners 🐍",
                description="Sharing what helped me get started with Python.",
                content="Use list comprehensions, understand dictionaries early, and don’t fear errors—they’re your best teachers!",
                tags="coding,python,learning",
                user_id=users[2].id
            ),
        ]

        db.session.add_all(posts)
        db.session.commit()
        print(f"✅ Created {len(posts)} test posts")
    else:
        print("✅ Database already contains data")
