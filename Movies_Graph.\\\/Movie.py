from flask import jsonify, request


from Movies import app
from Movies.models import Movie
from Movies import db
from Movie.schemas import MovieSchema


Movie_schema = MovieSchema()




@app.route('/Movies', methods=['POST'])
def add_Movie():
   """
   Add Movie . Example POST data format
   {
   "Movie_name": "abc",
   "email": "abc@domain.com",
   :phone_number": "7774445556"
   }
   :return: success or error message
   """
   try:
       data = request.get_json()
       errors = Movie_schema.validate(data)
       if errors:
           return jsonify(errors), 400
       email = data.get("email")
       phone_number = data.get("phone_number")
       # Check if the Movie already exists based on email or phone number
       existing_Movie = Movie.query.filter(
           (Movie.email == email) | (Movie.phone_number == phone_number)
       ).first()


       if existing_Movie:
           return jsonify({"message": f"Movie already existed"})
       Movie = Movie(Movie_name=data["Movie_name"], email=data["email"],
                           phone_number=data["phone_number"])


       # Add the new Movie to the database
       db.session.add(Movie)
       db.session.commit()


       return jsonify({"message": "Movie added successfully"})
   except Exception as e:
       return jsonify({"Error": f"Movie not added. Error {e}"})




@app.route('/Movies/<int:Movie_id>', methods=['GET'])
def get_Movie(Movie_id):
   """
   Get Movie data based on ID provided
   :param Movie_id: ID of the registered Movie.
   :return: Movie details oif found else Error message
   """
   try:
       Movie = Movie.query.get(Movie_id)


       if Movie:
           Movie_data = {
               "Movie_id": Movie.Movie_id,
               "Movie_name": Movie.Movie_name,
               "email": Movie.email,
               "phone_number": Movie.phone_number
           }
           return jsonify(Movie_data)
       else:
           return jsonify({"message": "Movie not found"})


   except Exception as e:
       print(f"Error in getting Movie. Error Message: {e}")
       return jsonify(
           {"message": f"Error while fetching Movie with ID: {Movie_id}. Error: {e}"})




@app.route('/Movies/<int:Movie_id>', methods=['PUT'])
def update_user(Movie_id):
   """
   Update the Movie details.
   example PUT data to update;
   {
   "Movie_name": "name",
   "email": "email",
   "phone_number": "number"
   }
   :param Movie_id:
   :return:
   """
   try:
       Movie = Movie.query.get(Movie_id)


       if Movie:
           data = request.get_json()
           error = Movie_schema.validate(data)
           if error:
               return jsonify(error), 400
           Movie.Movie_name = data.get('Movie_name', Movie.Movie_name)
           Movie.email = data.get('email', Movie.email)
           Movie.phone_number = data.get('phone_number', Movie.phone_number)


           db.session.commit()
           return jsonify({"message": "Movie updated successfully"})
       else:
           return jsonify({"message": "Movie Not Found!!!"})
   except Exception as e:
       return jsonify({"message": f"error in updating Movie. Error: {e}"})




@app.route('/Movies/<int:Movie_id>', methods=['DELETE'])
def delete_user(Movie_id):
   """
   Delete user based on the ID provided
   :param Movie_id: ID of the Movie to delete
   :return: success message if user deleted successfully else None
   """


   try:
       Movie = Movie.query.get(Movie_id)


       if Movie:
           # Delete the Movie from the database
           db.session.delete(Movie)
           db.session.commit()
           return jsonify({"message": "Movie deleted successfully"})
       else:
           return jsonify({"message": "Movie not found"})


   except Exception as e:
       return jsonify({"message": f"error in deleting Movie. Error: {e}"})