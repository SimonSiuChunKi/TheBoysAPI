from fastapi import APIRouter

from . import connection

router = APIRouter()

@router.get("/")
async def get_all_hand_signs():
    return get_all_hand_signs()


def get_all_hand_signs():

    hand_signs = set()

    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = "SELECT DISTINCT (v.AuslanSign) FROM Videos v UNION SELECT DISTINCT (i.AuslanSign) FROM Images i"
            cursor.execute(sql)
            
            # Fetch all the rows
            result = cursor.fetchall()
            
            # Print the results
            for row in result:
                hand_signs.update(row)
    
    finally:
        # Close the connection
        connection.close()

    return hand_signs