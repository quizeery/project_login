# OAuth REST API - Dokumentacja

## Opis
System autentykacji OAuth wykorzystujący tokeny JWT z automatycznym wylogowaniem po 60 sekundach.

## Funkcje
- Wzorzec Singleton dla konfiguracji i serwisu autoryzacji
- Tokeny JWT w nagłówkach HTTP
- Czarna lista tokenów
- Automatyczne wylogowanie po 60 sekundach
- Przechowywanie danych w MariaDB
- Odświeżanie tokenów

## Endpointy API

### POST /register
Rejestracja nowego użytkownika
- Body: `{"username": "string", "password": "string"}`
- Odpowiedź: 201 Created

### POST /login
Logowanie użytkownika
- Body: `{"username": "string", "password": "string"}`
- Odpowiedź: 200 OK
- Nagłówki: X-Access-Token, X-Refresh-Token

### POST /refresh
Odświeżanie tokenu dostępu
- Wymagane nagłówki: X-Refresh-Token
- Odpowiedź: 200 OK
- Nagłówki: X-Access-Token, X-Refresh-Token

### POST /logout
Wylogowanie użytkownika
- Wymagane nagłówki: X-Access-Token, X-Refresh-Token
- Odpowiedź: 200 OK

## Instalacja

1. Klonowanie repozytorium:
bash
git clone https://github.com/quizeery/project_login.git
cd oauth-api

2. Konfiguracja bazy danych MariaDB:
sql
CREATE DATABASE oauth_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

3. Konfiguracja pliku .env:
env
SECRET_KEY=project
DB_USER=root
DB_PASSWORD=root
DB_HOST=localhost
DB_NAME=oauth_db

4. Instalacja zależności:
bash
pip install -r requirements.txt

5. Uruchomienie aplikacji:
bash
python run.py

## Testowanie
- Interfejs webowy: http://localhost:5000/login-page

## Bezpieczeństwo
- Tokeny dostępu wygasają po 60 sekundach
- Tokeny odświeżania wygasają po 30 dniach
- Hasła są hashowane przed zapisaniem w bazie danych
- Tokeny są dodawane do czarnej listy po wylogowaniu

## Wymagania systemowe
- Python 3.8+
- MariaDB 10.5+
- Pakiety z requirements.txt
