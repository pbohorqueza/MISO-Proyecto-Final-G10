from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, model_validator, field_validator

from app.lib.validators import validate_date_string, validate_date_range
from flask_openapi3 import Tag

from app.commands.sales_plan.create import CreateSalesPlanCommand
from app.commands.sales_plan.delete import DeleteSalesPlanCommand
from app.commands.sales_plan.get import GetSalesPlanCommand, GetAllSalesPlansCommand
from app.commands.sales_plan.update import UpdateSalesPlanCommand
from app.lib.auth import validate_token, director_required
from . import plan_blueprint

from app.responses.sales_plan import SalesPlanResponse, SalesPlanListResponse, SalesPlanPath
from app.responses.seller import SellerResponse
from app.responses import ErrorResponse

sales_plan_tag = Tag(name="Planes de Venta", description="Operaciones sobre planes de venta")


# Pydantic models for request data
class SalesPlanCreate(BaseModel):
    """Esquema para crear un nuevo Plan de Ventas"""
    nombre: str = Field(..., min_length=3, max_length=255, description="Nombre del plan de ventas")
    descripcion: str = Field(..., min_length=3, max_length=500, description="Descripción del plan de ventas")
    valor_objetivo: float = Field(..., gt=0, description="Monto objetivo de ventas")
    fecha_inicio: str = Field(..., description="Fecha de inicio en formato YYYY-MM-DD")
    fecha_fin: str = Field(..., description="Fecha de fin en formato YYYY-MM-DD")
    seller_ids: List[int] = Field(..., description="Lista de IDs de vendedores asignados a este plan")

    @field_validator('fecha_inicio', 'fecha_fin', mode='after')
    @classmethod
    def validate_date(cls, value: str) -> str:
        """Validar que la cadena de fecha representa una fecha válida"""
        return validate_date_string(value)

    @model_validator(mode='after')
    def validate_dates(self):
        """Validar que fecha_fin es posterior a fecha_inicio"""
        if not hasattr(self, 'fecha_inicio') or not hasattr(self, 'fecha_fin'):
            return self

        validate_date_range(self.fecha_inicio, self.fecha_fin)
        return self

    @field_validator('seller_ids', mode='after')
    @classmethod
    def validate_seller_ids(cls, v: List[int]) -> List[int]:
        """Validar que seller_ids no está vacío"""
        if len(v) < 1:
            raise ValueError("Se debe proporcionar al menos un ID de vendedor")
        return v


class SalesPlanUpdate(BaseModel):
    """Esquema para actualizar un Plan de Ventas existente"""
    nombre: Optional[str] = Field(None, min_length=3, max_length=255, description="Nombre del plan de ventas")
    descripcion: Optional[str] = Field(None, min_length=3, max_length=500, description="Descripción del plan de ventas")
    valor_objetivo: Optional[float] = Field(None, gt=0, description="Monto objetivo de ventas")
    fecha_inicio: Optional[str] = Field(None, description="Fecha de inicio en formato YYYY-MM-DD")
    fecha_fin: Optional[str] = Field(None, description="Fecha de fin en formato YYYY-MM-DD")
    seller_ids: Optional[List[int]] = Field(None, description="Lista de IDs de vendedores asignados a este plan")

    @field_validator('fecha_inicio', 'fecha_fin', mode='after')
    @classmethod
    def validate_date(cls, value: Optional[str]) -> Optional[str]:
        """Validar que la cadena de fecha representa una fecha válida si se proporciona"""
        return validate_date_string(value)

    @model_validator(mode='after')
    def validate_dates(self):
        """Validar que fecha_fin es posterior a fecha_inicio si se proporcionan ambas"""
        if not hasattr(self, 'fecha_inicio') or not hasattr(self, 'fecha_fin'):
            return self

        validate_date_range(self.fecha_inicio, self.fecha_fin)
        return self

    @field_validator('seller_ids', mode='after')
    @classmethod
    def validate_seller_ids(cls, v: Optional[List[int]]) -> Optional[List[int]]:
        """Validar que seller_ids no está vacío si se proporciona"""
        if v is not None and len(v) < 1:
            raise ValueError("Se debe proporcionar al menos un ID de vendedor")
        return v


