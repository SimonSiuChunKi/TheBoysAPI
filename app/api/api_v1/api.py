from fastapi import APIRouter

from app.api.api_v1.endpoints import users
from app.api.api_v1.endpoints import resources
from app.api.api_v1.endpoints import hand_signs
from app.api.api_v1.endpoints import lessons
from app.api.api_v1.endpoints import cources
from app.api.api_v1.endpoints import quiz

router = APIRouter()

router.include_router(users.router, prefix="/users", tags=["Users"])

router.include_router(resources.router, prefix="/resources", tags=["Resources"])

router.include_router(hand_signs.router, prefix="/hand_signs", tags=["Hand Signs"])

router.include_router(lessons.router, prefix="/lessons", tags=["Lessons"])

router.include_router(cources.router, prefix="/courses", tags=["Courses"])

router.include_router(quiz.router, prefix="/quiz", tags=["Quiz"])