from auth.dtos import LogDTO
from auth.models import LogModel
from datetime import datetime


class LogFactory:
    @staticmethod
    def create_log_from_dto(data: LogDTO) -> LogModel:
        return LogModel(
            quien=data["quien"],
            accion=data["accion"],
            entidad_afectada=data["entidad_afectada"],
            fecha=datetime.now(),
            extra_data=str(data["extra_data"])
        )
