from datetime import timedelta
import os
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

class Config:
    _instance = None
    
    def __new__(cls):
        # Wzorzec Singleton: zapewnia, że istnieje tylko jedna instancja klasy Config
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        # Klucz tajny aplikacji (do podpisywania tokenów)
        self.SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
        
        # Konfiguracja bazy danych MariaDB
        DB_USER = os.getenv('DB_USER', 'root')  # Nazwa użytkownika bazy danych
        DB_PASSWORD = os.getenv('DB_PASSWORD', '')  # Hasło użytkownika bazy danych
        DB_HOST = os.getenv('DB_HOST', 'localhost')  # Adres hosta bazy danych
        DB_NAME = os.getenv('DB_NAME', 'oauth_db')  # Nazwa bazy danych
        
        # URI bazy danych dla SQLAlchemy
        self.SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False  # Wyłączenie śledzenia zmian w SQLAlchemy (oszczędność zasobów)
        
        # Ustawienia czasu życia tokenów
        self.ACCESS_TOKEN_EXPIRE_MINUTES = 30  # Czas wygaśnięcia tokenu dostępu (w minutach)
        self.REFRESH_TOKEN_EXPIRE_DAYS = 30  # Czas wygaśnięcia tokenu odświeżania (w dniach)
        self.TOKEN_BLACKLIST_EXPIRE_MINUTES = 1  # Czas przechowywania zablokowanego tokenu (w minutach)
