import os
from app import create_app, db
from app.models import seed_data # Also ensure seed_data is imported

db_path = 'instance/app.db'
if os.path.exists(db_path):
    os.remove(db_path) # Deleting the database
    print("Existing database deleted.")

app = create_app()
with app.app_context(): # Crucial application context
    db.create_all() # Reset the database
    seed_data() # Seed through the database
    print("Database reset and seeded.")