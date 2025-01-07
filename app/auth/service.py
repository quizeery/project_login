from datetime import datetime, timedelta
from jose import jwt
from app.config import Config
from app.models import User, TokenBlacklist, db

class AuthService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        self.config = Config()
    
    # Tworzenie tokenów dostępu i odświeżania
    def create_tokens(self, username):
        access_token = self._create_token(
            username,
            timedelta(seconds=60)  # Czas życia tokena dostępu
        )
        refresh_token = self._create_token(
            username,
            timedelta(days=self.config.REFRESH_TOKEN_EXPIRE_DAYS)  # Czas życia tokena odświeżania
        )
        return access_token, refresh_token
    
    # Wewnętrzna metoda do tworzenia tokena
    def _create_token(self, username, expires_delta):
        payload = {
            'username': username,
            'exp': datetime.utcnow() + expires_delta  # Data wygaśnięcia tokena
        }
        return jwt.encode(payload, self.config.SECRET_KEY, algorithm='HS256')
    
    # Walidacja tokena
    def validate_token(self, token):
        try:
            if self._is_token_blacklisted(token):  # Sprawdzenie, czy token jest na czarnej liście
                return None
            payload = jwt.decode(token, self.config.SECRET_KEY, algorithms=['HS256'])
            return payload['username']  # Zwraca nazwę użytkownika z ładunku tokena
        except jwt.ExpiredSignatureError:
            return None  # Token wygasł
        except jwt.JWTError:
            return None  # Błąd dekodowania tokena
    
    # Sprawdzenie, czy token znajduje się na czarnej liście
    def _is_token_blacklisted(self, token):
        return TokenBlacklist.query.filter_by(token=token).first() is not None
    
    # Dodanie tokena do czarnej listy
    def blacklist_token(self, token):
        blacklisted_token = TokenBlacklist(token=token)
        db.session.add(blacklisted_token)
        db.session.commit()