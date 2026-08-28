from uuid import UUID

from app.models.users import User
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class UserRepository:
    @staticmethod
    async def get_by_id(
        db: AsyncSession,
        user_id: UUID,
    ) -> User | None:

        result = await db.execute(select(User).where(User.id == user_id))

        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_email(
        db: AsyncSession,
        email: str,
    ) -> User | None:

        result = await db.execute(select(User).where(User.email == email))

        return result.scalar_one_or_none()
