from app.commands.base_command import BaseCommand
from app.models.sales_plan_seller import SalesPlanSeller
from app.lib.database import db
from app.lib.errors import NotFoundError


class UpdateSalesPlanSellerCommand(BaseCommand):
    def __init__(self, seller_id, data):
        self.seller_id = seller_id
        self.data = data

    def execute(self):
        seller = db.session.get(SalesPlanSeller, self.seller_id)

        if not seller:
            raise NotFoundError(f"Seller with ID {self.seller_id} not found")

        if 'nombre' in self.data:
            seller.nombre = self.data['nombre']

        db.session.commit()

        return seller