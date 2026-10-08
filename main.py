from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

import models
import schemas
import crud
from database import engine, get_db

# Create the SQLite tables on startup
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Student Database CRUD API",
    description="Manage student records with Create, Read, Update and Delete.",
    version="1.0.0",
)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Student CRUD API is running. Visit /docs for the API docs."}


# CREATE
@app.post("/students", response_model=schemas.StudentOut,
          status_code=status.HTTP_201_CREATED, tags=["Students"])
def create_student(student: schemas.StudentCreate, db: Session = Depends(get_db)):
    if crud.get_student(db, student.student_id):
        raise HTTPException(
            status_code=400,
            detail=f"Student with student_id '{student.student_id}' already exists.",
        )
    return crud.create_student(db, student)


# READ (list / filter)
@app.get("/students", response_model=List[schemas.StudentOut], tags=["Students"])
def list_students(
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    course: Optional[str] = None,
    db: Session = Depends(get_db),
):
    return crud.get_students(db, skip=skip, limit=limit, name=name, course=course)


# READ (one)
@app.get("/students/{student_id}", response_model=schemas.StudentOut, tags=["Students"])
def get_student(student_id: str, db: Session = Depends(get_db)):
    db_student = crud.get_student(db, student_id)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return db_student


# UPDATE
@app.put("/students/{student_id}", response_model=schemas.StudentOut, tags=["Students"])
@app.patch("/students/{student_id}", response_model=schemas.StudentOut, tags=["Students"])
def update_student(student_id: str, updates: schemas.StudentUpdate,
                   db: Session = Depends(get_db)):
    db_student = crud.update_student(db, student_id, updates)
    if not db_student:
        raise HTTPException(status_code=404, detail="Student not found.")
    return db_student


# DELETE
@app.delete("/students/{student_id}", status_code=status.HTTP_204_NO_CONTENT,
            tags=["Students"])
def delete_student(student_id: str, db: Session = Depends(get_db)):
    if not crud.delete_student(db, student_id):
        raise HTTPException(status_code=404, detail="Student not found.")
    return None


# OPTIONAL BONUS: AI question-answering (needs ai_extension.py and Ollama)
class AIQuestion(BaseModel):
    question: str


@app.post("/ai/ask", tags=["AI Extension (optional)"])
def ask_ai(payload: AIQuestion, db: Session = Depends(get_db)):
    import ai_extension
    return {"question": payload.question,
            "answer": ai_extension.ask_question(db, payload.question)}
