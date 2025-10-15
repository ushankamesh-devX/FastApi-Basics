from fastapi import FastAPI, Path, Query
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


students = {
    1: {"name": "Alice", "age": 20},
    2: {"name": "Bob", "age": 22},
    3: {"name": "Charlie", "age": 23}
}

class Student(BaseModel):
    name: str
    age: int


@app.get("/")
def index():
    return {"message": "Hello, World!"}


# @app.get("/students/{student_id}")
# def get_student(student_id: int = Path(None, description="The ID of the student to retrieve", gt=0)):
#     student = students.get(student_id)
#     if student:
#         return student
#     return {"error": "Student not found"}


@app.get("/students/search")
def search_students( *, name: Optional[str] = Query(None, description="The name to search for")):
    if name:
        results = [student for student in students.values() if name.lower() in student["name"].lower()]
        if results:
            return {"results": results}
        return {"error": f"No students found with that name: {name}"}
    return {"students": list(students.values())}

@app.post("/students/{student_id}")
def create_student(student_id: int, student: Student):
    if student_id in students:
        return {"error": "Student ID already exists"}
    students[student_id] = student
    return {
        "message": "Student created successfully",
        "student": students[student_id]
    }


@app.put("/students/{student_id}")
def update_student(student_id: int, student: Student):
    if student_id not in students:
        return {"error": "Student not found"}
    students[student_id] = student
    return {
        "message": "Student updated successfully",
        "student": students[student_id]
    }