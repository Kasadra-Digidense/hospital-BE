from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Auth"])


# Request Schema
class LoginRequest(BaseModel):
    username: str
    password: str


# Dummy Users (Hardcoded)
DUMMY_USERS = [
    {
        "id": 1,
        "username": "admin",
        "password": "admin123",
        "role": "admin"
    },
    {
        "id": 2,
        "username": "staff",
        "password": "staff123",
        "role": "staff"
    }
]


# Login API
@router.post("/login")
async def login(data: LoginRequest):
    for user in DUMMY_USERS:
        if user["username"] == data.username and user["password"] == data.password:
            return {
                "message": "Login successful",
                "user_id": user["id"],
                "role": user["role"]
            }

    raise HTTPException(status_code=401, detail="Invalid username or password")