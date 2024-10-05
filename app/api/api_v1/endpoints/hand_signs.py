from fastapi import APIRouter

from . import connection
from fastapi import Query

router = APIRouter()

@router.get("/")
async def get_all_hand_signs():
    return get_all_hand_signs()


def get_all_hand_signs():

    hand_signs = []

    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = "SELECT v.AuslanSign, i.Url FROM Videos v INNER JOIN Images i ON v.AuslanSign = i.AuslanSign"
            cursor.execute(sql)
            
            # Fetch all the rows
            result = cursor.fetchall()
            
            # Print the results
            for row in result:
                tmp = {}
                tmp["AuslanSign"] = row[0]
                tmp["ImageUrl"] = row[1]
                hand_signs.append(tmp)
    
    except Exception as e:
        print(f"Failed to get the hand signs. Here is the reason: {e}")

    return hand_signs


@router.get("/hand_sign")
async def get_hand_sign(hand_sign: str = Query(..., description="Provide the user id")):
    return get_hand_sign(hand_sign)


def get_hand_sign(hand_sign):

    hand_signs = []

    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = f"SELECT v.AuslanSign, i.Url, v.Url FROM Videos v INNER JOIN Images i ON v.AuslanSign = i.AuslanSign WHERE v.AuslanSign = '{hand_sign}'"
            cursor.execute(sql)
            
            # Fetch all the rows
            result = cursor.fetchall()
            
            # Print the results
            for row in result:
                tmp = {}
                tmp["AuslanSign"] = row[0]
                tmp["ImageUrl"] = row[1]
                tmp["VideoUrl"] = row[2]
                hand_signs.append(tmp)
    
    except Exception as e:
        print(f"Failed to get the hand signs. Here is the reason: {e}")

    return hand_signs