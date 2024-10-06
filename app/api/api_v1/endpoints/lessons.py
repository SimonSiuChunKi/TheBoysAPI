from fastapi import APIRouter, HTTPException
from fastapi import Query
from pydantic import BaseModel
import ast
from datetime import datetime



from . import connection

router = APIRouter()

@router.get("/")
async def get_all_lessons(course_id: int = Query(..., description="Provide the course id"), user_id: str = Query(..., description="Provide an user id")):
    return get_all_lessons(course_id, user_id)


def get_all_lessons(course_id: int, user_id: str):

    lessons = []

    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = f"SELECT Name, AuslanSigns, Description, Difficulty, ImageURL, ID FROM Lessons WHERE CourseID = {course_id}"
            cursor.execute(sql)
            
            # Fetch all the rows
            result = cursor.fetchall()
            
            # Print the results
            for row in result:
                holder = {}
                holder["Lesson"] = row[0]
                holder["Description"] = row[2]
                holder["Difficulty"] = row[3]
                holder["ImageURL"] = row[4]
                holder["ID"] = row[5]
                lessons.append(holder)

            sql = f"SELECT LessonID FROM LessonHistory lh WHERE UserID = '{user_id}' AND Status = 'In Progress';"
            cursor.execute(sql)
            
            # Fetch all the rows
            result = cursor.fetchall()

            tmp = []

            for row in result:
                tmp.append(row[0])

            for i in range(0, len(lessons)):
                if lessons[i]["ID"] in tmp:
                    lessons[i]["Status"] = "In Progress"
                else:
                    lessons[i]["Status"] = "Not Yet Started"

    
    except Exception as e:
        print(f"Failed to get the lessons. Here is the reason: {e}")

    return lessons


@router.get("/get_lesson_hostory")
async def get_lesson_hostory(user_id: int = Query(..., description="Provide the user id")):
    return get_lesson_hostory(user_id)

def get_lesson_hostory(user_id: int):

    tmp = []

    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = f"SELECT * FROM LessonHistory WHERE UserID = {user_id};"
            cursor.execute(sql)

            # Fetch all the rows
            result = cursor.fetchall()

            # Print the results
            for row in result:
                tmp.append({"user_id": row[1], "lesson_id": row[2], "status": row[3], "completed_date": row[4]})
            
    except Exception as e:
        print(f"Failed to start the lesson. Here is the reason: {e}")

    return tmp

@router.get("/get_lesson_details")
async def get_lesson_details(lesson_id: int = Query(..., description="Provide the lesson id"), user_id: str = Query(..., description="Provide the user id")):
    return get_lesson_details(lesson_id, user_id)

def get_lesson_details(lesson_id: int, user_id: str):

    tmp = []

    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = f"SELECT v.AuslanSign, v.url AS VideoURL, i.url AS ImageURL, lh.Status FROM Videos v CROSS JOIN Images i ON v.AuslanSign = i.AuslanSign CROSS JOIN LessonHistory lh ON v.AuslanSign = lh.AuslanSign WHERE v.LessonID = {lesson_id} AND lh.UserID = '{user_id}'"
            cursor.execute(sql)

            # Fetch all the rows
            result = cursor.fetchall()

            # Print the results
            for row in result:
                tmp.append({"auslan_sign": row[0], "video_url": row[1], "image_url": row[2], "status": row[3]})
            
    except Exception as e:
        print(f"Failed to get the lesson details. Here is the reason: {e}")

    return tmp

# Define a Pydantic model for the request body
class StartLessonRequest(BaseModel):
    user_id: str
    lesson_id: int

@router.post("/start_a_lesson")
async def start_a_lesson(request: StartLessonRequest):
    result = start_a_lesson_db(request.user_id, request.lesson_id)
    
    if not result:
        raise HTTPException(status_code=400, detail="Failed to start the lesson.")
    
    return {"message": "Lesson started successfully"}

def start_a_lesson_db(user_id, lesson_id):
    
    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = f"SELECT AuslanSigns FROM Lessons l WHERE ID = {lesson_id};"
            cursor.execute(sql)

            # Fetch all the rows
            result = cursor.fetchall()

            auslan_signs = result[0][0]

        auslan_signs = ast.literal_eval(auslan_signs)

        with connection.cursor() as cursor:
            # Execute a query to insert the lesson start event
            sql = f"INSERT INTO LessonHistory (UserID, LessonID, Status, DateCompleted, AuslanSign) VALUES"

            for sign in auslan_signs:
                sql += f"('{user_id}', {lesson_id}, 'In Progress', NULL, '{sign}'),"
            sql = sql[:-1]
            sql += ";"
            cursor.execute(sql)
            connection.commit()  # Commit the transaction
            return True
    except Exception as e:
        print(f"Failed to start the lesson. Error: {e}")
        return False
    
class CompleteLessonRequest(BaseModel):
    user_id: str
    lesson_id: int
    auslan_sign: str

@router.post("/completed_a_lesson")
async def completed_a_lesson(request: StartLessonRequest):
    return completed_a_lesson(request.user_id, request.lesson_id, request.auslan_sign)

def completed_a_lesson(user_id, lesson_id, auslan_sign):
    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = f"UPDATE LessonHistory SET Status = 'Completed', DateCompleted = {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} WHERE UserID = '{user_id}' AND LessonID = {lesson_id} AND Status = 'In Progress' AND AuslanSign = {auslan_sign};"
            cursor.execute(sql)
            
    except Exception as e:
        print(f"Failed to complete the lesson. Here is the reason: {e}")


@router.get("/completed_a_lesson")
async def completed_a_lesson(user_id: int = Query(..., description="Provide the user id"), lesson_id: int = Query(..., description="Provide the lesson id")):
    return completed_a_lesson(user_id, lesson_id)

def completed_a_lesson(user_id, lesson_id):
    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = f"UPDATE LessonHistory SET Status = 'Completed', DateCompleted = NOW() WHERE UserID = {user_id} AND LessonID = {lesson_id} AND Status = 'In Progress';"
            cursor.execute(sql)
            
    except Exception as e:
        print(f"Failed to complete the lesson. Here is the reason: {e}")
