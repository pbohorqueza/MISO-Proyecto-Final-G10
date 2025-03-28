class ApiError(Exception):
    code = 422
    description = "Mensaje genérico"

    def __init__(self, description=None, code=None):
        if description:
            self.description = description

        if code:
            self.code = code

    def to_dict(self):
        return {
            "status": self.code,
            "msg": self.description
        }

class Unauthorized(ApiError):
    code = 401
    description = "Acceso no autorizado"

class Forbidden(ApiError):
    code = 403
    description = "Acceso no autorizado"

class InvalidFabricanteData(ApiError):
    code = 400
    description = "Datos del fabricante no válidos"

class FabricanteNotFound(ApiError):
    code = 404
    description = "Fabricante no encontrado"
