import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, request, current_app
from database import db  
from models import Producto, InventarioBodega
from seed_data import seed_productos_inventario

# Se cargan las variables de entorno
load_dotenv()
app = Flask(__name__)
IAM_SERVICE_URL = os.getenv("IAM_SERVICE_URL", "http://IAMService:5002")
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
host = os.getenv("FLASK_RUN_HOST", "0.0.0.0")
port = int(os.getenv("FLASK_RUN_PORT", 5001))
db.init_app(app)
        
'''Método para verificar el estado del servicio'''
@app.route('/health', methods=['GET'])
def health():
    return {'status': 'ok gestionInventarioService'}

'''Método para consultar inventario de productos de la base de datos'''
@app.route("/consulta-productos", methods=["GET"])
def consulta_inventario_productos():
    identidad_valida, msj, statuscode = verificar_identidad()

    if identidad_valida:
        try:
            # Consultar todos los productos con su inventario
            inventario = db.session.query(InventarioBodega, Producto).join(Producto).all()

            
            res = [
                {
                    "producto_id": producto.id,
                    "sku": producto.sku,
                    "nombre": producto.nombre,
                    "descripcion_producto": producto.descripcion,
                    "inventario": inventario.cantidad,
                    "ubicacion_inventario": inventario.ubicacion  
                }
                for inventario, producto in inventario
            ]

            return jsonify(res), 200

        except Exception as e:
            return jsonify({"error": f"Error al consultar inventario: {str(e)}"}), 500
    
    else:
        return msj, statuscode
    


'''Método para inicializar la bdd y cargar datos de prueba'''
@app.route("/init_seeder", methods=["POST"])
def seeder():
    with app.app_context():  
        db.create_all()  
        print("Tablas creadas en la BD.")
        seed_productos_inventario(10)  
        return jsonify({"message": "Productos e inventarios insertados correctamente."})
        
'''Método para limpiar la base de datos y volver a crear las tablas'''
@app.route("/reset_db", methods=["POST"])
def reset_db():
    with current_app.app_context():
        try:
            db.drop_all()  # Eliminar todas las tablas
            db.create_all()  # Volver a crear las tablas
            db.session.commit()
            return jsonify({"message": "Base de datos reiniciada correctamente"}), 200
        
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Error al reiniciar la base de datos: {str(e)}"}), 500       
        
'''Método para hacer un llamado al servicio IAM para verificar y validar los Tokens de acceso'''
def verificar_identidad():
    authorization_token = request.headers.get('Authorization')
    url = IAM_SERVICE_URL + "/check_token"
    headers = {
        "Authorization": f"{authorization_token}"
    }
    print("Auth token: ",str(authorization_token), flush=True)
    #return True, True
    try:
        response = requests.post(url, headers=headers)
        print("status code: ",str(response.status_code), flush=True)
        
        if response.status_code == 200:
            res = response.json()
            rol = res.get("rol")
            print("response: ",res, flush=True)
            print("ROLLLLL: ",rol, flush=True)
            if rol == "gestor_inventario":
                return True, None, 200
            else:
                return False, jsonify({"mensaje": "El usuario no cuenta con el nivel de acceso requerido"}), 401

        else:
            return False, jsonify(response.json()), response.status_code

    except requests.exceptions.RequestException as e:
        print("Error IAMService: ",str(e), flush=True)
        return False, jsonify({"error": f"Error de conexión con IAMService: {str(e)}"}), 500
    


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Tablas creadas")        
    app.run(host=host, port=port, debug=True)