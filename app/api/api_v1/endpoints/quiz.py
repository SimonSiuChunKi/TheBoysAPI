import random

from fastapi import APIRouter
from fastapi import Query

from . import connection

router = APIRouter()

@router.get("/")
async def generate_a_quiz(type: str = Query(..., description="Provide the type of the quiz")):
    return generate_a_quiz(type)


def generate_a_quiz(type):

    auslan = []

    try:
        with connection.cursor() as cursor:
            # Execute a query
            sql = f"SELECT AuslanSign FROM Videos WHERE Type = '{type}';"
            cursor.execute(sql)
            
            # Fetch all the rows
            result = cursor.fetchall()

            # Print the results
            for row in result:
                auslan.append(row[0])

    except Exception as e:
        print(f"Failed to get the AuslanSign. Here is the reason: {e}")

    random_number = random.randint(0, 5)
    random.shuffle(auslan)

    if random_number == 0:
        answer = "None of these"
        question = f"https://the-boys-bucket.s3.ap-southeast-2.amazonaws.com/video/{auslan[-1]}.mp4"
    else:
        answer = auslan[0]
        question = f"https://the-boys-bucket.s3.ap-southeast-2.amazonaws.com/video/{auslan[0]}.mp4"

    random_number = random.randint(1, 4)

    quiz = {5: "None of these", "answer": answer, "question": question}

    for i in range(1, 5):
        if i == random_number and answer != "None of these":
            quiz[i] = answer
        else:
            quiz[i] = auslan[i]

    return quiz