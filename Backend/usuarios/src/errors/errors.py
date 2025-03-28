class ApiError(Exception):
    code = 422
    description = "Mensaj́e por defecto"

class InvalidUsuarioData(ApiError):
    code = 400
    description = "Datos invalidos para el usuario"
    
class Unauthorized(ApiError):
    code = 401
    description = "No autorizado"
    
class Forbidden(ApiError):
    code = 403
    description = "No autorizado"
    
class UsuarioAlreadyExists(ApiError):
    code = 412
    description = "El usuario ya existe"

class UsuarioNotFound(ApiError):
    code = 404
    description = "El usuario no existe"