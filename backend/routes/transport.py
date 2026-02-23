from fastapi import APIRouter

router = APIRouter()

@router.get("/transport")
def get_transport():
    return {"bus": "Arrives in 10 minutes"}
