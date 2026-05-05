# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy import select

# from database.db import get_session
# from models.user import User
# from schemas.auth import LoginRequest

# router = APIRouter(tags=["Auth"])


# @router.post("/login")
# async def login(
#     data: LoginRequest,
#     db: AsyncSession = Depends(get_session)
# ):
#     result = await db.execute(
#         select(User).where(User.username == data.username)
#     )
#     user = result.scalar_one_or_none()

#     if not user or user.password != data.password:
#         raise HTTPException(status_code=401, detail="Invalid credentials")

#     return {
#         "message": "Login successful",
#         "user_id": user.id,
#         "role": user.role
#     }