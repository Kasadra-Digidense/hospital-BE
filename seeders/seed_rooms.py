import pandas as pd
from sqlalchemy import select

from models.room import Room


async def seed_rooms(session):

    # Check existing data
    result = await session.execute(select(Room))
    existing = result.scalars().first()

    if existing:
        print("Rooms already seeded")
        return

    # Read CSV
    df = pd.read_csv("rooms.csv")

    # Remove empty rows
    df = df.dropna(subset=["RoomGroup", "RoomNumber", "Rate"])

    for _, row in df.iterrows():

        room = Room(
            room_group=str(row["RoomGroup"]).strip(),
            room_number=str(row["RoomNumber"]).strip(),
            rate=float(row["Rate"])
        )

        session.add(room)

    await session.commit()

    print("Rooms inserted successfully")








# import asyncio
# import pandas as pd

# from database.db import AsyncSessionLocal
# from models.room import Room


# async def seed_rooms():

#     # Read CSV
#     df = pd.read_csv("rooms.csv")

#     # Remove empty rows
#     df = df.dropna(subset=["RoomGroup", "RoomNumber", "Rate"])

#     async with AsyncSessionLocal() as session:

#         for _, row in df.iterrows():

#             room = Room(
#                 room_group=str(row["RoomGroup"]).strip(),
#                 room_number=str(row["RoomNumber"]).strip(),
#                 rate=float(row["Rate"])
#             )

#             session.add(room)

#         await session.commit()

#     print("✅ Rooms inserted successfully")


# asyncio.run(seed_rooms())