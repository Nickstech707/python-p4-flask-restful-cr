#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Newsletter

# Initialize the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///newsletters.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

# Set up database migration and initialization
migrate = Migrate(app, db)
db.init_app(app)

# Initialize the Flask-RESTful API
api = Api(app)

# Define the Home resource with a welcome message
class Home(Resource):
    def get(self):
        response_dict = {
            "message": "Welcome to the Newsletter RESTful API",
        }
        response = make_response(response_dict, 200)
        return response

# Add the Home resource to the API
api.add_resource(Home, '/')

# Define the Newsletters resource to handle all newsletters
class Newsletters(Resource):
    def get(self):
        # Retrieve all newsletters and convert them to a list of dictionaries
        response_dict_list = [n.to_dict() for n in Newsletter.query.all()]
        response = make_response(response_dict_list, 200)
        return response

    def post(self):
        # Create a new newsletter record from the request data
        new_record = Newsletter(
            title=request.form['title'],
            body=request.form['body'],
        )
        # Add the new record to the database session and commit
        db.session.add(new_record)
        db.session.commit()
        response_dict = new_record.to_dict()
        response = make_response(response_dict, 201)
        return response

# Add the Newsletters resource to the API
api.add_resource(Newsletters, '/newsletters')

# Define the NewsletterByID resource to handle operations on a specific newsletter by ID
class NewsletterByID(Resource):
    def get(self, id):
        # Retrieve the newsletter by ID and convert it to a dictionary
        newsletter = Newsletter.query.filter_by(id=id).first()
        if newsletter:
            response_dict = newsletter.to_dict()
            response = make_response(response_dict, 200)
        else:
            response = make_response({"error": "Newsletter not found"}, 404)
        return response

# Add the NewsletterByID resource to the API
api.add_resource(NewsletterByID, '/newsletters/<int:id>')

# Run the Flask application
if __name__ == '__main__':
    app.run(port=5555, debug=True)