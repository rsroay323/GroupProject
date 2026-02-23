from fastapi import APIRouter

router = APIRouter()

@router.get("/events")
def get_events():
    return [
        {"title": "Quiz Night", "time": "8 PM"},
        {"title": "Coding Club", "time": "5 PM"}
    ]
