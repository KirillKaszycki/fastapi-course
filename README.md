# Finance tracker

## Create the environment

### 1. Install
```
git clone https://github.com/KirillKaszycki/fastapi-course.git
```
### 2. Make environment
```
cd fastapi-course
```
```
python3.12 -m venv venv
```
```
source venv/bin/activate
```
```
pip install --upgrade pip
```
```
pip install -r requirements.txt
```
### 3. Launch server
```
uvicorn main:app --reload
```
#### Stop server
Hotkeys: control + c

### Run with Docker

```bash
cp .env.example .env
docker compose up --build
```

The API is available at `http://localhost:8000`, and Docker PostgreSQL is available at
`localhost:5433`. Change `POSTGRES_PASSWORD` in `.env` before using this setup
outside local development. Stop containers with:

```bash
docker compose down
```

To also delete the PostgreSQL data volume:

```bash
docker compose down -v
```

### 4. Tree

- **API (router) layer:**\
Handles HTTP requests and responses. Defines endpoints, validates input, and delegates business logic to the service layer.
- **Repository layer:**\
Responsible for direct interaction with the database. Encapsulates CRUD operations and data access logic.
- **Services layer:**\
Contains business logic. Orchestrates operations, applies rules, and coordinates between API and repository layers.

```
fastapi-course/
├── app/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── __init__.py
│   │   │   ├── operations.py
│   │   │   ├── users.py
│   │   │   └── wallets.py
│   │   └── __init__.py
│   ├── repository/
│   │   ├── __init__.py
│   │   ├── operations.py
│   │   ├── users.py
│   │   └── wallets.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── exchange_service.py
│   │   ├── operations.py
│   │   ├── users.py
│   │   └── wallets.py
│   ├── static/
│   │   ├── css/
│   │   │   ├── bootstrap.min.css
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── app.js
│   │   │   └── bootstrap.bundle.min.js
│   │   └── index.html
│   ├── __init__.py
│   ├── database.py
│   ├── dependency.py
│   ├── enum.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   ├── test_api/
│   │   ├── __init__.py
│   │   └── test_operations.py
│   ├── __init__.py
│   └── conftest.py
├── venv/
├── .gitignore
├── finance.db
├── test.db
├── main.py
├── README.md
└── requirements.txt
```
