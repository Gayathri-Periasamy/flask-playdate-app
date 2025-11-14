# Playdate Finder – Flask Web App (MVP)

A web application that helps parents arrange **kids’ playdates** with nearby families.  
Built using **Python Flask**, **SQLAlchemy**, **Bootstrap/Tailwind**, and a simple relational database.

This project is part of a 3-week MVP build and will be expanded with new features, enhancements, and improvements in future versions.

---

## Features (MVP)

✔ User registration & login  
✔ Manage children’s profiles  
✔ Create and view playdates  
✔ Set city/area or use browser geolocation (optional MVP)  
✔ Browse nearby playdates based on proximity  
✔ Simple, intuitive UI built with Bootstrap/Tailwind  
✔ Secure forms using Flask-WTF  

---

## Tech Stack

    **Backend:**  
    - Python 3  
    - Flask (Blueprint-ready structure)  
    - SQLAlchemy  
    - Flask-WTF (forms & CSRF protection)  
    - Flask-Login (authentication)

    **Frontend:**  
    - Jinja2 templates  
    - Bootstrap or TailwindCSS  
    - Optional: JavaScript for geolocation

    **Database:**  
    - SQLite (development)  
    - PostgreSQL (future deployment)

    **Tools:**  
    - Python-dotenv  
    - Geopy (optional for distance calculation)  
    - Draw.io (architecture diagrams)

## Project Structure

FLASK_PLAYDATE_APP/
│
├── flaskplaydate/
│ ├── init.py
│ ├── models.py
│ ├── routes.py
│ ├── forms.py
│ ├── templates/
│ └── static/
│
├── instance/ (auto-created for local DB)
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
└── run.py

---

## Installation & Setup

### 1. Clone the repository
```bash
git clone <your-repository-url>
cd playdate_app

2️⃣ Create a virtual environment

python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Environment variables
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///site.db

5️⃣ Run the application
flask run


Architecture
docs/Flask_Playdate_TechArch_V1.drawio

## Future Enhancements (Post-MVP)

🔹 Full geolocation matching via browser API
🔹 Email notifications (Flask-Mail)
🔹 Profile pictures upload
🔹 Google Maps integration
🔹 Refactor using Flask Blueprints
🔹 Deploy to Render/Railway
🔹 Add pytest test suite & CI pipeline
🔹 API endpoints (v1 REST API)

## License

This project is licensed under the MIT License.

