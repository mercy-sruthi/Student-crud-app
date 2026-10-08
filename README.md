# Student Database CRUD Application

Internship project - Python Backend Development | EWB Edu Tech Pvt. Ltd.

A FastAPI backend that manages student records (Create, Read, Update, Delete)
with persistent SQLite storage.

## Features
- Full CRUD on student records
- Filter by name or course, with pagination
- Input validation (required fields, email format, email or phone required)
- 404 for missing records, 400 for duplicate student IDs
- Auto-generated API docs at `/docs`

## Project Files
- `main.py` - FastAPI app and routes
- `models.py` - SQLAlchemy Student table
- `schemas.py` - Pydantic validation schemas
- `crud.py` - database operations
- `database.py` - SQLite connection
- `requirements.txt` - dependencies

## Prerequisites
- Python 3.9+

## Installation
```bash
git clone https://github.com/mercy-sruthi/Student-crud-app.git
cd Student-crud-app
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Run
```bash
uvicorn main:app --reload
```
Open http://127.0.0.1:8000/docs to test every endpoint.
The file `students.db` is created automatically on first run.

## Endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| POST | /students | Create a student |
| GET | /students | List / filter students (?name=, ?course=) |
| GET | /students/{student_id} | View a student |
| PUT / PATCH | /students/{student_id} | Update a student |
| DELETE | /students/{student_id} | Delete a student |

## Student Fields
Required: `student_id`, `name`, `date_of_birth`, and at least one of `email` / `phone`.
Optional: `course`, `address`, `enrollment_date`.

## Testing Example
```bash
curl -X POST http://127.0.0.1:8000/students \
  -H "Content-Type: application/json" \
  -d '{"student_id":"S001","name":"Asha Verma","date_of_birth":"2006-03-14","email":"asha@example.com","course":"Computer Science"}'

curl http://127.0.0.1:8000/students
```

## Notes
- Use dummy data only. No real student information is stored in this repository.
- `students.db` is excluded from Git.
