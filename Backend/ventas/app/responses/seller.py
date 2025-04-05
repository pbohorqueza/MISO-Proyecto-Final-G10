"""SalesPlanSeller response models."""
from typing import List
from pydantic import BaseModel, Field


class SellerPath(BaseModel):
    """Parámetros de ruta para las rutas de Vendedor"""
    seller_id: int = Field(..., description="ID del vendedor")


class SellerResponse(BaseModel):
    """Esquema para devolver un Vendedor"""
    id: int
    nombre: str
    seller_id: int


class SellerListResponse(BaseModel):
    """Esquema para devolver múltiples Vendedores"""
    items: List[SellerResponse]
