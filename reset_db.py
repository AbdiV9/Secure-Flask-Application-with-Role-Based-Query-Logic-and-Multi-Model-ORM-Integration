import os
from app import create_app, db
from app.models import seed_data # Also ensure seed_data is imported

db_path = 'instance/app.db'
if os.path.exists(db_path):
    os.remove(db_path)
    print("Existing database deleted.")

app = create_app()
with app.app_context(): # <--- Crucial application context
    db.create_all()
    seed_data()
    print("Database reset and seeded.")