import os
import secrets
from PIL import Image
from geopy.geocoders import Nominatim
from flask import Blueprint,current_app, render_template, url_for,flash,redirect,request,abort
from flaskplaydate.models import User, Playdate
from flaskplaydate import db, bcrypt
from flaskplaydate.forms import RegistrationForm, LoginForm, UpdateAccountForm, PlaydateForm
from flask_login import login_user,current_user, logout_user,login_required
from datetime import datetime
from geopy.distance import geodesic

# Define a Blueprint instead of using app directly
main = Blueprint('main', __name__)

@main.route('/', endpoint='home')
def home():
    page_number = request.args.get('page', 1, type=int)  #default to 1 if no page query parameter, page num restrictd to int, values other than int throw value error
    playdates = Playdate.query.order_by(Playdate.date_posted.desc()).paginate(page=page_number, per_page=5)
    return render_template('home.html',playdatesinfo=playdates,searchtext="")

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


def save_picture(form_picture):
        random_hex = secrets.token_hex(8)
        _, f_ext = os.path.splitext(form_picture.filename)
        picture_fn = random_hex + f_ext
        picture_path = os.path.join(current_app.root_path, 'static/pictures', picture_fn)

        output_size = (125, 125)
        target_image = Image.open(form_picture)
        target_image.thumbnail(output_size)
        target_image.save(picture_path)
        
        return picture_fn


@main.route('/account', endpoint = 'account', methods=['GET','POST'])
@login_required
def account():
    form= UpdateAccountForm()
    if form.validate_on_submit():
        current_user.image_file = save_picture(form.picture.data)
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


geolocator = Nominatim(user_agent="flask-playdate-app")
def validate_geocode_location(location_string):
    result = geolocator.geocode(location_string, country_codes='de', addressdetails=True)
    if result is None:
        raise ValueError('Location not found. Please enter a more precise city/area name.')
    '''if (result.latitude== 0 or result.longitude == 0):
        raise ValueError('Invalid location coordinates. Please refine your input.')
    #importance = result.raw.get('importance', 0)
    #if importance < 0.5:
    #    raise ValueError('Location is too vague. Please enter a more specific city/area name.')
    
    address = result.raw['address']
    
    allowed_types=['city','town','village','suburb','neighbourhood','hamlet','house','residential']
    place_type = result.raw.get('type', '')
    if place_type not in allowed_types:
        raise ValueError(f'This does not look like a real place, ({place_type}) Try a city or neighborhood.')
    '''
    return result.latitude, result.longitude
    
     
@main.route("/new/playdate",methods=['GET','POST'])
@login_required
def create_playdate():
    form= PlaydateForm()
    if form.validate_on_submit():
        try:
        
            lat,lon=validate_geocode_location(form.city.data)

            playdate=Playdate(
                title = form.title.data,
                description=form.description.data,
                city=form.city.data, 
                latitude=lat,
                longitude=lon,
                playdate_date_time=datetime.combine(form.date.data, form.time.data),
                author=current_user
            )
            
            db.session.add(playdate)
            db.session.commit()
            flash('Your playdate has been created!','success')
            return redirect(url_for('main.home'))
        
        except ValueError as e:
            flash(str(e), 'danger')
        
    return render_template('create_playdate.html', title='New Playdate', form=form,legend='New Playdate') 


@main.route("/playdate/<int:playdate_id>")
def playdate(playdate_id):
     playdate=Playdate.query.get_or_404(playdate_id)
     return render_template('playdate.html', title='playdate.title',playdate=playdate) 


@main.route("/playdate/<int:playdate_id>/update",methods=['GET','POST'])
def update_playdate(playdate_id):
    playdate=Playdate.query.get_or_404(playdate_id)
    if playdate.author != current_user:
        abort(403)
    form= PlaydateForm()
    if form.validate_on_submit():
         
        playdate.title=form.title.data
        playdate.description=form.description.data

        if playdate.city != form.city.data :
            lat,lon=validate_geocode_location(form.city.data)
            playdate.latitude=lat
            playdate.longitude=lon
            playdate.city=form.city.data         
        playdate.playdate_date_time=datetime.combine(form.date.data, form.time.data)
        db.session.commit()
        flash('Your playdate has been updated!','success')
        return redirect(url_for('main.playdate',playdate_id=playdate.id))
    elif request.method == 'GET':
         
         form.title.data = playdate.title
         form.description.data = playdate.description
         form.city.data = playdate.city
         temp_date= datetime.date(playdate.playdate_date_time)
         temp_time = datetime.time(playdate.playdate_date_time)
         form.date.data = temp_date
         form.time.data = temp_time
         
    return render_template('create_playdate.html', title='Update playdate', form=form,legend='Update playdate') 

@main.route("/playdate/<int:playdate_id>/delete",methods=['GET','POST'])
def delete_playdate(playdate_id):
    playdate=Playdate.query.get_or_404(playdate_id)
    if playdate.author != current_user:
        abort(403)
    db.session.delete(playdate)
    db.session.commit()
    flash('Your playdate has been deleted!','success')
    return redirect(url_for('main.home'))

@main.route("/user/<string:username>")
def user_playdates(username):
    page_number = request.args.get('page', 1, type=int)  #default to 1 if no page query parameter, page num restrictd to int, values other than int throw value error
    user = User.query.filter_by(username=username).first_or_404()
    playdates = Playdate.query.filter_by(author=user)\
        .order_by(Playdate.date_posted.desc())\
        .paginate(page=page_number, per_page=5)
    return render_template('user_playdates.html',playdatesinfo = playdates,user=user)

@main.route("/search",methods=['GET'])
def search_playdates():
    page_number = request.args.get('page', 1, type=int)  #default to 1 if no page query parameter, page num restrictd to int, values other than int throw value error
    searchtext=request.args.get('search')
    like=f"%{searchtext}%"

    search_lat,search_lon=validate_geocode_location(searchtext)
    if search_lat:
        lat1=search_lat
    if search_lon:
        lon1=search_lon
    result_id=[]
    all_playdates = Playdate.query.all()
    for playdate in all_playdates:
        lat2=playdate.latitude
        lon2=playdate.longitude
        distance = distance_calculator(lat1,lon1,lat2,lon2)
        print (distance)
        if distance < 3:
            result_id.append(playdate.id)
        print(len(result_id))
    filtered_playdates=Playdate.query.filter(Playdate.id.in_(result_id)).paginate(page=page_number, per_page=5)
    #filtered_playdates=Playdate.query.filter(Playdate.city.ilike(like)).paginate(page=page_number, per_page=5)
    return render_template('home.html',playdatesinfo = filtered_playdates, searchtext=searchtext)


def distance_calculator(lat1,lon1,lat2,lon2):
    playdate_address=(lat1,lon1)
    search_address=(lat2,lon2)
    distance=geodesic(playdate_address,search_address).km
    return distance
