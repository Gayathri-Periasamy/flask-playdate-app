from flaskplaydate import db, login_manager
from datetime import datetime
from flask_login import UserMixin

# Define how Flask-Login loads a user from an ID stored in session
@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20),nullable=False, default='default.jpg')
    playdates = db.relationship('Playdate',backref = 'author',lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Child(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(20), nullable=False,default='Anonymous')
    age = db.Column(db.Integer,nullable=False)
    interests = db.Column(db.String(200), nullable=False,default='Not Mentioned')

    def __repr__(self):
        return f"Child('{self.name}','{self.age}','{self.interests}')"


class Playdate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(100), nullable=False)
    latitude= db.Column(db.Float, nullable=False)
    longitude= db.Column(db.Float, nullable=False)
    playdate_date_time = db.Column(db.DateTime, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)   

    def __repr__(self):
        return f"Playdate('{self.title}',{self.city}'{self.playdate_date_time}')"
    


