from flask import Flask
from .models import db
from .views import main_blueprint
# from .auth.google_auth import auth_blueprint # Uncomment after creating google_auth.py
# from .payments.stripe_integration import payment_blueprint # Uncomment after creating stripe_integration.py

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)

    app.register_blueprint(main_blueprint)
    # app.register_blueprint(auth_blueprint) # Uncomment after creating google_auth.py
    # app.register_blueprint(payment_blueprint) # Uncomment after creating stripe_integration.py

    return app
