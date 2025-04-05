from flask import jsonify, json, redirect
from flask_openapi3 import OpenAPI, Info
from flask_openapi3.models import Server
from marshmallow import ValidationError
from werkzeug.exceptions import HTTPException

from app.blueprints import api, plan_blueprint, seller_blueprint, command_bp
from app.blueprints.commands import commands
from app.config.application import ApplicationConfig
from app.lib.database import db, migrate
from app.lib.errors import ApiError
from app.lib.schema import marshmallow


def create_app():
    # Set up API info for OpenAPI documentation
    info = Info(
        title="Sales API",
        version="1.0.0",
        description=(
            "Sales microservice API for CCP Gestión.\n\n"
            "This API manages sales plans and sellers integration.\n\n"
            "Features:\n"
            "* Sales Plans management (CRUD operations)\n"
            "* Sellers management (CRUD operations)\n"
            "* JWT-based authentication"
        )
    )

    # Set up security schemes
    security_schemes = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter JWT token obtained from authentication"
        }
    }

    # Configure API servers
    servers = [
        Server(url="/", description="Local development server")
    ]

    # Initialize OpenAPI application with configuration
    app = OpenAPI(
        __name__,
        info=info,
        security_schemes=security_schemes,
        servers=servers,
        doc_prefix="/api",
        doc_ui=True,
        doc_url="/openapi.json"
    )

    # Load application configuration
    app.config.from_object(ApplicationConfig)

    """
    The following code snippet registers the error handlers for the application.
    """

    @app.errorhandler(ApiError)
    def handle_api_error(error):
        app.logger.error(f"{error}")
        return jsonify(error.to_dict()), error.status_code

    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        app.logger.error(f"Validation error: {error}")
        return jsonify({"error": error.messages}), 400

    @app.errorhandler(ValueError)
    def handle_value_error(error):
        app.logger.error(f"Value error: {error}")
        return jsonify({"error": str(error)}), 400

    @app.errorhandler(HTTPException)
    def handle_exception(e):
        app.logger.error(f"HTTP exception: {e}")
        response = e.get_response()
        response.data = json.dumps({
            "message": e.description,
        })
        response.content_type = "application/json"
        return response

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        app.logger.error(f"Unexpected error: {e}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

    """
    The following code snippet initializes the application with the necessary extensions.
    """
    db.init_app(app)
    migrate.init_app(app, db, command="mg")
    marshmallow.init_app(app)

    """
    The following code snippet registers the blueprints for the application.
    """

    # Register all the API blueprints
    app.register_api(api)  # Main API blueprint
    app.register_api(plan_blueprint)  # Sales plans blueprint
    app.register_api(seller_blueprint)  # Sellers blueprint

    app.register_blueprint(command_bp)  # Register regular blueprint for commands
    app.register_blueprint(commands)  # Register commands blueprint

    # Configure security schemes for OpenAPI
    app.security_schemes = {
        "bearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "Enter JWT token obtained from authentication"
        }
    }

    # Add a documentation index page
    @app.route('/docs')
    def api_docs():
        """Redirect to Swagger UI documentation"""
        return redirect('/api/swagger')

    """
    The following code snippet initializes the application context and imports the models.
    """
    with app.app_context():
        from app.models import sales_plan_seller, sales_plan

    return app
