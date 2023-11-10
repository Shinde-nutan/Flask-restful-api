
#import required library
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api
from flask_migrate import Migrate
from flasgger import Swagger

#Configure app
app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

# Configuration for SQLAlchemy database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'flaskassigment'


# Initialize SQLAlchemy and Migrate
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Initialize Flask-Login
login_manager = LoginManager(app)
#login_manager.login_view = 'login'

from models import User
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

from resources import MovieCreate, MovieDelete, MovieDetails, MovieList, MovieUpdate
from auth import UserLogin,  UserRegistration ,  UserLogout 

# Add resources to the API
api.add_resource(UserRegistration, '/register')
api.add_resource(UserLogin, '/login')
api.add_resource(UserLogout, '/logout')
api.add_resource(MovieCreate, '/movies')  # POST request for creating a movie
api.add_resource(MovieList, '/movies')    # GET request for listing all movies
api.add_resource(MovieDetails, '/movies/<int:movie_id>')  # GET request for a specific movie
api.add_resource(MovieUpdate, '/movies/<int:movie_id>')  # PUT request for updating a specific movie
api.add_resource(MovieDelete, '/movies/<int:movie_id>')  # DELETE request for deleting a specific movie



if __name__ == '__main__':
    app.run(debug=True)
