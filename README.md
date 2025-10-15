Student Management API

A simple REST API built with FastAPI to manage student information. This project allows you to create, retrieve, update, and search student records using an in-memory data store.

Table of Contents
- Features
- Technologies
- Installation
- Usage
  - Running the API
  - API Endpoints
  - Tutorial: Using the API
- Code Explanation
  - Dependencies and Setup
  - Data Model
  - Endpoints
- Limitations
- Contributing
- License

Features
- Retrieve a student by ID.
- Search students by name or list all students.
- Create new student records.
- Update existing student records.
- Input validation using Pydantic.
- Error handling with proper HTTP status codes.
- Interactive API documentation via FastAPI's Swagger UI.

Technologies
- Python 3.8+: Programming language.
- FastAPI: Web framework for building APIs.
- Pydantic: Data validation and settings management.
- Uvicorn: ASGI server for running the FastAPI application.

Installation
1. Clone the repository:
   git clone https://github.com/your-username/student-management-api.git
   cd student-management-api

2. Create a virtual environment (optional but recommended):
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
   pip install fastapi uvicorn pydantic

4. Save the code:
   Save the provided code in a file named main.py.

Usage

Running the API
1. Start the FastAPI server using Uvicorn:
   uvicorn main:app --reload
   - main:app refers to the app object in main.py.
   - --reload enables auto-reload for development.

2. Access the API:
   - Open your browser or API client (e.g., Postman, curl) and navigate to http://127.0.0.1:8000.
   - Visit http://127.0.0.1:8000/docs for interactive Swagger UI documentation.

API Endpoints
| Method | Endpoint                | Description                              | Parameters                          |
|--------|-------------------------|------------------------------------------|-------------------------------------|
| GET    | /                       | Returns a welcome message.               | None                                |
| GET    | /students/{student_id}  | Retrieves a student by ID.               | student_id (int, required, >0)      |
| GET    | /students/search        | Searches students by name or lists all.  | name (str, optional)                |
| POST   | /students/{student_id}  | Creates a new student.                   | student_id (int, required, >0), body: {name: str, age: int} |
| PUT    | /students/{student_id}  | Updates an existing student.             | student_id (int, required, >0), body: {name: str, age: int} |

Tutorial: Using the API
This tutorial walks you through using the API with curl or the Swagger UI.

1. Access the root endpoint:
   curl http://127.0.0.1:8000
   Response:
   {"message": "Hello, World!"}

2. Get a student by ID:
   curl http://127.0.0.1:8000/students/1
   Response:
   {"name": "Alice", "age": 20}
   If the ID doesn't exist:
   {"detail": "Student not found"}

3. Search students by name:
   curl "http://127.0.0.1:8000/students/search?name=Ali"
   Response:
   {"data": [{"name": "Alice", "age": 20}]}

4. List all students:
   curl http://127.0.0.1:8000/students/search
   Response:
   {"data": [{"name": "Alice", "age": 20}, {"name": "Bob", "age": 22}, {"name": "Charlie", "age": 23}]}

5. Create a new student:
   curl -X POST http://127.0.0.1:8000/students/4 -H "Content-Type: application/json" -d '{"name": "David", "age": 21}'
   Response:
   {"message": "Student created successfully", "data": {"name": "David", "age": 21}}

6. Update a student:
   curl -X PUT http://127.0.0.1:8000/students/4 -H "Content-Type: application/json" -d '{"name": "David", "age": 22}'
   Response:
   {"message": "Student updated successfully", "data": {"name": "David", "age": 22}}

7. Using Swagger UI:
   - Open http://127.0.0.1:8000/docs.
   - Explore endpoints, test requests, and view responses interactively.

Code Explanation

Dependencies and Setup
- Imports:
  - FastAPI, Path, Query, HTTPException: From FastAPI for building the API, handling path/query parameters, and throwing HTTP errors.
  - Optional, List: From typing for type hints.
  - BaseModel: From Pydantic for data validation.
- FastAPI App:
  app = FastAPI()
  Creates a FastAPI application instance.
- In-memory Data:
  students = {
      1: {"name": "Alice", "age": 20},
      2: {"name": "Bob", "age": 22},
      3: {"name": "Charlie", "age": 23}
  }
  A dictionary storing student data (ID as key, name and age as values). Note: This is non-persistent and resets on server restart.

