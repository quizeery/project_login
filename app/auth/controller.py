from flask import Blueprint, request, jsonify, render_template
from app.auth.service import AuthService
from app.models import User, db

# Tworzymy blueprint dla uwierzytelniania
auth_bp = Blueprint('auth', __name__)
auth_service = AuthService()

# Rejestracja nowego użytkownika
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Sprawdzamy, czy użytkownik już istnieje
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists'}), 400
    
    # Tworzymy nowego użytkownika i zapisujemy do bazy
    user = User(username, password)
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

# Logowanie użytkownika
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Sprawdzamy dane logowania
    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Tworzymy tokeny dostępu i odświeżenia
    access_token, refresh_token = auth_service.create_tokens(username)
    
    response = jsonify({'message': 'Login successful'})
    response.headers['X-Access-Token'] = access_token  # Przekazujemy token dostępu
    response.headers['X-Refresh-Token'] = refresh_token  # Przekazujemy token odświeżenia
    
    return response

# Odświeżenie tokena
@auth_bp.route('/refresh', methods=['POST'])
def refresh():
    refresh_token = request.headers.get('X-Refresh-Token')
    if not refresh_token:
        return jsonify({'error': 'Refresh token required'}), 401
    
    # Walidacja tokena odświeżania
    username = auth_service.validate_token(refresh_token)
    if not username:
        return jsonify({'error': 'Invalid refresh token'}), 401
    
    # Tworzymy nowe tokeny
    access_token, new_refresh_token = auth_service.create_tokens(username)
    
    response = jsonify({'message': 'Token refreshed'})
    response.headers['X-Access-Token'] = access_token  # Przekazujemy nowy token dostępu
    response.headers['X-Refresh-Token'] = new_refresh_token  # Przekazujemy nowy token odświeżenia
    
    return response

# Wylogowanie użytkownika
@auth_bp.route('/logout', methods=['POST'])
def logout():
    access_token = request.headers.get('X-Access-Token')
    refresh_token = request.headers.get('X-Refresh-Token')
    
    # Czarna lista tokenów
    if access_token:
        auth_service.blacklist_token(access_token)
    if refresh_token:
        auth_service.blacklist_token(refresh_token)
    
    return jsonify({'message': 'Logged out successfully'}), 200 

# Strona logowania (formularz)
@auth_bp.route('/login-page')
def login_page():
    return render_template('login.html')  # Wyświetlenie formularza logowania