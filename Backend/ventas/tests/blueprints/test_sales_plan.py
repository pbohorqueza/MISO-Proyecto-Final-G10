import json
from datetime import date, timedelta
import pytest

from app.models.sales_plan import SalesPlan
from app.models.sales_plan_seller import SalesPlanSeller
from app.lib.database import db


class TestSalesPlan:
    def test_create_sales_plan(self, auth_client, db_session):
        # Create a test seller
        seller = SalesPlanSeller(
            nombre="Test Seller",
            seller_id=1
        )
        db_session.add(seller)
        db_session.commit()

        # With our mocked authentication in conftest.py, we don't need to get a real token
        # We'll add a dummy header that will be ignored
        auth_header = 'Bearer test_token'

        # Define test sales plan data
        today = date.today()
        end_date = today + timedelta(days=30)

        data = {
            "nombre": "Test Sales Plan",
            "descripcion": "A test sales plan",
            "valor_objetivo": 1000.0,
            "fecha_inicio": today.strftime('%Y-%m-%d'),
            "fecha_fin": end_date.strftime('%Y-%m-%d'),
            "seller_ids": [1]
        }

        # Create a sales plan
        response = auth_client.post(
            '/planes',
            json=data,
            headers={'Authorization': auth_header}
        )

        assert response.status_code == 201

        # Check that the plan was created in the database using SQLAlchemy 2.0 style
        sales_plan = db_session.execute(
            db.select(SalesPlan).where(SalesPlan.nombre == "Test Sales Plan")
        ).scalar_one_or_none()
        assert sales_plan is not None
        assert sales_plan.descripcion == "A test sales plan"
        assert sales_plan.valor_objetivo == 1000.0
        assert len(sales_plan.sellers) == 1
        assert sales_plan.sellers[0].seller_id == 1

    def test_get_sales_plans(self, auth_client, db_session):
        # Create a test seller
        seller = SalesPlanSeller(
            nombre="Test Seller",
            seller_id=1
        )
        db_session.add(seller)

        # Create a test sales plan
        today = date.today()
        end_date = today + timedelta(days=30)

        sales_plan = SalesPlan(
            nombre="Test Sales Plan",
            descripcion="A test sales plan",
            valor_objetivo=1000.0,
            fecha_inicio=today,
            fecha_fin=end_date
        )
        sales_plan.sellers.append(seller)

        db_session.add(sales_plan)
        db_session.commit()

        # With our mocked authentication in conftest.py, we don't need to get a real token
        auth_header = 'Bearer test_token'

        # Get all sales plans
        response = auth_client.get(
            '/planes',
            headers={'Authorization': auth_header}
        )

        assert response.status_code == 200
        assert len(response.json['items']) == 1
        assert response.json['items'][0]['nombre'] == "Test Sales Plan"

    def test_validation_invalid_date_http(self, auth_client, db_session):
        """
        Test validation of invalid dates through the HTTP endpoint.
        This tests that dates must be valid calendar dates.
        """
        # Create a test seller for the plan
        seller = SalesPlanSeller(
            nombre="Test Seller",
            seller_id=1
        )
        db_session.add(seller)
        db_session.commit()

        # Define test data with invalid calendar date
        data = {
            "nombre": "Invalid Calendar Date Plan",
            "descripcion": "A sales plan with invalid calendar date",
            "valor_objetivo": 1000.0,
            "fecha_inicio": "2023-02-30",  # February 30th doesn't exist
            "fecha_fin": "2023-03-15",
            "seller_ids": [1]
        }

        # Add authorization header for testing
        auth_header = 'Bearer test_token'

        # Make a request to create a sales plan with invalid calendar date
        response = auth_client.post(
            '/planes',
            json=data,
            headers={'Authorization': auth_header}
        )

        # Verify the response
        assert response.status_code == 422

        response_text = response.get_data(as_text=True)

        # Verify that the validation error is present in the response
        assert "Invalid date" in response_text

    def test_validation_date_format_http(self, auth_client, db_session):
        """
        Test validation of date format through the HTTP endpoint.
        This tests that dates must be in YYYY-MM-DD format.
        """
        # Create a test seller for the plan
        seller = SalesPlanSeller(
            nombre="Test Seller",
            seller_id=1
        )
        db_session.add(seller)
        db_session.commit()

        # Define test data with invalid date format
        data = {
            "nombre": "Invalid Date Format Plan",
            "descripcion": "A sales plan with invalid date format",
            "valor_objetivo": 1000.0,
            "fecha_inicio": "01/15/2023",  # MM/DD/YYYY format instead of YYYY-MM-DD
            "fecha_fin": "2023-02-15",
            "seller_ids": [
                seller.id
            ]
        }

        # Add authorization header for testing
        auth_header = 'Bearer test_token'

        # Make a request to create a sales plan with invalid date format
        response = auth_client.post(
            '/planes',
            json=data,
            headers={'Authorization': auth_header}
        )

        # Verify the response
        assert response.status_code == 422

        response_text = response.get_data(as_text=True)

        # Verify that the validation error is present in the response
        assert "Date must be in the format YYYY-MM-DD" in response_text

    def test_validation_end_date_before_start_date_http(self, auth_client, db_session):
        """
        Test validation that end date must be after start date through the HTTP endpoint.
        This tests the API validation directly.
        """
        # Create a test seller for the plan
        seller = SalesPlanSeller(
            nombre="Test Seller",
            seller_id=1
        )
        db_session.add(seller)
        db_session.commit()

        # Define test data with end_date before start_date
        today = date.today()
        yesterday = today - timedelta(days=1)

        data = {
            "nombre": "Invalid Sales Plan",
            "descripcion": "A sales plan with invalid dates",
            "valor_objetivo": 1000.0,
            "fecha_inicio": today.strftime('%Y-%m-%d'),
            "fecha_fin": yesterday.strftime('%Y-%m-%d'),
            "seller_ids": [
                seller.id
            ]
        }

        # Add authorization header for testing
        auth_header = 'Bearer test_token'

        # Make a request to create a sales plan with invalid dates
        response = auth_client.post(
            '/planes',
            json=data,
            headers={'Authorization': auth_header}
        )

        # Verify the response
        # 422 is the standard response code for validation errors in OpenAPI/Pydantic
        assert response.status_code == 422

        response_text = response.get_data(as_text=True)

        # Verify that the validation error is present in the response
        assert "End date must be after start date" in response_text

    def test_get_sales_plan_by_id(self, auth_client, db_session):
        """Test getting a specific sales plan by ID"""
        # Create a test seller
        seller = SalesPlanSeller(
            nombre="Test Seller",
            seller_id=1
        )
        db_session.add(seller)

        # Create a test sales plan
        today = date.today()
        end_date = today + timedelta(days=30)

        sales_plan = SalesPlan(
            nombre="Test Sales Plan",
            descripcion="A test sales plan",
            valor_objetivo=1000.0,
            fecha_inicio=today,
            fecha_fin=end_date
        )
        sales_plan.sellers.append(seller)

        db_session.add(sales_plan)
        db_session.commit()

        # Get the newly created sales plan's ID
        sales_plan_id = sales_plan.id

        # With our mocked authentication in conftest.py
        auth_header = 'Bearer test_token'

        # Get the sales plan by ID
        response = auth_client.get(
            f'/planes/{sales_plan_id}',
            headers={'Authorization': auth_header}
        )

        assert response.status_code == 200
        assert response.json['nombre'] == "Test Sales Plan"
        assert response.json['descripcion'] == "A test sales plan"
        assert float(response.json['valor_objetivo']) == 1000.0
        assert len(response.json['sellers']) == 1

    def test_update_sales_plan(self, auth_client, db_session):
        """Test updating a sales plan"""
        # Create a test seller
        seller = SalesPlanSeller(
            nombre="Test Seller",
            seller_id=1
        )
        db_session.add(seller)

        # Create a test sales plan
        today = date.today()
        end_date = today + timedelta(days=30)

        sales_plan = SalesPlan(
            nombre="Original Name",
            descripcion="Original description",
            valor_objetivo=1000.0,
            fecha_inicio=today,
            fecha_fin=end_date
        )
        sales_plan.sellers.append(seller)

        db_session.add(sales_plan)
        db_session.commit()

        # Get the newly created sales plan's ID
        sales_plan_id = sales_plan.id

        # With our mocked authentication in conftest.py
        auth_header = 'Bearer test_token'

        # Update data
        update_data = {
            "nombre": "Updated Name",
            "descripcion": "Updated description",
            "valor_objetivo": 2000.0,
            "seller_ids": [
                seller.id
            ]
        }

        # Update the sales plan
        response = auth_client.put(
            f'/planes/{sales_plan_id}',
            json=update_data,
            headers={'Authorization': auth_header}
        )

        assert response.status_code == 200
        assert response.json['nombre'] == "Updated Name"
        assert response.json['descripcion'] == "Updated description"
        assert float(response.json['valor_objetivo']) == 2000.0

        # Verify the update in the database using session.get() as recommended in SQLAlchemy 2.0
        updated_plan = db_session.get(SalesPlan, sales_plan_id)
        assert updated_plan.nombre == "Updated Name"
        assert updated_plan.descripcion == "Updated description"
        assert updated_plan.valor_objetivo == 2000.0

    def test_delete_sales_plan(self, auth_client, db_session):
        """Test deleting a sales plan"""
        # Create a test seller
        seller = SalesPlanSeller(
            nombre="Test Seller",
            seller_id=1
        )
        db_session.add(seller)

        # Create a test sales plan
        today = date.today()
        end_date = today + timedelta(days=30)

        sales_plan = SalesPlan(
            nombre="To Delete",
            descripcion="A sales plan to delete",
            valor_objetivo=1000.0,
            fecha_inicio=today,
            fecha_fin=end_date
        )
        sales_plan.sellers.append(seller)

        db_session.add(sales_plan)
        db_session.commit()

        # Get the newly created sales plan's ID
        sales_plan_id = sales_plan.id

        # With our mocked authentication in conftest.py
        auth_header = 'Bearer test_token'

        # Delete the sales plan
        response = auth_client.delete(
            f'/planes/{sales_plan_id}',
            headers={'Authorization': auth_header}
        )

        assert response.status_code == 204

        # Verify the sales plan was deleted from the database using session.get() as recommended in SQLAlchemy 2.0
        deleted_plan = db_session.get(SalesPlan, sales_plan_id)
        assert deleted_plan is None
