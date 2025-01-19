from flask_sqlalchemy import SQLAlchemy

# Create an instance of the SQLAlchemy class
db = SQLAlchemy()

# Initialize the database with the Flask app
def initialize_database(app, db):
    db.init_app(app)