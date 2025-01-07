from flask import Flask
from app.models import db
from app.auth.controller import auth_bp

def create_app(config_name=None):
    app = Flask(__name__)
    
    # Ładowanie konfiguracji aplikacji
    from app.config import Config
    app.config.from_object(Config())
    
    # Inicjalizacja bazy danych
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Tworzenie wszystkich tabel w bazie danych, jeśli jeszcze nie istnieją
    
    # Rejestracja blueprintów (modułów)
    app.register_blueprint(auth_bp)  # Rejestruje blueprint związany z modułem uwierzytelniania
    
    return app