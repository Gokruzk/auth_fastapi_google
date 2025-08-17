from datetime import datetime
from sqlalchemy import String
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(AsyncAttrs, DeclarativeBase):
    pass


class LogModel(Base):
    __tablename__ = "registro_log"

    id_log: Mapped[int] = mapped_column(autoincrement=True,primary_key=True)
    quien: Mapped[str] = mapped_column(
        String(150), nullable=False)
    accion: Mapped[str] = mapped_column(String(50), nullable=False)
    entidad_afectada: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    extra_data: Mapped[str] = mapped_column(
        String(10), nullable=False)
