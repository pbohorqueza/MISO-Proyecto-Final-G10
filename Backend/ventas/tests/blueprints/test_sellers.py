import json
import pytest
from datetime import date, timedelta
from unittest.mock import patch
import logging

from app.models.sales_plan import SalesPlan
from app.models.sales_plan_seller import SalesPlanSeller
from app.lib.database import db
from flask import g, request


class TestSellers:
    def test_add_seller_to_plan(self, auth_client, db_session):
        """Test adding a new seller to a sales plan"""
        # Create a test sales plan first
        today = date.today()
        end_date = today + timedelta(days=30)

        sales_plan = SalesPlan(
            nombre="Test Plan",
            descripcion="A test sales plan",
            valor_objetivo=1000.0,
            fecha_inicio=today,
            fecha_fin=end_date
        )
        db_session.add(sales_plan)
        db_session.commit()

        plan_id = sales_plan.id

        # With our mocked authentication in conftest.py, we don't need to get a real token
        auth_header = 'Bearer test_token'

        # Define test seller data
        data = {
            "nombre": "Test Seller",
            "seller_id": 100
        }

        # Add a seller to the plan
        response = auth_client.post(
            f'/planes/{plan_id}/vendedores',
            json=data,
            headers={'Authorization': auth_header}
        )

        assert response.status_code == 201

        # Check that the seller was created and associated with the plan
        seller = db_session.execute(
            db.select(SalesPlanSeller).where(SalesPlanSeller.seller_id == 100)
        ).scalar_one_or_none()
        assert seller is not None
        assert seller.nombre == "Test Seller"
        assert seller.sales_plan_id == plan_id

    def test_get_plan_sellers(self, auth_client, db_session):
        """Test getting all sellers for a specific plan"""
        # Create a test sales plan
        today = date.today()
        end_date = today + timedelta(days=30)

        sales_plan = SalesPlan(
            nombre="Test Plan",
            descripcion="A test sales plan",
            valor_objetivo=1000.0,
            fecha_inicio=today,
            fecha_fin=end_date
        )
        db_session.add(sales_plan)
        db_session.commit()

        plan_id = sales_plan.id

        # Create test sellers and associate them with the plan
        seller1 = SalesPlanSeller(
            nombre="Seller 1",
            seller_id=101,
            sales_plan_id=plan_id
        )
        seller2 = SalesPlanSeller(
            nombre="Seller 2",
            seller_id=102,
            sales_plan_id=plan_id
        )
        # Create a seller not in the plan
        seller3 = SalesPlanSeller(
            nombre="Seller 3",
            seller_id=103
        )

        db_session.add_all([seller1, seller2, seller3])
        db_session.commit()

        # With our mocked authentication in conftest.py, we don't need to get a real token
        auth_header = 'Bearer test_token'

        # Get all sellers for the plan
        response = auth_client.get(
            f'/planes/{plan_id}/vendedores',
            headers={'Authorization': auth_header}
        )

        assert response.status_code == 200
        assert len(response.json['items']) == 2

        # Check that only the sellers associated with the plan are returned
        seller_ids = [seller['seller_id'] for seller in response.json['items']]
        assert 101 in seller_ids
        assert 102 in seller_ids
        assert 103 not in seller_ids

    def test_get_plan_seller_by_id(self, auth_client, db_session):
        """Test getting a specific seller by ID within a plan"""
        # Create a test sales plan
        today = date.today()
        end_date = today + timedelta(days=30)

        sales_plan = SalesPlan(
            nombre="Test Plan",
            descripcion="A test sales plan",
            valor_objetivo=1000.0,
            fecha_inicio=today,
            fecha_fin=end_date
        )
        db_session.add(sales_plan)
        db_session.commit()

        plan_id = sales_plan.id

        # Create a test seller associated with the plan
        seller = SalesPlanSeller(
            nombre="Specific Seller",
            seller_id=200,
            sales_plan_id=plan_id
        )
        db_session.add(seller)
        db_session.commit()

        # Get the database ID
        seller_db_id = seller.id

        # With our mocked authentication in conftest.py, we don't need to get a real token
        auth_header = 'Bearer test_token'

        # Get the seller by ID within the plan
        response = auth_client.get(
            f'/planes/{plan_id}/vendedores/{seller_db_id}',
            headers={'Authorization': auth_header}
        )

        assert response.status_code == 200
        assert response.json['nombre'] == "Specific Seller"
        assert response.json['seller_id'] == 200

        # For a non-existent plan, we expect a 404
        # Try with a plan ID that's guaranteed not to exist
        wrong_plan_id = 999999

        # Using the same auth_client and auth_header as the successful request
        response = auth_client.get(
            f'/planes/{wrong_plan_id}/vendedores/{seller_db_id}',
            headers={'Authorization': auth_header}
        )

        # Since decorator was removed, should return 404
        assert response.status_code == 404

    def test_update_plan_seller(self, auth_client, db_session):
        """Test updating a seller within a plan"""
        # Create a test sales plan
        today = date.today()
        end_date = today + timedelta(days=30)

        sales_plan = SalesPlan(
            nombre="Test Plan",
            descripcion="A test sales plan",
            valor_objetivo=1000.0,
            fecha_inicio=today,
            fecha_fin=end_date
        )
        db_session.add(sales_plan)
        db_session.commit()

        plan_id = sales_plan.id

        # Create a test seller associated with the plan
        seller = SalesPlanSeller(
            nombre="Original Name",
            seller_id=300,
            sales_plan_id=plan_id
        )
        db_session.add(seller)
        db_session.commit()

        # Get the database ID
        seller_db_id = seller.id

        # With our mocked authentication in conftest.py, we don't need to get a real token
        auth_header = 'Bearer test_token'

        # Update the seller within the plan
        data = {
            "nombre": "Updated Name"
        }

        response = auth_client.put(
            f'/planes/{plan_id}/vendedores/{seller_db_id}',
            json=data,
            headers={'Authorization': auth_header}
        )

        assert response.status_code == 200

        # Check that the seller was updated in the database
        updated_seller = db_session.execute(
            db.select(SalesPlanSeller).where(SalesPlanSeller.id == seller_db_id)
        ).scalar_one_or_none()
        assert updated_seller.nombre == "Updated Name"

        # For a non-existent plan, we expect a 404
        # Try with a plan ID that's guaranteed not to exist
        wrong_plan_id = 999999

        # Using the same auth_client and auth_header as the successful request
        response = auth_client.put(
            f'/planes/{wrong_plan_id}/vendedores/{seller_db_id}',
            json=data,
            headers={'Authorization': auth_header}
        )

        # Since decorator was removed, should return 404
        assert response.status_code == 404

    def test_delete_plan_seller(self, auth_client, db_session):
        """Test removing a seller from a plan"""
        # Create a test sales plan
        today = date.today()
        end_date = today + timedelta(days=30)

        sales_plan = SalesPlan(
            nombre="Test Plan",
            descripcion="A test sales plan",
            valor_objetivo=1000.0,
            fecha_inicio=today,
            fecha_fin=end_date
        )
        db_session.add(sales_plan)
        db_session.commit()

        plan_id = sales_plan.id

        # Create a test seller associated with the plan
        seller = SalesPlanSeller(
            nombre="To Delete",
            seller_id=400,
            sales_plan_id=plan_id
        )
        db_session.add(seller)
        db_session.commit()

        # Get the database ID
        seller_db_id = seller.id

        # With our mocked authentication in conftest.py, we don't need to get a real token
        auth_header = 'Bearer test_token'

        # Delete the seller from the plan
        response = auth_client.delete(
            f'/planes/{plan_id}/vendedores/{seller_db_id}',
            headers={'Authorization': auth_header}
        )

        assert response.status_code == 204

        # Check that the seller was deleted from the database
        deleted_seller = db_session.execute(
            db.select(SalesPlanSeller).where(SalesPlanSeller.id == seller_db_id)
        ).scalar_one_or_none()
        assert deleted_seller is None

        # Try to delete a seller with a wrong plan ID
        # First recreate the seller
        new_seller = SalesPlanSeller(
            nombre="To Delete Again",
            seller_id=401,
            sales_plan_id=plan_id
        )
        db_session.add(new_seller)
        db_session.commit()

        seller_db_id = new_seller.id

        # For a non-existent plan, we expect a 404
        # Try with a plan ID that's guaranteed not to exist
        wrong_plan_id = plan_id + 1

        # Using the same auth_client and auth_header as the successful request
        r2 = auth_client.delete(
            f'/planes/{wrong_plan_id}/vendedores/{seller_db_id}',
            headers={'Authorization': auth_header}
        )

        # Since decorator was removed, should return 404
        assert r2.status_code == 404
