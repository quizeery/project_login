# OAuth REST API

## Описание
Это REST API реализует OAuth аутентификацию с использованием токенов доступа и обновления.

## Особенности
- Singleton паттерн для конфигурации и сервиса аутентификации
- Токены JWT в заголовках
- Blacklist для разлогиненных токенов
- Время жизни токена доступа: 30 минут
- Время жизни токена обновления: 30 дней
- Время хранения токена в черном списке: 1 минута

## API Endpoints

### POST /register
Регистрация нового пользователя
- Body: `{"username": "string", "password": "string"}`
- Response: 201 Created

### POST /login
Аутентификация пользователя
- Body: `{"username": "string", "password": "string"}`
- Response: 200 OK
- Headers: X-Access-Token, X-Refresh-Token

### POST /refresh
Обновление токена доступа
- Headers required: X-Refresh-Token
- Response: 200 OK
- Headers: X-Access-Token, X-Refresh-Token

### POST /logout
Выход из системы
- Headers required: X-Access-Token, X-Refresh-Token
- Response: 200 OK

## Установка и запуск
1. Установите зависимости: `pip install -r requirements.txt`
2. Настройте переменные окружения в `.env`
3. Запустите тесты: `pytest`
4. Запустите сервер: `flask run` 