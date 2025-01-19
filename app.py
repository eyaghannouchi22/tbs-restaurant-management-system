from flask import Flask
from routes.init import init_routes
from database import db, initialize_database

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0000@localhost:5432/university_restaurant'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
initialize_database(app, db)

# Initialize Routes
init_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
