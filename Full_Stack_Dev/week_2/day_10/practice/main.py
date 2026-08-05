from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from week_2.day_10.practice.model import StudentService

app = FastAPI()

student_service = StudentService()


class StudentRequest(BaseModel):
    name: str
    age: int


@app.post("/students/{student_id}")
def create_student(student_id: int, student: StudentRequest):
    return student_service.add_student(
        student_id,
        student.name,
        student.age
    )


@app.get("/students")
def get_students():
    return student_service.get_students()


@app.get("/students/{student_id}")
def get_student(student_id: int):
    student = student_service.get_student(student_id)

    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student


@app.put("/students/{student_id}")
def update_student(student_id: int, student: StudentRequest):

    updated_student = student_service.update_student(
        student_id,
        student.name,
        student.age
    )

    if not updated_student:
        raise HTTPException(status_code=404, detail="Student not found")

    return updated_student


@app.delete("/students/{student_id}")
def delete_student(student_id: int):

    deleted_student = student_service.delete_student(student_id)

    if not deleted_student:
        raise HTTPException(status_code=404, detail="Student not found")

    return {"message": "Student deleted successfully"}