from app.commands.base_command import BaseCommand
from app.models.sales_plan_seller import SalesPlanSeller
from app.lib.database import db
from app.lib.errors import NotFoundError
from app.commands.sales_plan.get import GetSalesPlanCommand


class GetSalesPlanSellerCommand(BaseCommand):
    def __init__(self, seller_id, plan_id=None):
        self.seller_id = seller_id
        self.plan_id = plan_id

    def execute(self):
        seller = db.session.get(SalesPlanSeller, self.seller_id)

        if not seller:
            raise NotFoundError(f"Seller with ID {self.seller_id} not found")

        # If plan_id is provided, verify the seller belongs to this plan
        if self.plan_id is not None and seller.sales_plan_id != self.plan_id:
            raise NotFoundError(f"Seller with ID {self.seller_id} not found")

        return seller


class GetPlanSellersCommand(BaseCommand):
    def __init__(self, plan_id):
        self.plan_id = plan_id

    def execute(self):
        # First verify that the plan exists using the existing command
        GetSalesPlanCommand(self.plan_id).execute()

        # Get sellers for the specified plan
        sellers = db.session.execute(
            db.select(SalesPlanSeller)
            .where(SalesPlanSeller.sales_plan_id == self.plan_id)
            .order_by(SalesPlanSeller.id)
        ).scalars().all()

        return sellers


class GetAllSalesPlanSellersCommand(BaseCommand):
    def execute(self):
        sellers = db.session.execute(
            db.select(SalesPlanSeller).order_by(SalesPlanSeller.id)
        ).scalars().all()

        return sellers
