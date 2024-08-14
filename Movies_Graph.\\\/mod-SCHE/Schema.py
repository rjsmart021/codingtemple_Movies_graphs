# schema.py
import graphene
from graphene_sqlalchemy import SQLAlchemyObjectType
from app.models import Movie as MovieModel, Genre as GenreModel, movie_genres, db
from sqlalchemy.orm import Session

class Movie(SQLAlchemyObjectType):
    class Meta:
        model = MovieModel

class Genre(SQLAlchemyObjectType):
    class Meta:
        model = GenreModel

class Query(graphene.ObjectType):
    movies = graphene.List(Movie)
    search_movies = graphene.List(Movie, title=graphene.String(), director=graphene.String(), year=graphene.Int())
    get_movies_by_genre = graphene.List(Movie, genre_id=graphene.Int())
    get_genre_by_movie = graphene.List(Genre, movie_id=graphene.Int())

    def resolve_movies(root, info):
        return db.session.execute(db.select(MovieModel)).scalars()

    def resolve_search_movies(root, info, title=None, director=None, year=None):        
        query = db.select(MovieModel)
        if title:
            query = query.where(MovieModel.title.ilike(f'%{title}%'))
        if director:
            query = query.where(MovieModel.director.ilike(f'%{director}%'))
        if year:
            query = query.where(MovieModel.year == year)
        results = db.session.execute(query).scalars().all()
        return results
    
    def resolve_get_movies_by_genre(root, info, genre_id):
        return db.session.query(MovieModel).join(movie_genres).filter(movie_genres.c.genre_id == genre_id).all()

    def resolve_get_genre_by_movie(root, info, movie_id):
        return db.session.query(GenreModel).join(movie_genres).filter(movie_genres.c.movie_id == movie_id).all()
    
class AddMovie(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        director = graphene.String(required=True)
        year = graphene.Int(required=True)
        genres = graphene.List(graphene.String, required=True)

    movie = graphene.Field(Movie)

    def mutate(root, info, title, director, year, genres):

        # get genres from table, or add them if necessary
        genre_instances = []
        for genre_name in genres:
            genre_instance = db.session.query(GenreModel).filter_by(name=genre_name).first()
            if not genre_instance:
                genre_instance = GenreModel(name=genre_name)
            genre_instances.append(genre_instance)

        movie = MovieModel(title=title, director=director, year=year, genres=genre_instances) 
        return AddMovie(movie=movie)

class UpdateMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        title = graphene.String()
        director = graphene.String()
        year = graphene.Int()
        genres = graphene.List(graphene.String, required=True)

    movie = graphene.Field(Movie)

    def mutate(root, info, id, title=None, director=None, year=None, genres=None):
        movie = db.session.get(MovieModel, id)         
        if not movie:
            return None
        if title:    
            movie.title = title
        if director:
            movie.director = director
        if year:
            movie.year = year
        if genres:
            genre_instances = []
            for genre_name in genres:
                genre_instance = db.session.query(GenreModel).filter_by(name=genre_name).first()
                if not genre_instance:
                    genre_instance = GenreModel(name=genre_name)
                genre_instances.append(genre_instance)
            movie.genres = genre_instances
        db.session.commit()
        return UpdateMovie(movie=movie)

class DeleteMovie(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    message = graphene.String()

    def mutate(root, info, id):
        movie = db.session.get(MovieModel, id)         
        if not movie:
            return DeleteMovie(message="That movie was not found")
        else:
            db.session.delete(movie)
            db.session.commit()
            return DeleteMovie(message="Success")


### GENRE MUTATIONS ###

class AddGenre(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    genre = graphene.Field(Genre)

    def mutate(root, info, name):
        genre = GenreModel(name=name)
        return AddGenre(genre=genre)

class UpdateGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        name = graphene.String()

    genre = graphene.Field(Genre)

    def mutate(root, info, id, name=None):
        genre = db.session.get(GenreModel, id)         
        if not genre:
            return None
        if name:    
            genre.name = name
        db.session.commit()
        return UpdateGenre(genre=genre)

class DeleteGenre(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    message = graphene.String()

    def mutate(root, info, id):
        genre = db.session.get(GenreModel, id)         
        if not genre:
            return DeleteGenre(message="That genre was not found")
        else:
            db.session.delete(genre)
            db.session.commit()
            return DeleteGenre(message="Success")


class Mutation(graphene.ObjectType):
    create_movie = AddMovie.Field()
    update_movie = UpdateMovie.Field()
    delete_movie = DeleteMovie.Field()
    create_genre = AddGenre.Field()
    update_genre = UpdateGenre.Field()
    delete_genre = DeleteGenre.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)