@plan_blueprint.get('', tags=[sales_plan_tag], responses={200: SalesPlanListResponse})
@validate_token
def get_sales_plans():
    """Obtener todos los planes de venta"""
    sales_plans = GetAllSalesPlansCommand().execute()

    return SalesPlanListResponse(
        items=[
            SalesPlanResponse(
                id=plan.id,
                nombre=plan.nombre,
                descripcion=plan.descripcion,
                valor_objetivo=plan.valor_objetivo,
                fecha_inicio=plan.fecha_inicio,
                fecha_fin=plan.fecha_fin,
                sellers=[
                    SellerResponse(
                        id=seller.id,
                        nombre=seller.nombre,
                        seller_id=seller.seller_id
                    ) for seller in plan.sellers
                ]
            ) for plan in sales_plans
        ]
    ).model_dump()


@plan_blueprint.get('/<plan_id>', tags=[sales_plan_tag], responses={200: SalesPlanResponse, 404: ErrorResponse})
@validate_token
def get_sales_plan(path: SalesPlanPath):
    """Obtener un plan de venta específico por ID"""
    sales_plan = GetSalesPlanCommand(path.plan_id).execute()

    return SalesPlanResponse(
        id=sales_plan.id,
        nombre=sales_plan.nombre,
        descripcion=sales_plan.descripcion,
        valor_objetivo=sales_plan.valor_objetivo,
        fecha_inicio=sales_plan.fecha_inicio,
        fecha_fin=sales_plan.fecha_fin,
        sellers=[
            SellerResponse(
                id=seller.id,
                nombre=seller.nombre,
                seller_id=seller.seller_id
            ) for seller in sales_plan.sellers
        ]
    ).model_dump()


@plan_blueprint.post('', tags=[sales_plan_tag],
                     responses={201: SalesPlanResponse, 400: ErrorResponse, 403: ErrorResponse})
@validate_token
@director_required
def create_sales_plan(body: SalesPlanCreate):
    """Crear un nuevo plan de venta - requiere rol de Director"""
    sales_plan = CreateSalesPlanCommand(body.model_dump()).execute()

    response = SalesPlanResponse(
        id=sales_plan.id,
        nombre=sales_plan.nombre,
        descripcion=sales_plan.descripcion,
        valor_objetivo=sales_plan.valor_objetivo,
        fecha_inicio=sales_plan.fecha_inicio,
        fecha_fin=sales_plan.fecha_fin,
        sellers=[
            SellerResponse(
                id=seller.id,
                nombre=seller.nombre,
                seller_id=seller.seller_id
            ) for seller in sales_plan.sellers
        ]
    )

    return response.model_dump(), 201


@plan_blueprint.put('/<plan_id>', tags=[sales_plan_tag],
                    responses={200: SalesPlanResponse, 400: ErrorResponse, 403: ErrorResponse, 404: ErrorResponse})
@validate_token
@director_required
def update_sales_plan(path: SalesPlanPath, body: SalesPlanUpdate):
    """Actualizar un plan de venta existente - requiere rol de Director"""
    id = path.plan_id
    sales_plan = UpdateSalesPlanCommand(id, body.model_dump(exclude_none=True)).execute()

    return SalesPlanResponse(
        id=sales_plan.id,
        nombre=sales_plan.nombre,
        descripcion=sales_plan.descripcion,
        valor_objetivo=sales_plan.valor_objetivo,
        fecha_inicio=sales_plan.fecha_inicio,
        fecha_fin=sales_plan.fecha_fin,
        sellers=[
            SellerResponse(
                id=seller.id,
                nombre=seller.nombre,
                seller_id=seller.seller_id
            ) for seller in sales_plan.sellers
        ]
    ).model_dump()


@plan_blueprint.delete('/<plan_id>', tags=[sales_plan_tag],
                       responses={204: None, 403: ErrorResponse, 404: ErrorResponse})
@validate_token
@director_required
def delete_sales_plan(path: SalesPlanPath):
    """Eliminar un plan de venta - requiere rol de Director"""
    id = path.plan_id
    DeleteSalesPlanCommand(id).execute()

    return '', 204
