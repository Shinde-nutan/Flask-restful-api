from flask_login import current_user, login_required
from app import db
from flask import request
from flask_restful import Resource
from models import Movie , Rating
from schemas import MovieSchema
from sqlalchemy import extract, or_


movie_schema = MovieSchema()

class MovieCreate(Resource):
    @login_required
    def post(self):
        try:
            data = movie_schema.load(request.json)
            new_movie = Movie(
                title=data['title'],
                description=data['description'],
                release_date=data['release_date'],
                director=data['director'],
                genre=data['genre'],
                average_rating=data['average_rating'],
                ticket_price=data['ticket_price'],
                cast=data['cast']
            )
            db.session.add(new_movie)
            db.session.commit()
            return {'message': 'Movie created successfully'}, 201
        except Exception as e:
            return {'message': f'Error creating the movie: {str(e)}'}, 500


class MovieList(Resource):
    def get(self):

        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('limit', 10))
        genre = request.args.get('genre')
        director = request.args.get('director')
        release_year = request.args.get('release_year')
        search_query = request.args.get('search')
        sort_by = request.args.get('sort_by')

        # Fetch all movies
        movies = Movie.query

        # Apply filters if provided
        if genre:
            movies = movies.filter_by(genre=genre)

        if director:
            movies = movies.filter_by(director=director)

        if release_year:
            movies = movies.filter(extract('year', Movie.release_date) == int(release_year))

        # Apply search if provided
        if search_query:
            movies = movies.filter(
                or_(
                    Movie.title.ilike(f'%{search_query}%'),
                    Movie.cast.ilike(f'%{search_query}%'),
                    Movie.description.ilike(f'%{search_query}%'),
                    Movie.genre.ilike(f'%{search_query}%')
                )
            )

        # Apply sorting if provided
        if sort_by == 'release_date':
            movies = movies.order_by(Movie.release_date)

        if sort_by == 'ticket_price':
            movies = movies.order_by(Movie.ticket_price)


        paginated_movies = movies.paginate(page=page, per_page=page_size, error_out=False)

        if page > paginated_movies.pages:
            return {'movies': [], 'total_pages': 0, 'current_page': page, 'total_movies': 0}, 200

        # Convert paginated movies to a list of dictionaries
        movie_list = [
            {
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'release_date': movie.release_date.strftime('%Y-%m-%d'),
                'director': movie.director,
                'genre': movie.genre,
                'average_rating': movie.average_rating,
                'ticket_price': movie.ticket_price,
                'cast': movie.cast
            }
            for movie in paginated_movies.items
        ]

        return {
            'movies': movie_list,
            'total_pages': paginated_movies.pages,
            'current_page': paginated_movies.page,
            'total_movies': paginated_movies.total,
        }, 200


class MovieDetails(Resource):
    def get(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie:
            movie_data = {
                'id': movie.id,
                'title': movie.title,
                'description': movie.description,
                'release_date': movie.release_date.strftime('%Y-%m-%d'),
                'director': movie.director,
                'genre': movie.genre,
                'average_rating': movie.average_rating,
                'ticket_price': movie.ticket_price,
                'cast': movie.cast
            }
            return movie_data, 200
        return {'message': 'Movie not found'}, 404
    
    def post(self, movie_id):
        rating_value = request.json.get('rating')
        if not rating_value or not (1 <= rating_value <= 10):
            return {'message': 'Invalid rating. Please provide a rating between 1 and 10.'}, 400

        movie = Movie.query.get(movie_id)
        if not movie:
            return {'message': 'Movie not found'}, 404

        # Assuming you have a user authentication system, get the user ID
        user_id = current_user.id

        # Check if the user has already rated the movie
        existing_rating = Rating.query.filter_by(user_id=user_id, movie_id=movie_id).first()

        
        if existing_rating:
            return {'message': 'You have already rated this movie'}, 400

        # Create a new rating
        new_rating = Rating(rating=rating_value, user_id=user_id, movie_id=movie_id)
        db.session.add(new_rating)
        db.session.commit()

        return {'message': 'Rating added successfully'}, 201
    

class MovieUpdate(Resource):
    @login_required
    def put(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie and (current_user.is_admin or current_user == movie.creator):
            data = movie_schema.load(request.json)
            movie.title = data.get('title', movie.title)
            movie.description = data.get('description', movie.description)
            movie.release_date = data.get('release_date')
            movie.director = data.get('director', movie.director)
            movie.genre = data.get('genre', movie.genre)
            movie.average_rating = data.get('average_rating', movie.average_rating)
            movie.ticket_price = data.get('ticket_price', movie.ticket_price)
            movie.cast = data.get('cast', movie.cast)
            db.session.commit()
            return {'message': 'Movie updated successfully'}, 200
        return {'message': 'Movie not found'}, 404


class MovieDelete(Resource):
    @login_required
    def delete(self, movie_id):
        movie = Movie.query.get(movie_id)
        if movie and (current_user.is_admin or current_user == movie.creator):
            db.session.delete(movie)
            db.session.commit()
            return {'message': 'Movie deleted successfully'}, 200
        return {'message': 'Movie not found'}, 404
