from fastapi import APIRouter
from fastapi import Query

from . import connection

router = APIRouter()

@router.get("/")
async def get_all_lessons(course_id: int = Query(..., description="Provide the course id")):
    return get_all_lessons(course_id)


def get_all_lessons(course_id: int):

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
async def get_lesson_details(lesson_id: int = Query(..., description="Provide the lesson id")):
    return get_lesson_details(lesson_id)

def get_lesson_details(lesson_id: int):

    tmp = []

    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = f"SELECT v.AuslanSign, v.url AS VideoURL, i.url AS ImageURL FROM Videos v CROSS JOIN Images i ON v.AuslanSign = i.AuslanSign WHERE v.LessonID = {lesson_id};"
            cursor.execute(sql)

            # Fetch all the rows
            result = cursor.fetchall()

            # Print the results
            for row in result:
                tmp.append({"auslan_sign": row[0], "video_url": row[1], "image_url": row[2]})
            
    except Exception as e:
        print(f"Failed to start the lesson. Here is the reason: {e}")

    return tmp

@router.get("/start_a_lesson")
async def start_a_lesson(user_id: int = Query(..., description="Provide the user id"), lesson_id: int = Query(..., description="Provide the lesson id")):
    return start_a_lesson(user_id, lesson_id)

def start_a_lesson(user_id, lesson_id):
    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = f"INSERT INTO LessonHistory (UserID, LessonID, Status, DateCompleted) VALUES ({user_id}, {lesson_id}, 'In Progress', NULL);"
            cursor.execute(sql)
            
    except Exception as e:
        print(f"Failed to start the lesson. Here is the reason: {e}")

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

@router.get("/start_a_lesson")
async def start_a_lesson(user_id: int = Query(..., description="Provide the user id"), lesson_id: int = Query(..., description="Provide the lesson id")):
    return start_a_lesson(user_id, lesson_id)

def start_a_lesson(user_id, lesson_id):
    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = f"INSERT INTO LessonHistory (UserID, LessonID, Status, DateCompleted) VALUES ({user_id}, {lesson_id}, 'In Progress', NULL);"
            cursor.execute(sql)
            
    except Exception as e:
        print(f"Failed to start the lesson. Here is the reason: {e}")

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
