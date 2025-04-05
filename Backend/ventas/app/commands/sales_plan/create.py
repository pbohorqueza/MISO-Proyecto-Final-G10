from app.commands.base_command import BaseCommand
from app.lib.database import db
from app.lib.errors import BadRequestError
from app.models.sales_plan import SalesPlan
from app.models.sales_plan_seller import SalesPlanSeller
from app.lib.validators import validate_date_range


class CreateSalesPlanCommand(BaseCommand):
    def __init__(self, data):
        self.data = data

    def execute(self):
        try:
            validate_date_range(self.data['fecha_inicio'], self.data['fecha_fin'])
        except ValueError as e:
            raise BadRequestError(str(e))

        sales_plan = SalesPlan(
            nombre=self.data['nombre'],
            descripcion=self.data['descripcion'],
            valor_objetivo=float(self.data['valor_objetivo']),
            fecha_inicio=self.data['fecha_inicio'],
            fecha_fin=self.data['fecha_fin']
        )

        seller_ids = self.data.get('seller_ids', [])

        for seller_id in seller_ids:
            seller = db.session.execute(
                db.select(SalesPlanSeller).where(SalesPlanSeller.seller_id == seller_id)
            ).scalar_one_or_none()

            if not seller:
                # In a real implementation, make an authenticated API call to users microservice
                seller = SalesPlanSeller(
                    nombre=f"Seller {seller_id}",  # This would come from the users microservice
                    seller_id=seller_id
                )
                db.session.add(seller)

            sales_plan.sellers.append(seller)

        db.session.add(sales_plan)
        db.session.commit()

        return sales_plan
