from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

# Inicjalizacja obiektu SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    # Definicja tabeli `User` (użytkownik) w bazie danych
    id = db.Column(db.Integer, primary_key=True)  # Kolumna `id` - klucz główny
    username = db.Column(db.String(80), unique=True, nullable=False)  # Kolumna `username` - unikalna nazwa użytkownika
    password_hash = db.Column(db.String(256), nullable=False)  # Kolumna `password_hash` - hasz hasła
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Kolumna `created_at` - czas utworzenia użytkownika
    
    def __init__(self, username, password):
        # Konstruktor klasy User
        self.username = username  # Ustawienie nazwy użytkownika
        self.password_hash = generate_password_hash(password)  # Generowanie hasza hasła
        self.created_at = datetime.utcnow()  # Ustawienie aktualnej daty i godziny

    def check_password(self, password):
        # Sprawdza poprawność wprowadzonego hasła względem zapisanego hasza
        return check_password_hash(self.password_hash, password)

class TokenBlacklist(db.Model):
    # Definicja tabeli `TokenBlacklist` (czarna lista tokenów) w bazie danych
    id = db.Column(db.Integer, primary_key=True)  # Kolumna `id` - klucz główny
    token = db.Column(db.String(500), unique=True, nullable=False)  # Kolumna `token` - unikalny token na czarnej liście
    blacklisted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Kolumna `blacklisted_on` - czas dodania tokenu na czarną listę
    
    def __init__(self, token):
        # Konstruktor klasy TokenBlacklist
        self.token = token  # Ustawienie tokenu
