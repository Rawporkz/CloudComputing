from fastapi import FastAPI, HTTPException
import mysql.connector
from pydantic import BaseModel
from mysql.connector import Error

app = FastAPI()

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="xyz-university-db.ciorbgfjwp67.us-east-1.rds.amazonaws.com",
            user="admin",
            password="XYZ-University123",
            database="students_db",
            ssl_disabled=True,
        )
        return connection
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {e}")

# Data model for a student
class Student(BaseModel):
    name: str
    address: str = None
    city: str = None     
    state: str = None   
    email: str          
    phone_number: str = None 

# Add a new student
@app.post("/students/")
def add_student(student: Student):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = """
        INSERT INTO students (name, address, city, state, email, phone_number)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (student.name, student.address, student.city, student.state, student.email, student.phone_number)
        cursor.execute(query, values)
        connection.commit()
        student_id = cursor.lastrowid
        return {"id": student_id, "student": student}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error adding student: {e}")
    finally:
        cursor.close()
        connection.close()

# Delete a student by ID
@app.delete("/students/{student_id}")
def delete_student(student_id: int):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = "DELETE FROM students WHERE id = %s"
        cursor.execute(query, (student_id,))
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"message": "Student deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error deleting student: {e}")
    finally:
        cursor.close()
        connection.close()

# Edit a student by ID
@app.put("/students/{student_id}")
def edit_student(student_id: int, updated_student: Student):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        query = """
        UPDATE students
        SET name = %s, address = %s, city = %s, state = %s, email = %s, phone_number = %s
        WHERE id = %s
        """
        values = (
            updated_student.name,
            updated_student.address,
            updated_student.city,
            updated_student.state,
            updated_student.email,
            updated_student.phone_number,
            student_id,
        )
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Student not found")
        return {"id": student_id, "student": updated_student}
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error updating student: {e}")
    finally:
        cursor.close()
        connection.close()

# List all students
@app.get("/students/")
def list_students():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT * FROM students"
        cursor.execute(query)
        students = cursor.fetchall()
        return students
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error fetching students: {e}")
    finally:
        cursor.close()
        connection.close()

# Health check endpoint
@app.get("/")
def list_students():
    return {"status": "OK"}
