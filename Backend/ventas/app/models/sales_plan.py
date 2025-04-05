from sqlalchemy import Integer, String, Float, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List

from app.lib.database import db
from .model import Model


class SalesPlan(db.Model, Model):
    """
    Sales Plan model representing sales targets for sellers.
    Has a one-to-many relationship with sales plan sellers.
    """
    __tablename__ = 'sales_plans'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    descripcion: Mapped[str] = mapped_column(String(500), nullable=False)
    valor_objetivo: Mapped[float] = mapped_column(Float, nullable=False)
    fecha_inicio: Mapped[str] = mapped_column(String(10), nullable=False)  # YYYY-MM-DD format (10 chars)
    fecha_fin: Mapped[str] = mapped_column(String(10), nullable=False)  # YYYY-MM-DD format (10 chars)

    # One-to-many relationship with sales plan sellers
    sellers: Mapped[List["SalesPlanSeller"]] = relationship(
        "SalesPlanSeller",
        back_populates="sales_plan",
        cascade="all, delete-orphan"
    )
