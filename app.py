from flaskr import create_app
from flaskr.modelos.modelos import Usuario, Producto, Categoria, Pedido, DetallePedido, Pago 
from .modelos import db
from flask_restful import Api
from .vistas import VistaUsuarios, VistaUsuario, VistaSignIn, VistaLogIn, VistaProtegida,VistaProductos, VistaProducto, VistaPedidos, VistaPedido, VistaPagos, VistaPago, VistaCategorias, VistaCategoria, VistaDetalleDePedido, VistaDetallesDePedidos, VistaSeguimientoPedidos, VistaSeguimientoDePedido
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

USER_DB = 'root'
PASS_DB = ''
URL_DB = 'localhost'
NAME_DB = 'qlocura'
FULL_URL_DB = f'mysql+pymysql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATONS'] = False

db =SQLAlchemy(app)


migrate = Migrate
migrate.init_app(app, db)

app = create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

CORS(app)

api = Api(app)
api.add_resource(VistaProducto, '/producto')
api.add_resource(VistaUsuarios, '/usuarios')
api.add_resource(VistaCategoria, '/categoria')
api.add_resource(VistaSignIn, '/signin')
api.add_resource(VistaLogIn, '/login')
api.add_resource(VistaUsuario, '/usuario')
api.add_resource(VistaProtegida, '/protegida')
api.add_resource(VistaProductos,'/productos')
api.add_resource(VistaPedidos,'/pedidos')
api.add_resource(VistaPedido,'/pedido')
api.add_resource(VistaPagos,'/pagos')
api.add_resource(VistaPago,'/pago')
api.add_resource(VistaCategorias,'/categorias')
api.add_resource(VistaCategoria,'/categoria')
api.add_resource(VistaDetallesDePedidos,'/detallepedidos')
api.add_resource(VistaDetalleDePedido, '/detallepedido')
api.add_resource(VistaSeguimientoPedidos, '/seguymientopedidos')
api.add_resource(VistaSeguimientoDePedido, '/segumientopedido')

jwt = JWTManager(app)

with app.app_context():
   u = Usuario(nombre='juan', contrasena='12345')
   p = Producto(nombre_producto='Salchipapa grande', precio_unitario=10.00, estado='disponible', categoria_id=1)
   c = Categoria(nombre_categoria='Salchipapas', descripcion='Salchipapas de distintos tamaños y precios')
   pe = Pedido(fecha_pedido='2023-08-30', estado='pendiente', detalles='Salchipapa grande', direccion_entrega='Calle 10', forma_pago='efectivo')
   d = DetallePedido(cantidad='1', precio_unitario=10.000)
   pa = Pago(monto_total='10.000', metodo_pago='efectivo', estado_pago='pendiente', pedido_id=1)
   
   p.categoria.append(c)
   pe.productos.append(p)
   pe.detalles.append(d)
   pa.pedido.append(pe)
   p.pedidos.append(pe)
   pe.pagos.append(pa)
  
   
   
   db.session.add(u)
   db.session.add(c)
   db.session.add(p)
   db.session.add(pe)
   db.session.add(d)
   db.session.add(pa)
   db.session.commit()
    



