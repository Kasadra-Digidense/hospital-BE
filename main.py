from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database.db import init_db
from routes import patient, login

# 👇 IMPORTANT: import models so tables register
import models.patient
import models.user

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

# ✅ THIS is how async DB init should be done
@app.on_event("startup")
async def on_startup():
    await init_db()


@app.get("/")
def root():
    return {"message": "Ayurvedic API Running 🌿"}