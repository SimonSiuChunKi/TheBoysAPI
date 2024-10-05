from fastapi import APIRouter

from . import connection

router = APIRouter()

@router.get("/")
async def get_all_courses():
    return get_all_courses()


def get_all_courses():

    courses = []

    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = "SELECT ID, CourseName, Description, ImageURL FROM Courses"
            cursor.execute(sql)
            
            # Fetch all the rows
            result = cursor.fetchall()
            
            # Print the results
            for row in result:
                holder = {}
                holder["ID"] = row[0]
                holder["CourseName"] = row[1]
                holder["Description"] = row[2]
                holder["ImageURL"] = row[3]
                courses.append(holder)
    
    except Exception as e:
        print(f"Failed to get the cources. Here is the reason: {e}")

    return courses