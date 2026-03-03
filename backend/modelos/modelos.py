from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

db = SQLAlchemy()

class Marca(db.Model):
  __tablename__ = "marca"
  id = db.Column(db.Integer, primary_key=True)
  nombre = db.Column(db.String(28), unique=True)
  pais = db.Column(db.String(28))
  fundacion = db.Column(db.Integer)
  vehiculos = db.relationship("Vehiculo",back_populates="marca")

class Vehiculo(db.Model):
  __tablename__ = "vehiculo"
  id = db.Column(db.Integer, primary_key= True)
  modelo = db.Column(db.String(28))
  anio = db.Column(db.Integer)
  precio = db.Column(db.Integer)
  color = db.Column(db.String(28))
  marca_id= db.Column(db.Integer, db.ForeignKey("marca.id"))
  marca = db.relationship("Marca",back_populates="vehiculos")
  __table_args__= (db.UniqueConstraint('marca_id','modelo',name='modelo_unico_marca'),)
  
class MarcaSchema(SQLAlchemyAutoSchema):
  class Meta:
    model = Marca
    load_instance = True
    include_relationships = True
    


class VehiculoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model= Vehiculo
        include_relationships = True
        include_fk = True
        load_instance = True