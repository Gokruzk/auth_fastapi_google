from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from auth.models import LogModel
from sqlalchemy import select


class LogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> List[LogModel]:
        result = await self.db.execute(select(LogModel))
        return result.scalars().all()

    async def register_log(self, log_data: LogModel) -> LogModel:
        self.db.add(log_data)
        await self.db.commit()
        await self.db.refresh(log_data)
        return log_data
