from app.commands.base_command import BaseCommand
from app.models.sales_plan_seller import SalesPlanSeller
from app.lib.database import db
from app.lib.errors import ConflictError


class CreateSalesPlanSellerCommand(BaseCommand):
    def __init__(self, data):
        self.data = data

    def execute(self):
        existing_seller = db.session.execute(
            db.select(SalesPlanSeller).where(SalesPlanSeller.seller_id == self.data['seller_id'])
        ).scalar_one_or_none()

        if existing_seller:
            raise ConflictError(f"Seller with ID {self.data['seller_id']} already exists")

        seller = SalesPlanSeller(
            nombre=self.data['nombre'],
            seller_id=self.data['seller_id'],
            sales_plan_id=self.data.get('sales_plan_id')
        )

        db.session.add(seller)
        db.session.commit()

        return seller