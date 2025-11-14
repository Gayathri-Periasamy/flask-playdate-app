import os
import secrets
#from PIL import Image
from flask import Blueprint,current_app, render_template, url_for,flash,redirect,request,abort
from flaskplaydate.models import User
from flaskplaydate import db, bcrypt
from flaskplaydate.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flask_login import login_user,current_user, logout_user,login_required

# Define a Blueprint instead of using app directly
main = Blueprint('main', __name__)

@main.route('/', endpoint='home')
#@main.route('/home')
def home():
    #posts = Post.query.all()
    return render_template('home.html')

@main.route('/about', endpoint='about')
def about():
    return render_template('about.html',title="About")


@main.route('/register',endpoint = 'register', methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
         return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email= form.email.data,password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You are now able to log in','success')
        return redirect(url_for('main.login'))
    return render_template('register.html', title='Register', form=form)   
 

@main.route('/login', endpoint = 'login', methods=['GET','POST'])
def login():
    print("DB URI:", current_app.config["SQLALCHEMY_DATABASE_URI"])
    if current_user.is_authenticated:
         return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user and bcrypt.check_password_hash(user.password, form.password.data):
                 login_user(user,remember=form.remember.data)
                 next_page = request.args.get('next')
                 return redirect(next_page) if next_page else redirect(url_for('main.home'))
            else:
                flash("Login unsuccessful. Please check your email and password","danger")
    return render_template('login.html', title='Login', form=form) 


@main.route('/logout',endpoint = 'logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))

'''
def save_picture(form_picture):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(app.root_path, 'static/pictures', picture_fn)

        output_size = (125, 125)
        target_image = Image.open(form_picture)
        target_image.thumbnail(output_size)
        target_image.save(picture_path)
        
        return picture_fn

'''

@main.route('/account', endpoint = 'account', methods=['GET','POST'])
@login_required
def account():
    form= UpdateAccountForm()
    if form.validate_on_submit():
        #current_user.image_file = save_picture(form.picture.data)
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!','success')
        return redirect(url_for('main.account'))
    elif request.method == 'GET':
        form.picture.data = current_user.image_file
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='pictures/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file,form=form) 
