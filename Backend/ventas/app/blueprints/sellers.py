from typing import Optional

from flask_openapi3 import Tag
from pydantic import BaseModel, Field

from app.commands.sales_plan_seller.create import CreateSalesPlanSellerCommand
from app.commands.sales_plan_seller.delete import DeleteSalesPlanSellerCommand
from app.commands.sales_plan_seller.get import GetSalesPlanSellerCommand, GetPlanSellersCommand
from app.commands.sales_plan_seller.update import UpdateSalesPlanSellerCommand
from app.lib.auth import validate_token, director_required
from app.responses import ErrorResponse
from app.responses.sales_plan import SalesPlanPath
from app.responses.seller import SellerResponse, SellerListResponse
from . import seller_blueprint

# Define API tag
sellers_tag = Tag(name="Vendedores", description="Operaciones sobre vendedores asignados a planes de venta")


# Pydantic models for request data
class SellerCreate(BaseModel):
    """Esquema para crear un nuevo Vendedor"""
    nombre: str = Field(..., min_length=2, max_length=255, description="Nombre del vendedor")
    seller_id: int = Field(..., gt=0, description="ID del vendedor del servicio de usuarios")


class SellerUpdate(BaseModel):
    """Esquema para actualizar un Vendedor existente"""
    nombre: Optional[str] = Field(None, min_length=2, max_length=255, description="Nombre del vendedor")


class PlanSellerPath(BaseModel):
    """Parámetros de ruta para las rutas de Vendedores"""
    plan_id: int = Field(..., description="ID del plan de ventas")
    seller_id: int = Field(..., description="ID del vendedor")


@seller_blueprint.get('', tags=[sellers_tag],
                      responses={200: SellerListResponse, 404: ErrorResponse})
@validate_token
def get_plan_sellers(path: SalesPlanPath):
    """Obtener todos los vendedores asignados a un plan de venta específico"""
    plan_id = path.plan_id
    # Get sellers for the specified plan using the optimized command
    plan_sellers = GetPlanSellersCommand(plan_id).execute()

    # Return as Pydantic models
    return SellerListResponse(
        items=[
            SellerResponse(
                id=seller.id,
                nombre=seller.nombre,
                seller_id=seller.seller_id
            ) for seller in plan_sellers
        ]
    ).model_dump()


@seller_blueprint.get('/<int:seller_id>', tags=[sellers_tag],
                      responses={200: SellerResponse, 404: ErrorResponse})
@validate_token
def get_plan_seller(path: PlanSellerPath):
    """Obtener un vendedor específico por ID dentro de un plan de venta"""
    # Execute the command to get the seller, passing plan_id for verification
    seller = GetSalesPlanSellerCommand(path.seller_id, plan_id=path.plan_id).execute()

    # Return as Pydantic model
    return SellerResponse(
        id=seller.id,
        nombre=seller.nombre,
        seller_id=seller.seller_id
    ).model_dump()


@seller_blueprint.post('', tags=[sellers_tag],
                       responses={201: SellerResponse, 400: ErrorResponse, 403: ErrorResponse, 404: ErrorResponse})
@validate_token
@director_required
def add_seller_to_plan(path: SalesPlanPath, body: SellerCreate):
    """Añadir un nuevo vendedor a un plan de venta - requiere rol de Director"""
    plan_id = path.plan_id

    # Prepare data with plan_id
    seller_data = body.model_dump()
    seller_data['sales_plan_id'] = plan_id

    # Execute the command to create a seller with validated data
    seller = CreateSalesPlanSellerCommand(seller_data).execute()

    # Return as Pydantic model
    response = SellerResponse(
        id=seller.id,
        nombre=seller.nombre,
        seller_id=seller.seller_id
    )

    return response.model_dump(), 201


@seller_blueprint.put('/<int:seller_id>', tags=[sellers_tag],
                      responses={200: SellerResponse, 400: ErrorResponse, 403: ErrorResponse, 404: ErrorResponse})
@validate_token
@director_required
def update_plan_seller(path: PlanSellerPath, body: SellerUpdate):
    """Actualizar un vendedor dentro de un plan de venta - requiere rol de Director"""
    seller_id = path.seller_id
    plan_id = path.plan_id

    # Verify the seller belongs to the plan
    GetSalesPlanSellerCommand(seller_id, plan_id=plan_id).execute()

    # Execute the command to update the seller with validated data
    updated_seller = UpdateSalesPlanSellerCommand(seller_id, body.model_dump(exclude_none=True)).execute()

    # Return as Pydantic model
    return SellerResponse(
        id=updated_seller.id,
        nombre=updated_seller.nombre,
        seller_id=updated_seller.seller_id
    ).model_dump()


@seller_blueprint.delete('/<int:seller_id>', tags=[sellers_tag],
                         responses={204: None, 403: ErrorResponse, 404: ErrorResponse})
@validate_token
@director_required
def remove_seller_from_plan(path: PlanSellerPath):
    """Eliminar un vendedor de un plan de venta - requiere rol de Director"""
    seller_id = path.seller_id
    plan_id = path.plan_id

    # Verify the seller belongs to the plan
    GetSalesPlanSellerCommand(seller_id, plan_id=plan_id).execute()

    # Execute the command to delete the seller
    DeleteSalesPlanSellerCommand(seller_id).execute()

    return '', 204
