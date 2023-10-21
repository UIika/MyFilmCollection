from time import sleep
from flask import Flask, flash, redirect, render_template, session, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from db import db, db_init, Movie, User, UserMovie
from flask_login import LoginManager, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'koi2938vur2987rvu2120i0cm3902m4u18437'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///moviesdb.db'
db_init(app)

login_manager = LoginManager()
login_manager.login_view = 'home'
login_manager.init_app(app)

with app.app_context():
    context = {
        'movies': Movie.query.all()
    }

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/')
def home():
    if current_user.is_authenticated:
        user_movies = db.session.query(Movie, UserMovie).\
            join(UserMovie, UserMovie.movie_id == Movie.id).\
                filter(UserMovie.user_id == current_user.id).all()
    else:
        flash('You must be logged in to view your collection.', 'warning')
        user_movies = []
    return render_template('home.html', title='Your Movie Collection', user_movies=user_movies, **context)

@app.route('/movie/<int:id>/')
def movie(id):
    movie=Movie.query.get(id)
    user_movie = UserMovie.query.filter_by(user_id=current_user.id, movie_id=id).first() if current_user.is_authenticated else None
    user_rating = user_movie.rating if user_movie else None
    return render_template('movie.html', title=movie.title, movie=movie, user_rating=user_rating, **context)

@app.route('/add/<int:id>/', methods=['POST'])
def add(id):
    new_movie = UserMovie(user_id=current_user.id, movie_id=id, rating=request.form.get('rating'))
    db.session.add(new_movie)
    db.session.commit()
    return redirect(url_for('movie', id=id))

@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    movie = UserMovie.query.filter_by(user_id=current_user.id, movie_id=id).first()
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for('movie', id=id))

@app.route('/about/') 
def about():
    return 'About Hello World!'

@app.route('/signup/', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        if password1 != password2:
            flash('Passwords must match.', 'error')
            return redirect(url_for('signup'))

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email address already exists.', 'error')
            return redirect(url_for('signup'))

        new_user = User(email=email, name=name, password=generate_password_hash(password1, method='pbkdf2:sha1'))
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        
        return redirect('/')
    return render_template('register.html', title='Sign Up', **context)

@app.route('/', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
    else:
        login_user(user)
    return redirect('/')

@app.route('/loogout/')
def logout():
    logout_user()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
