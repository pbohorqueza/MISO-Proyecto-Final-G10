"""Sales plan response models."""
from typing import List
from pydantic import BaseModel, Field

from app.responses.seller import SellerResponse


class SalesPlanPath(BaseModel):
    """Parámetros de ruta para las rutas de Planes de Venta"""
    plan_id: int = Field(..., description="ID del plan de ventas")


class SalesPlanResponse(BaseModel):
    """Esquema para devolver un Plan de Ventas"""
    id: int
    nombre: str
    descripcion: str
    valor_objetivo: float
    fecha_inicio: str
    fecha_fin: str
    sellers: List[SellerResponse]


class SalesPlanListResponse(BaseModel):
    """Esquema para devolver múltiples Planes de Venta"""
    items: List[SalesPlanResponse]
