from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas

@router.get("/", response_model=List[schemas.AttendanceOut])
def get_attendance(group_id: int, date: date, db: Session = Depends(get_db)):
    # знаходжу відповідне заняття
    lesson = db.query(models.Lesson).filter_by(group_id=group_id).first()
    if not lesson:
        raise HTTPException(404, "Lesson not found")
    # формую статус присутності
    data = []
    for student in lesson.group.students:
        att = db.query(models.Attendance).filter_by(
            lesson_id=lesson.id, student_id=student.id, date=date
        ).first()
        data.append({
            "student_id": student.id,
            "name": f"{student.last_name} {student.first_name}",
            "present": att.present if att else False
        })
    return data

@router.post("/update")
def update_attendance(payload: List[schemas.AttendanceIn], db: Session = Depends(get_db)):
    for entry in payload:
        att = db.query(models.Attendance).filter_by(
            lesson_id=entry.lesson_id, student_id=entry.student_id, date=entry.date
        ).first()
        if att:
            att.present = entry.present
        else:
            att = models.Attendance(**entry.dict())
            db.add(att)
    db.commit()
    return {"status": "ok"}
