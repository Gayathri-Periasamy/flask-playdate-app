from flaskplaydate import create_global_app, db
import os
app = create_global_app()

# Ensure persistent DB tables exist when running via 'flask run' (module import path)
# This will only create tables if the DB file is missing (avoids always touching DB)
with app.app_context():
    db_path = os.path.join(app.instance_path, "playdate.db")
    if not os.path.exists(db_path):
        print("Creating persistent DB at", db_path)
        db.create_all()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()   # create persistent DB when running the app normally
    app.run(debug=True)