Data Model
- Student Model:
  class Student(BaseModel):
      name: str
      age: int
  A Pydantic model defining the structure of a student (name as string, age as integer). Used for request body validation and response attached to the commit message.

Endpoints
1. Root Endpoint (/):
   @app.get("/", response_model=dict)
   def index():
       """Root endpoint returning a welcome message."""
       return {"message": "Hello, World!"}
   - Purpose: Returns a simple welcome message.
   - Response: A JSON object with a message key.
   - Use Case: Test if the API is running.

2. Get Student by ID (/students/{student_id}):
   @app.get("/students/{student_id}", response_model=Student)
   def get_student(student_id: int = Path(..., description="The ID of the student to retrieve", gt=0)):
       """Retrieve a student by their ID."""
       student = students.get(student_id)
       if not student:
           raise HTTPException(status_code=404, detail="Student not found")
       return student
   - Purpose: Retrieves a student's details by their ID.
   - Parameters: student_id (integer, required, must be >0).
   - Validation: Uses Path to ensure student_id is positive.
   - Response: Returns the student data or a 404 error if not found.
   - Response Model: Ensures the response matches the Student schema.

3. Search Students (/students/search):
   @app.get("/students/search", response_model=dict)
   def search_students(name: Optional[str] = Query(None, description="The name to search for")):
       """Search for students by name or return all students if no name is provided."""
       if name:
           results = [student for student in students.values() if name.lower() in student["name"].lower()]
           if not results:
               raise HTTPException(status_code=404, detail=f"No students found with name: {name}")
           return {"data": results}
       return {"data": list(students.values())}
   - Purpose: Searches students by name (case-insensitive) or lists all students.
   - Parameters: name (optional string, query parameter).
   - Logic: Filters students whose names contain the query string or returns all students if no name is provided.
   - Response: A JSON object with a data key containing a list of students or a 404 error if no matches.

4. Create Student (/students/{student_id}):
   @app.post("/students/{student_id}", response_model=dict)
   def create_student(student_id: int = Path(..., description="The ID for the new student", gt=0), student: Student = None):
       """Create a new student with the given ID."""
       if student_id in students:
           raise HTTPException(status_code=400, detail="Student ID already exists")
       students[student_id] = student.dict()
       return {
           "message": "Student created successfully",
           "data": students[student_id]
       }
   - Purpose: Creates a new student with the specified ID.
   - Parameters:
     - student_id (integer, required, >0).
     - student (JSON body matching the Student model).
   - Validation: Checks if the ID already exists (returns 400 if it does).
   - Logic: Stores the student data in the students dictionary.
   - Response: Confirms creation with the student data.

5. Update Student (/students/{student_id}):
   @app.put("/students/{student_id}", response_model=dict)
   def update_student(student_id: int = Path(..., description="The ID of the student to update", gt=0), student: Student = None):
       """Update an existing student's information."""
       if student_id not in students:
           raise HTTPException(status_code=404, detail="Student not found")
       students[student_id] = student.dict()
       return {
           "message": "Student updated successfully",
           "data": students[student_id]
       }
   - Purpose: Updates an existing student's details.
   - Parameters:
     - student_id (integer, required, >0).
     - student (JSON body matching the Student model).
   - Validation: Checks if the ID exists (returns 404 if not).
   - Logic: Updates the student data in the students dictionary.
   - Response: Confirms update with the updated student data.

Limitations
- Data Persistence: The students dictionary is in-memory, so data is lost when the server restarts. For production, consider using a database (e.g., SQLite, PostgreSQL).
- Scalability: The in-memory store is not suitable for large datasets or concurrent access.
- Security: No authentication or authorization is implemented. Add JWT or OAuth for secure access in production.
- Input Validation: Basic validation is provided by Pydantic, but additional checks (e.g., age range, name format) could be added.

Contributing
1. Fork the repository.
2. Create a feature branch (git checkout -b feature/your-feature).
3. Commit your changes (git commit -m 'Add your feature').
4. Push to the branch (git push origin feature/your-feature).
5. Open a Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
