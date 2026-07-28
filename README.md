# Task Tracker API

A RESTful task-management API built with **FastAPI**, **SQLModel**, and **SQLite**.

This project allows users to create, retrieve, update, and delete tasks. Task data is stored persistently in a local SQLite database, and all endpoints can be tested through FastAPI’s automatically generated Swagger documentation.

<p>
  <img src="https://img.shields.io/badge/Python-3.14-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/SQLModel-ORM-CC2927" alt="SQLModel" />
  <img src="https://img.shields.io/badge/SQLite-Database-003B57?logo=sqlite&logoColor=white" alt="SQLite" />
</p>

## Features

- Create new tasks
- Retrieve all tasks
- Retrieve one task by ID
- Update existing tasks
- Delete tasks
- Store task data persistently with SQLite
- Validate request data with SQLModel
- Return appropriate HTTP status codes
- Handle missing tasks with clear error responses
- Test endpoints through Swagger UI

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Return the API welcome message |
| `GET` | `/tasks` | Retrieve all tasks |
| `GET` | `/tasks/{task_id}` | Retrieve one task by ID |
| `POST` | `/tasks` | Create a new task |
| `PUT` | `/tasks/{task_id}` | Update an existing task |
| `DELETE` | `/tasks/{task_id}` | Delete a task |

## Task Model

Each task contains an automatically generated ID, a title, and a completion status.

```json
{
  "id": 1,
  "title": "Study FastAPI",
  "completed": false
}
```

## Technologies

- Python
- FastAPI
- SQLModel
- SQLite
- Uvicorn
- Swagger UI
- Git and GitHub

## Project Structure

```text
task-tracker-api/
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```

The virtual environment and local database file are excluded from GitHub.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Asmaabe01/task-tracker-api.git
cd task-tracker-api
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 4. Install the dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Start the development server

```bash
python -m uvicorn main:app --reload
```

The API will run at:

```text
http://127.0.0.1:8000
```

## API Documentation

After starting the server, open the Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Alternative ReDoc documentation is available at:

```text
http://127.0.0.1:8000/redoc
```

## Example Request

Create a task using `POST /tasks`:

```json
{
  "title": "Complete Python exercises",
  "completed": false
}
```

Example response:

```json
{
  "id": 1,
  "title": "Complete Python exercises",
  "completed": false
}
```

If a requested task does not exist, the API returns:

```json
{
  "detail": "Task not found"
}
```

## What I Learned

Through this project, I practised:

- Building REST API endpoints
- Using HTTP methods and status codes
- Validating request data
- Working with path parameters
- Handling API errors
- Connecting FastAPI to SQLite
- Performing database CRUD operations
- Managing project dependencies with a virtual environment
- Using Git and GitHub for version control

## Future Improvements

- Add automated tests
- Add task filtering and search
- Add pagination
- Add task priorities and due dates
- Add user authentication
- Add Docker support
- Migrate to PostgreSQL or MySQL
- Deploy the API online

## Author

**Asmae Bequi**

- [GitHub](https://github.com/Asmaabe01)
- [LinkedIn](https://www.linkedin.com/in/asmaa-bequi-609070422/)
- [LeetCode](https://leetcode.com/u/asmaebequi/)
