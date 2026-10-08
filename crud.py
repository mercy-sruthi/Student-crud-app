from typing import Optional
from sqlalchemy.orm import Session

import models
import schemas


def create_student(db: Session, student: schemas.StudentCreate) -> models.Student:
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


def get_student(db: Session, student_id: str) -> Optional[models.Student]:
    return db.query(models.Student).filter(
        models.Student.student_id == student_id
    ).first()


def get_students(
    db: Session,
    skip: int = 0,
    limit: int = 100,
    name: Optional[str] = None,
    course: Optional[str] = None,
):
    query = db.query(models.Student)
    if name:
        query = query.filter(models.Student.name.ilike(f"%{name}%"))
    if course:
        query = query.filter(models.Student.course.ilike(f"%{course}%"))
    return query.offset(skip).limit(limit).all()


def update_student(
    db: Session, student_id: str, updates: schemas.StudentUpdate
) -> Optional[models.Student]:
    db_student = get_student(db, student_id)
    if not db_student:
        return None
    update_data = updates.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_student, field, value)
    db.commit()
    db.refresh(db_student)
    return db_student


def delete_student(db: Session, student_id: str) -> bool:
    db_student = get_student(db, student_id)
    if not db_student:
        return False
    db.delete(db_student)
    db.commit()
    return True
