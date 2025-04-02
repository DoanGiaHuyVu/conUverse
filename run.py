from app import create_app
from app.models import init_db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        init_db()  # Initialize database tables
    app.run(debug=True)