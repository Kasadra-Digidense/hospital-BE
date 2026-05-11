from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import init_db
from routes import patient, login, treatment, rooms

# IMPORTANT: import models so tables register
import models.patient
import models.treatment
import models.room

from database.db import AsyncSessionLocal
from seeders.seed_treatments import seed_treatments
from seeders.seed_rooms import seed_rooms

app = FastAPI(
    title="Ayurvedic",
    version="1.0.0",
    docs_url="/docs",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(patient.router)
app.include_router(login.router)
app.include_router(treatment.router)
app.include_router(rooms.router)

# THIS is how async DB init should be done
@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
def root():
    return {"message": "Ayurvedic API Running 🌿"}

@app.on_event("startup")
async def on_startup():
    # Create tables
    await init_db()
    # Seed master data
    async with AsyncSessionLocal() as session:
        await seed_treatments(session)
        await seed_rooms(session)