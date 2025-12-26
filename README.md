🚀 Playdate Finder – Flask Web App (MVP)

Playdate Finder is a full-stack Flask web application that helps parents discover nearby playdates and connect with other families in their area.

This project was developed as a 6-week MVP to demonstrate practical backend and frontend engineering skills, including authentication, database modeling, form validation, and location-aware features. 

🌐 Live Demo
https://flask-playdate-app.onrender.com

👉 Deployed on Render
(Free-tier deployment; geocoding gracefully degrades when external services are unavailable)

📸 Screenshots

Screenshots showcasing key user flows:

Public Home Page

Home Page (Authenticated User)

Playdate Creation Form

Update / Delete Playdates

Playdates Grouped by Author

User Account Page

Search & Browse Playdates

Static Pages (About, Contact)

(Screenshots stored in /docs/screenshots)

⭐ Key Features (MVP)
👤 User Authentication

User registration & login

Secure password hashing

Session management with Flask-Login

Personalized user accounts

📅 Playdate Management

Create playdates with:

Title

Description

City / Location

Date & Time

Edit and delete own playdates

Browse playdates created by other users

📍 Location-Aware Browsing

Search playdates by city or area

Distance calculation using Geopy

Graceful fallback when geocoding services are unavailable (important for production reliability)

Design note:
Location lookup failures never crash the app. Users receive clear feedback and can retry with a more specific location.

🖥️ Responsive UI

Mobile-friendly layout using Bootstrap 5

Conditional rendering:

Guests see limited information

Authenticated users see full details

🛡️ Form Security & Validation

Flask-WTF CSRF protection

Server-side validation for:

Dates and times

Required fields

Ownership checks for updates/deletes

🧱 Tech Stack
Backend

Python 3

Flask (application factory pattern)

SQLAlchemy ORM

Flask-Login

Flask-WTF / WTForms

Frontend

Jinja2 templates

Bootstrap 5

Minimal vanilla JavaScript

Database

SQLite (local development)

PostgreSQL (planned for production scaling)

Utilities & Tooling

Geopy (geocoding & distance calculation)

python-dotenv

Draw.io (architecture diagram)

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
├── Procfile
└── run.py

⚠️ Known Limitations (MVP)

Geocoding Availability
This application uses free OpenStreetMap (Nominatim) geocoding via Geopy.

In cloud hosting environments, free geocoding services may be rate-limited or temporarily unavailable. To ensure application stability, playdates can still be created when geocoding fails, and distance-based filtering degrades gracefully.

Future versions will integrate a production-grade geocoding API with caching and improved reliability.


🔧 Local Installation & Setup
1️⃣ Clone the repository
git clone <your-repository-url>
cd flask-playdate-app

2️⃣ Create & activate virtual environment
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Configure environment variables

Create a .env file:

SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///site.db

5️⃣ Run the app
flask run

🏗️ Architecture Diagram

Located at:

docs/Flask_Playdate_TechArch_V1.drawio.png

🚀 Future Enhancements (Post-MVP)
Architecture & Scalability

PostgreSQL migration for production

Blueprint-based modularization

REST API (v1)

Location & UX Improvements

Browser-based geolocation

Full distance-based sorting (SQL + in-memory)

Map-based playdate visualization

Communication Features

Email notifications

Messaging between parents

Quality & DevOps

Automated tests (pytest)

CI with GitHub Actions

📄 License

MIT License