from app import create_app, db
from app.models import User, Post

app = create_app()

with app.app_context():
    print("\n🔎 Database Status:")
    print(f"User table exists: {User.__table__.exists(db.engine)}")
    print(f"Post table exists: {Post.__table__.exists(db.engine)}")
    print(f"Users count: {User.query.count()}")
    print(f"Posts count: {Post.query.count()}")