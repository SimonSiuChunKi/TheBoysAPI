from fastapi import APIRouter
from fastapi import Query

from ..endpoints import connection


router = APIRouter()

@router.get("/images")
async def get_images(auslan_sign: str = Query(..., description="Provide an Auslan hand sign")):
    return get_images(auslan_sign)


def get_images(auslan_sign: str):

    urls = set()

    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = f'SELECT Url FROM Images i WHERE AuslanSign = "{auslan_sign}";'
            cursor.execute(sql)
            
            # Fetch all the rows
            result = cursor.fetchall()
            
            # Print the results
            for row in result:
                urls.update(row)

    except Exception as e:
        print(f"Failed to get the URLs. Here is the reason: {e}")
    
    return urls

@router.get("/videos")
async def get_videoss(auslan_sign: str = Query(..., description="Provide an Auslan hand sign")):
    return get_videos(auslan_sign)


def get_videos(auslan_sign: str):

    urls = set()

    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = f'SELECT Url FROM Videos v WHERE AuslanSign = "{auslan_sign}";'
            cursor.execute(sql)
            
            # Fetch all the rows
            result = cursor.fetchall()
            
            # Print the results
            for row in result:
                urls.update(row)

    except Exception as e:
        print(f"Failed to get the URLs. Here is the reason: {e}")

    return urls