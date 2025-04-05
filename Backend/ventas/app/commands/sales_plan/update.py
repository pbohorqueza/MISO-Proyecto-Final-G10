from app.commands.base_command import BaseCommand
from app.models.sales_plan import SalesPlan
from app.models.sales_plan_seller import SalesPlanSeller
from app.lib.database import db
from app.lib.errors import NotFoundError, BadRequestError
from app.lib.validators import validate_date_range


class UpdateSalesPlanCommand(BaseCommand):
    def __init__(self, sales_plan_id, data):
        self.sales_plan_id = sales_plan_id
        self.data = data

    def execute(self):
        sales_plan = db.session.get(SalesPlan, self.sales_plan_id)

        if not sales_plan:
            raise NotFoundError(f"Sales plan with ID {self.sales_plan_id} not found")

        if 'nombre' in self.data:
            sales_plan.nombre = self.data['nombre']

        if 'descripcion' in self.data:
            sales_plan.descripcion = self.data['descripcion']

        if 'valor_objetivo' in self.data:
            sales_plan.valor_objetivo = float(self.data['valor_objetivo'])

        if 'fecha_inicio' in self.data:
            sales_plan.fecha_inicio = self.data['fecha_inicio']

        if 'fecha_fin' in self.data:
            sales_plan.fecha_fin = self.data['fecha_fin']
        
        try:
            validate_date_range(sales_plan.fecha_inicio, sales_plan.fecha_fin)
        except ValueError as e:
            raise BadRequestError(str(e))

        if 'seller_ids' in self.data:
            seller_ids = self.data['seller_ids']
            sales_plan.sellers = []

            for seller_id in seller_ids:
                seller = db.session.execute(
                    db.select(SalesPlanSeller).where(SalesPlanSeller.seller_id == seller_id)
                ).scalar_one_or_none()

                if not seller:
                    seller = SalesPlanSeller(
                        nombre=f"Seller {seller_id}",
                        seller_id=seller_id
                    )
                    db.session.add(seller)

                sales_plan.sellers.append(seller)

        db.session.commit()

        return sales_plan
