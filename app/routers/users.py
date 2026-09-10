from fastapi import APIRouter


router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/test")
def test_user_router():
    return {
        "message": "Users router is working"
    }