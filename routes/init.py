from flask import Flask

def init_routes(app: Flask):
    from routes.auth_routes import auth_routes
    from routes.reservation_routes import reservation_routes
    from routes.meal_routes import meal_routes
    from routes.review_routes import review_routes
    from routes.user_routes import user_routes
    
    app.register_blueprint(auth_routes)
    app.register_blueprint(reservation_routes)
    app.register_blueprint(meal_routes)
    app.register_blueprint(review_routes)
    app.register_blueprint(user_routes)