from datetime import datetime, date
from typing import Optional, List
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, String, Integer, Date, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class RolUsuarioModel(Base):
    __tablename__ = "rol_usuario"

    id_rol: Mapped[int] = mapped_column(primary_key=True)
    rol: Mapped[str] = mapped_column(String(20), nullable=False)

    # Relación uno a muchos: un rol puede tener varios usuarios
    usuarios: Mapped[List["UsuarioModel"]] = relationship(back_populates="rol")


class UsuarioModel(Base):
    __tablename__ = "usuario"

    email: Mapped[str] = mapped_column(String(100), primary_key=True)
    cedula: Mapped[str] = mapped_column(
        String(10), nullable=False)  # asumimos que cedula es el PK
    nombres: Mapped[str] = mapped_column(String(50), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(50), nullable=False)
    celular: Mapped[str] = mapped_column(String(20), nullable=False)
    bool_status: Mapped[bool]
    created_at: Mapped[date] = mapped_column(Date, nullable=False)
    updated_at: Mapped[date] = mapped_column(Date, nullable=True)
    deleted_at: Mapped[date] = mapped_column(Date, nullable=True)

    id_rol: Mapped[int] = mapped_column(ForeignKey("rol_usuario.id_rol"))
    contrasena: Mapped[str] = mapped_column(String(200), nullable=False)
    rol: Mapped["RolUsuarioModel"] = relationship(back_populates="usuarios")
