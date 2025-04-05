from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import Optional

from app.lib.database import db
from .model import Model


class SalesPlanSeller(db.Model, Model):
    """
    SalesPlanSeller model representing an association between a sales plan and a seller.
    It contains minimal seller reference data from the users microservice.
    """
    __tablename__ = 'sales_plan_sellers'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nombre: Mapped[str] = mapped_column(String(255), nullable=False)
    seller_id: Mapped[int] = mapped_column(Integer, nullable=False)

    # Foreign key to sales plan
    sales_plan_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey("sales_plans.id"),
        nullable=True
    )

    # Relationship with sales plan
    sales_plan = relationship(
        "SalesPlan",
        back_populates="sellers"
    )
