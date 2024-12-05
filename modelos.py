from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields
from werkzeug.security import generate_password_hash, check_password_hash
import enum

db = SQLAlchemy()


class RolUsuario(enum.Enum):
    CLIENTE = "cliente"
    ADMINISTRADOR = "administrador"
    PILOTO = "piloto"

# Tablas relacionales
detalle_pedido = db.Table('detalle_pedido',
    db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id'), primary_key=True),
    db.Column('producto_id', db.Integer, db.ForeignKey('producto.id'), primary_key=True)
)


# Modelos
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(50), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    direccion = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    contrasena_hash = db.Column(db.String(255), nullable=False)
    fecha_registro = db.Column(db.DateTime, nullable=False)
    rol_id = db.Column(db.Enum(RolUsuario), default=RolUsuario.CLIENTE, nullable=False)
    pagos = db.relationship('Pago', back_populates='usuario', cascade='all, delete-orphan')
    pedidos = db.relationship('Pedido', back_populates='usuario', cascade='all, delete-orphan')

    @property
    def contrasena(self):
        raise AttributeError("error.")

    @contrasena.setter
    def contrasena(self, password):
        self.contrasena_hash = generate_password_hash(password)

    def verificar_contrasena(self, password):
        return check_password_hash(self.contrasena_hash, password)

class Pago(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    monto_total = db.Column(db.Float, nullable=False)
    metodo_pago = db.Column(db.String(50), nullable=False)
    fecha_hora = db.Column(db.DateTime, nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', back_populates='pagos')

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fecha_pedido = db.Column(db.DateTime, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    detalles = db.Column(db.Text, nullable=False)
    direccion_entrega = db.Column(db.String(255), nullable=False)
    forma_pago = db.Column(db.String(50), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    usuario = db.relationship('Usuario', back_populates='pedidos')
    productos = db.relationship('Producto', secondary=detalle_pedido, back_populates='pedidos')

class SeguimientoPedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    estado_actual = db.Column(db.String(50), nullable=False)
    fecha_actualizacion = db.Column(db.DateTime, nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)

class Producto(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_producto = db.Column(db.String(100), nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    estado = db.Column(db.String(50), nullable=False)
    categoria_id = db.Column(db.Integer, db.ForeignKey('categoria.id'), nullable=False)
    categoria = db.relationship('Categoria', back_populates='productos')
    pedidos = db.relationship('Pedido', secondary=detalle_pedido, back_populates='productos')

class Categoria(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(100), unique=True, nullable=False)
    descripcion = db.Column(db.Text, nullable=True)
    productos = db.relationship('Producto', back_populates='categoria', cascade='all, delete-orphan')

class DetallePedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cantidad = db.Column(db.Integer, nullable=False)
    precio_unitario = db.Column(db.Float, nullable=False)
    pedido_id = db.Column(db.Integer, db.ForeignKey('pedido.id'), nullable=False)
    producto_id = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable=False)

# Serializadores
class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"llave": value.name, "valor": value.value}

class UsuarioSchema(SQLAlchemyAutoSchema):
    rol_id = EnumADiccionario(attribute="rol_id")
    class Meta:
        model = Usuario
        include_relationships = True
        load_instance = True
        exclude = ("contrasena_hash",)

class PagoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pago
        include_relationships = True
        load_instance = True

class PedidoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Pedido
        include_relationships = True
        load_instance = True

class SeguimientoPedidoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = SeguimientoPedido
        include_relationships = True
        load_instance = True

class ProductoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Producto
        include_relationships = True
        load_instance = True

class CategoriaSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Categoria
        include_relationships = True
        load_instance = True

class DetallePedidoSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = DetallePedido
        include_relationships = True
        load_instance = True
