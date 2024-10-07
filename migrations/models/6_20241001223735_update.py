from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "students" ALTER COLUMN "phone" TYPE VARCHAR(15) USING "phone"::VARCHAR(15);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "students" ALTER COLUMN "phone" TYPE INT USING "phone"::INT;"""
