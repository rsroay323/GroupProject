from fastapi import APIRouter

router = APIRouter()

@router.get("/facilities")
def get_facilities():
    return [
        {"name": "Gym", "status": "Open"},
        {"name": "Library", "status": "Busy"}
    ]
