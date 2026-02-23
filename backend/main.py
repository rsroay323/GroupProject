from fastapi import FastAPI
from routes import facilities, events, transport, clubs

app = FastAPI()

app.include_router(facilities.router)
app.include_router(events.router)
app.include_router(transport.router)
app.include_router(clubs.router)

@app.get("/")
def home():
    return {"message": "Live Campus Hub API running"}
