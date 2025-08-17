from sqlalchemy.ext.asyncio import AsyncSession
from auth.repository import LogRepository
from auth.factory import LogFactory
from auth.dtos import LogDTO


class LogService():
    def __init__(self, db: AsyncSession):
        self.repository = LogRepository(db)

    async def register_log(self, log_data: LogDTO) -> LogDTO:
        try:
            # Create entity to insert in db
            log_data = LogFactory.create_log_from_dto(log_data)

            # Insert data in db
            log_post = await self.repository.register_log(log_data)

            # Validate model to return
            log_post = LogDTO.model_validate(log_post)

        except Exception as e:
            print(e)
            return "US9999"
        else:
            return log_post
