🚀 Playdate Finder – Flask Web App (MVP)

A simple, intuitive web application that helps parents discover nearby playdates and connect with other families in their area.

This is a 3-week MVP project, built to demonstrate full-stack development skills with Python/Flask, SQLAlchemy, Bootstrap, and location-based filtering. The application will be extended in future versions with new features and improved UX.

📸 Screenshots
    Home Page
    Playdate Create Form
    User Account Page
    About Page
    Contact Page
    Search Playdates



⭐ Features (MVP)
👤 User Authentication

    User registration and login

    Secure password hashing

    Personalized account management

📅 Playdate Management

1. Create playdates with:

    Title

    Description

    City/Location

    Date & Time

2. Edit or delete own playdates

3. View playdates created by any user

📍 Location-Based Browsing

    Search playdates by city/area

    Optional radius-based filtering

    Distance calculation using Geopy (MVP simplified: minimal matching)

🖥️ Responsive UI

    Clean, mobile-friendly interface

    Bootstrap components

    Conditional UI (blurred info for guests, full details for logged-in users)

🛡️ Form Security

    Flask-WTF CSRF protection

    Server-side validation (including date/time validation)

🧱 Tech Stack
Backend

    Python 3

    Flask (app factory pattern)

    SQLAlchemy ORM

    Flask-Login

    Flask-WTF / WTForms

Frontend

    Jinja2 templating

    Bootstrap 5

    Optional vanilla JavaScript

Database

    SQLite (dev)

    PostgreSQL (planned for deployment)

Utilities

    Geopy – optional geocoding & distance calculation

    python-dotenv

Draw.io – architecture diagram

📁 Project Structure
FLASK_PLAYDATE_APP/
│
├── flaskplaydate/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   ├── forms.py
│   ├── templates/
│   └── static/
│
├── instance/               # Auto-created for local SQLite DB
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
|---Procfile
└── run.py

🔧 Installation & Setup
1️⃣ Clone the repository
git clone <your-repository-url>
cd flask-playdate-app

2️⃣ Create a virtual environment
python3 -m venv venv
source venv/bin/activate       # macOS/Linux
venv\Scripts\activate          # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure environment variables

Create a .env file:

SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///site.db

5️⃣ Run the application
flask run

🏗️ Architecture Diagram

Located in:

docs/Flask_Playdate_TechArch_V1.drawio.png

🚀 Future Enhancements (Post-MVP)
🔹 Location & UI Improvements

    Browser geolocation integration

    Full distance-based sorting (SQL & in-memory hybrid)

    Google Maps embed for playdate locations

🔹 Communication

    Email notifications using Flask-Mail

    Messaging system between parents

🔹 Scalability & Deployment

    Deployment to Render / Railway

    Swap to PostgreSQL in production

🔹 Codebase Improvements

    Add Flask Blueprint modularization

    Add automated tests (pytest)

    GitHub Actions CI

    API endpoints (REST v1)

📄 License

This project is licensed under the MIT License.