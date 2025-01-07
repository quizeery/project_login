import os

# Aktywacja wirtualnego środowiska (virtual environment)
# Tworzy ścieżkę do pliku `activate_this.py` znajdującego się w folderze `venv`.
venv_path = os.path.join(os.path.dirname(__file__), 'venv', 'Scripts', 'activate_this.py')

# Sprawdzenie, czy plik `activate_this.py` istnieje.
# Jeśli plik istnieje, otwiera go i wykonuje jego zawartość, aktywując wirtualne środowisko.
if os.path.exists(venv_path):
    with open(venv_path) as file:
        exec(file.read(), dict(__file__=venv_path))

# Importuje funkcję `create_app` z modułu `app`.
from app import create_app

# Tworzy instancję aplikacji za pomocą funkcji `create_app`.
app = create_app()

# Główna część programu. Jeśli plik jest uruchamiany jako główny skrypt, 
# startuje aplikację w trybie debugowania.
if __name__ == '__main__':
    app.run(debug=True)