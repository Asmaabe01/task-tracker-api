# Task Tracker API

A secure and containerized RESTful task-management API built with **FastAPI**, **SQLModel**, **PostgreSQL**, **JWT authentication**, **Alembic**, **Pytest**, and **Docker**.

The application allows users to register, authenticate, and manage their own tasks. It includes task priorities, filtering, pagination, automated testing, database migrations, environment-based configuration, and Docker support.

<p align="left">
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLModel-ORM-CC2927" alt="SQLModel" />
  <img src="https://img.shields.io/badge/PostgreSQL-Database-4169E1?logo=postgresql&logoColor=white" alt="PostgreSQL" />
  <img src="https://img.shields.io/badge/Docker-Container-2496ED?logo=docker&logoColor=white" alt="Docker" />
  <img src="https://img.shields.io/badge/Pytest-Testing-0A9EDC?logo=pytest&logoColor=white" alt="Pytest" />
</p>

---

## Features

- User registration and login
- Secure password hashing
- JWT authentication
- Protected API routes
- User-owned tasks
- Create, read, update, and delete tasks
- Task priorities: `low`, `medium`, `high`
- Filter tasks by completion status
- Filter tasks by priority
- Pagination support
- PostgreSQL database
- SQLModel ORM
- Alembic database migrations
- Environment-based configuration
- Automated API tests with Pytest
- Isolated test database
- Docker and Docker Compose support
- Swagger UI and ReDoc documentation

---

## API Endpoints

### Users

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/users/register` | Register a new user |
| `POST` | `/users/login` | Log in and receive a JWT token |

### Tasks

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/tasks/` | Retrieve the authenticated user's tasks |
| `GET` | `/tasks/{task_id}` | Retrieve one task |
| `POST` | `/tasks/` | Create a task |
| `PUT` | `/tasks/{task_id}` | Update a task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

### General

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Return the API welcome message |

---

## Authentication

The API uses **JWT bearer authentication**.

Authentication flow:

```text
Register
   ↓
Password is hashed
   ↓
User is stored in PostgreSQL
   ↓
Login
   ↓
Password is verified
   ↓
JWT access token is generated
   ↓
Token is sent with protected requests
   ↓
FastAPI identifies the current user
```

Protected task routes ensure that users can only access their own tasks.

---

## Task Model

A task contains:

```json
{
  "id": 1,
  "title": "Study FastAPI",
  "completed": false,
  "priority": "high",
  "user_id": 1
}
```

### Priority Values

The API accepts only:

```text
low
medium
high
```

Invalid priority values are rejected automatically.

---

## Filtering

Tasks can be filtered using query parameters.

### Filter by completion status

```http
GET /tasks/?completed=true
```

### Filter by priority

```http
GET /tasks/?priority=high
```

### Combine filters

```http
GET /tasks/?completed=false&priority=high
```

---

## Pagination

Tasks support pagination using `page` and `limit`.

Example:

```http
GET /tasks/?page=1&limit=10
```

Filters and pagination can also be combined:

```http
GET /tasks/?completed=false&priority=high&page=1&limit=5
```

---

## Technologies

| Technology | Purpose |
|---|---|
| Python | Programming language |
| FastAPI | Web API framework |
| SQLModel | ORM and data models |
| PostgreSQL | Production database |
| Psycopg | PostgreSQL driver |
| Pydantic Settings | Environment configuration |
| JWT | Authentication |
| Pwdlib | Password hashing |
| Alembic | Database migrations |
| Pytest | Automated testing |
| HTTPX | API testing |
| Docker | Application containerization |
| Docker Compose | Multi-container orchestration |
| Uvicorn | ASGI server |
| Swagger UI | Interactive API documentation |
| Git / GitHub | Version control |

---

## Project Structure

```text
task-tracker-api/
│
├── app/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── task.py
│   │   └── user.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── tasks.py
│   │   └── users.py
│   │
│   ├── __init__.py
│   ├── config.py
│   ├── database.py
│   ├── main.py
│   └── security.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_tasks.py
│   └── test_users.py
│
├── alembic/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pytest.ini
├── requirements.txt
└── README.md
```

---

## Environment Variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
DATABASE_URL=postgresql+psycopg://postgres:postgres@db:5432/tasktracker
```

The real `.env` file is excluded from GitHub.

An `.env.example` file is included to show the required variables.

---

# Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/Asmaabe01/task-tracker-api.git
cd task-tracker-api
```

## 2. Create a virtual environment

```bash
python -m venv .venv
```

## 3. Activate the virtual environment

### Windows PowerShell

```powershell
.\.venv\Scripts\Activate.ps1
```

## 4. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## 5. Create the environment file

Create:

```text
.env
```

and configure the required environment variables.

---

# Running with Docker

## Build the application

```bash
docker compose build
```

