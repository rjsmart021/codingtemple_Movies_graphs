from flask import jsonify, request

from Movies import app
from Movies.models import Genre
from Movies import db
from Genre.schemas import GenreSchema


Genre_schema = GenreSchema()




@app.route('/Genres', methods=['POST'])
def add_Genre():
   """
   Add Genre . Example POST data format
   {
   "Genre_name": "abc",
   "email": "abc@domain.com",
   :phone_number": "7774445556"
   }
   :return: success or error message
   """
   try:
       data = request.get_json()
       errors = Genre_schema.validate(data)
       if errors:
           return jsonify(errors), 400
       email = data.get("email")
       phone_number = data.get("phone_number")
       # Check if the Genre already exists based on email or phone number
       existing_Genre = Genre.query.filter(
           (Genre.email == email) | (Genre.phone_number == phone_number)
       ).first()


       if existing_Genre:
           return jsonify({"message": f"Genre already existed"})
       Genre = Genre(Genre_name=data["Genre_name"], email=data["email"],
                           phone_number=data["phone_number"])


       # Add the new Genre to the database
       db.session.add(Genre)
       db.session.commit()


       return jsonify({"message": "Genre added successfully"})
   except Exception as e:
       return jsonify({"Error": f"Genre not added. Error {e}"})




@app.route('/Genres/<int:Genre_id>', methods=['GET'])
def get_Genre(Genre_id):
   """
   Get Genre data based on ID provided
   :param Genre_id: ID of the registered Genre.
   :return: Genre details oif found else Error message
   """
   try:
       Genre = Genre.query.get(Genre_id)


       if Genre:
           Genre_data = {
               "Genre_id": Genre.Genre_id,
               "Genre_name": Genre.Genre_name,
               "email": Genre.email,
               "phone_number": Genre.phone_number
           }
           return jsonify(Genre_data)
       else:
           return jsonify({"message": "Genre not found"})


   except Exception as e:
       print(f"Error in getting Genre. Error Message: {e}")
       return jsonify(
           {"message": f"Error while fetching Genre with ID: {Genre_id}. Error: {e}"})




@app.route('/Genres/<int:Genre_id>', methods=['PUT'])
def update_user(Genre_id):
   """
   Update the Genre details.
   example PUT data to update;
   {
   "Genre_name": "name",
   "email": "email",
   "phone_number": "number"
   }
   :param Genre_id:
   :return:
   """
   try:
       Genre = Genre.query.get(Genre_id)


       if Genre:
           data = request.get_json()
           error = Genre_schema.validate(data)
           if error:
               return jsonify(error), 400
           Genre.Genre_name = data.get('Genre_name', Genre.Genre_name)
           Genre.email = data.get('email', Genre.email)
           Genre.phone_number = data.get('phone_number', Genre.phone_number)


           db.session.commit()
           return jsonify({"message": "Genre updated successfully"})
       else:
           return jsonify({"message": "Genre Not Found!!!"})
   except Exception as e:
       return jsonify({"message": f"error in updating Genre. Error: {e}"})




@app.route('/Genres/<int:Genre_id>', methods=['DELETE'])
def delete_user(Genre_id):
   """
   Delete user based on the ID provided
   :param Genre_id: ID of the Genre to delete
   :return: success message if user deleted successfully else None
   """


   try:
       Genre = Genre.query.get(Genre_id)


       if Genre:
           # Delete the Genre from the database
           db.session.delete(Genre)
           db.session.commit()
           return jsonify({"message": "Genre deleted successfully"})
       else:
           return jsonify({"message": "Genre not found"})


   except Exception as e:
       return jsonify({"message": f"error in deleting Genre. Error: {e}"})
