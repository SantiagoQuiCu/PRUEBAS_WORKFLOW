from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from vistas import (
    VistaMarcas,
    VistaMarca,
    VistaVehiculos,
    VistaVehiculo,
    VistaReporteMarcas,
)
from modelos.modelos import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///concesionario.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
app_context= app.app_context()
app_context.push()
db.init_app(app)
db.create_all()
CORS(app)


api = Api(app)
api.add_resource(VistaMarcas, "/marcas")
api.add_resource(VistaMarca, "/marcas/<int:id_marca>")
api.add_resource(VistaVehiculos, "/vehiculos")
api.add_resource(VistaVehiculo, "/vehiculos/<int:id_vehiculo>")
api.add_resource(VistaReporteMarcas, "/reporte-marcas")

if __name__ == "__main__":
    app.run(debug=True, port=5001)
