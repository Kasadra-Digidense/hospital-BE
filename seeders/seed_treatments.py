import pandas as pd
from sqlalchemy import select

from models.treatment import Treatment


async def seed_treatments(session):

    # Check existing data
    result = await session.execute(select(Treatment))
    existing = result.scalars().first()

    if existing:
        print("Treatments already seeded")
        return

    # Read CSV
    df = pd.read_csv("treatments.csv")

    # Remove empty rows
    df = df.dropna(subset=["item_name", "price"])

    for _, row in df.iterrows():

        treatment = Treatment(
            item_name=str(row["item_name"]).strip(),
            price=float(row["price"])
        )

        session.add(treatment)

    await session.commit()

    print("Treatments inserted successfully")



# import asyncio
# import pandas as pd

# from database.db import AsyncSessionLocal
# from models.treatment import Treatment


# async def seed_data():

#     # Read CSV
#     df = pd.read_csv("treatments.csv")

#     # Remove empty rows
#     df = df.dropna(subset=["item_name", "price"])

#     async with AsyncSessionLocal() as session:

#         for _, row in df.iterrows():

#             treatment = Treatment(
#                 item_name=str(row["item_name"]).strip(),
#                 price=float(row["price"])
#             )

#             session.add(treatment)

#         await session.commit()

#     print("Treatments inserted successfully")


# asyncio.run(seed_data())