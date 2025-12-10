# Task & Productivity Tracker – Django Backend

A simple backend service built with Django and Django REST Framework to manage tasks for a "Task & Productivity Tracker" application.

## Features

- Create, read, update, delete tasks
- Filter tasks by **status** and **priority**
- Sort tasks by **creation date**
- Task summary API: count of tasks grouped by **status**
- Proper error handling with meaningful messages and HTTP status codes

---

## Tech Stack

- Python 3.x
- Django
- Django REST Framework
- SQLite (default Django DB)

---

## Setup & Installation

### 1. Clone the repository

```bash
1.git clone <your-repo-url>.git
cd tasktracker


2. Install dependencies
pip install -r requirements.txt

3. Run migrations
python manage.py migrate

4. Run development server
python manage.py runserver


The API will be available at: http://127.0.0.1:8000/api/

#### API Endpoints

- GET /api/tasks/ - List all tasks (supports ?status=... & ?priority=... & ?ordering=created_at|-created_at)
- POST /api/tasks/ - Create a task (JSON body)
- GET /api/tasks/<task_id>/ - Get a specific task
- PUT /api/tasks/<task_id>/ - Update a specific task (JSON body)
- DELETE /api/tasks/<task_id>/ - Delete a specific task

Example requests (curl)
Create a task
curl -X POST http://127.0.0.1:8000/api/tasks/ \
  -H "Content-Type: application/json" \
  -d '{"title":"Buy milk","description":"2 liters","priority":"HIGH","status":"PENDING"}'

List tasks
curl "http://127.0.0.1:8000/api/tasks/?status=PENDING&priority=HIGH&ordering=-created_at"

Get by ID
curl http://127.0.0.1:8000/api/tasks/1/

Update (PATCH)
curl -X PATCH http://127.0.0.1:8000/api/tasks/1/ \
  -H "Content-Type: application/json" \
  -d '{"status":"COMPLETED"}'

Delete
curl -X DELETE http://127.0.0.1:8000/api/tasks/1/