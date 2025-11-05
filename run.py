from app import create_app, db # <--- Make sure db is imported here

app = create_app()

with app.app_context():
    db.create_all() # <--- This must be inside the app context

if __name__ == '__main__':
    app.run(debug=True)