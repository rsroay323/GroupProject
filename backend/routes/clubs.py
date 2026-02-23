from fastapi import APIRouter

router = APIRouter()

@router.get("/clubs")
def get_clubs():
    return [
        {"name": "Coding Club"},
        {"name": "Cybersecurity Club"}
    ]
