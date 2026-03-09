from fastapi import FastAPI
from database import engine, Base
from routes import events, clubs, facilities, transport

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(events.router)
app.include_router(clubs.router)
app.include_router(facilities.router)
app.include_router(transport.router)

@app.get("/")
def home():
    return {"message": "Live Campus Hub API running"}