## Start FastAPI and PostgreSQL

```bash
docker compose up -d
```

## Check running containers

```bash
docker compose ps
```

You should see two services:

```text
api    FastAPI application
db     PostgreSQL database
```

## Apply database migrations

```bash
docker compose exec api alembic upgrade head
```

## Stop the application

```bash
docker compose down
```

---

## API Documentation

After starting the application:

### Swagger UI

```text
http://127.0.0.1:8000/docs
```

### ReDoc

```text
http://127.0.0.1:8000/redoc
```

---

# Usage Examples

## Register a User

**Endpoint**

```http
POST /users/register
```

**Request**

```json
{
  "username": "testuser",
  "password": "password123"
}
```

**Response**

```json
{
  "id": 1,
  "username": "testuser"
}
```

---

## Login

**Endpoint**

```http
POST /users/login
```

A successful login returns:

```json
{
  "access_token": "your-jwt-access-token",
  "token_type": "bearer"
}
```

The token is then used to access protected endpoints.

---

## Create a Task

**Endpoint**

```http
POST /tasks/
```

**Request**

```json
{
  "title": "Complete FastAPI project",
  "completed": false,
  "priority": "high"
}
```

**Response**

```json
{
  "id": 1,
  "title": "Complete FastAPI project",
  "completed": false,
  "priority": "high",
  "user_id": 1
}
```

---

## Update a Task

**Endpoint**

```http
PUT /tasks/1
```

**Request**

```json
{
  "title": "Finish FastAPI project",
  "completed": true,
  "priority": "medium"
}
```

---

## Delete a Task

```http
DELETE /tasks/1
```

Example response:

```json
{
  "message": "Task deleted"
}
```

---

# Error Handling

### Invalid Login

```json
{
  "detail": "Invalid username or password"
}
```

### Invalid Token

```json
{
  "detail": "Invalid token"
}
```

### Expired Token

```json
{
  "detail": "Token expired"
}
```

### Missing or Unauthorized Task

```json
{
  "detail": "Task not found"
}
```

Using `404` for tasks belonging to another user avoids exposing information about resources the authenticated user does not own.

---

# Automated Tests

The project includes automated tests for:

- Home endpoint
- User registration
- User login
- Invalid login attempts
- Task creation
- Task retrieval
- Task updates
- Task deletion
- User authorization
- Task ownership protection

Run:

```bash
python -m pytest
```

Current test result:

```text
9 passed
```

The test suite uses an isolated SQLite test database so automated tests do not modify the PostgreSQL development database.

---

# Database Migrations

The project uses **Alembic** to manage database schema changes.

Create a migration:

```bash
alembic revision --autogenerate -m "migration description"
```

Apply migrations locally:

```bash
alembic upgrade head
```

When using Docker:

```bash
docker compose exec api alembic upgrade head
```

---

# Docker Architecture

```text
                  Docker Compose
                       │
            ┌──────────┴──────────┐
            │                     │
            ▼                     ▼
      FastAPI Container     PostgreSQL Container
           api                      db
            │                       │
            └───────────┬───────────┘
                        │
                    Database
```

The FastAPI application communicates with PostgreSQL through the Docker Compose network.

---

# Security

The project includes several basic security practices:

- Passwords are hashed before storage
- Plain-text passwords are never stored
- JWT tokens are used for authentication
- JWT tokens have expiration times
- Secrets are stored in environment variables
- `.env` is excluded from Git
- Users can only access their own tasks
- Protected routes require authentication

---

# What I Learned

Through this project, I practised:

- Building RESTful APIs
- Understanding HTTP methods and status codes
- Organizing a FastAPI project with routers and models
- Using dependency injection with `Depends`
- Validating request data
- Using SQLModel and database sessions
- Designing one-to-many database relationships
- Implementing CRUD operations
- Building user registration and login
- Hashing and verifying passwords
- Creating and validating JWT tokens
- Protecting API endpoints
- Implementing user-specific authorization
- Managing configuration using environment variables
- Working with PostgreSQL
- Managing database migrations with Alembic
- Writing automated tests with Pytest
- Using isolated test databases
- Implementing filtering and pagination
- Validating task priority values
- Containerizing an application with Docker
- Running FastAPI and PostgreSQL with Docker Compose
- Using Git and GitHub for version control

---

# Future Improvements

Possible future improvements include:

- Task due dates
- Task search
- Sorting options
- Refresh tokens
- Role-based authorization
- Additional test coverage
- CI/CD with GitHub Actions
- Cloud deployment
- Frontend integration

---

## Author

**Asmae Bequi**

[GitHub](https://github.com/Asmaabe01)  
[LinkedIn](https://www.linkedin.com/in/asmaa-bequi-609070422/)  
[LeetCode](https://leetcode.com/u/asmaebequi/)
