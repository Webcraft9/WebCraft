from flask import request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import (
    jwt_required, create_access_token, get_jwt_identity
)
from modelos.modelos import db, Usuario, Pedido, Pago, Producto, Categoria, SeguimientoPedido, DetallePedido, UsuarioSchema, PagoSchema, PedidoSchema, ProductoSchema, CategoriaSchema, DetallePedidoSchema, SeguimientoPedidoSchema

# Esquemas
usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)
pago_schema = PagoSchema()
pagos_schema = PagoSchema(many=True)
pedido_schema = PedidoSchema()
pedidos_schema = PedidoSchema(many=True)
producto_schema = ProductoSchema()
productos_schema = ProductoSchema(many=True)
categoria_schema = CategoriaSchema()
categorias_schema = CategoriaSchema(many=True)
detalle_schema = DetallePedidoSchema(many=True)
detalles_schema = DetallePedidoSchema(many=True)
seguimiento_schema = SeguimientoPedidoSchema(many=True)
seguimientos_schema = SeguimientoPedidoSchema(many=True)

# Vistas para autenticación
class VistaSignIn(Resource):
    def post(self):
        nombre_usuario = request.json.get("nombre")
        email_usuario = request.json.get("email")
        contrasena_usuario = request.json.get("contrasena")

        # Verificar si el nombre de usuario o correo ya existen
        if Usuario.query.filter_by(nombre=nombre_usuario).first():
            return {"mensaje": "El nombre de usuario ya está registrado"}, 409
        if Usuario.query.filter_by(email=email_usuario).first():
            return {"mensaje": "El correo electrónico ya está registrado"}, 409

        # Crear el nuevo usuario
        nuevo_usuario = Usuario(nombre=nombre_usuario, email=email_usuario)
        nuevo_usuario.contrasena = contrasena_usuario
        db.session.add(nuevo_usuario)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Error al crear el usuario. Intenta nuevamente."}, 500

        return {"mensaje": "Usuario creado exitosamente"}, 201


class VistaLogIn(Resource):
    def post(self):
        nombre = request.json.get("nombre")
        contrasena = request.json.get("contrasena")

        # Buscar el usuario por nombre
        usuario = Usuario.query.filter_by(nombre=nombre).first()

        # Verificar credenciales
        if usuario and usuario.verificar_contrasena(contrasena):
            token_de_acceso = create_access_token(identity=usuario.id)
            return {"mensaje": "Inicio de sesión exitoso", "token": token_de_acceso}, 200

        return {"mensaje": "Usuario o contraseña incorrectos"}, 401


class VistaProtegida(Resource):
    @jwt_required()
    def get(self):
        usuario_actual = get_jwt_identity()
        return {"mensaje": f"Bienvenido {usuario_actual}"}, 200


# Vistas para gestión de usuarios
class VistaUsuarios(Resource):
    @jwt_required()
    def get(self):
        return usuarios_schema.dump(Usuario.query.all()), 200

    @jwt_required()
    def post(self):
        nuevo_usuario = Usuario(
            nombre=request.json['nombre'],
            apellido=request.json['apellido'],
            email=request.json['email'],
            contrasena=request.json['contrasena'],
            fecha_registro=request.json['fecha_registro'],
            direccion=request.json.get('direccion'),
            telefono=request.json.get('telefono'),
            nombre_rol=request.json['nombre_rol']
        )
        db.session.add(nuevo_usuario)
        try:
            db.session.commit()
            return usuario_schema.dump(nuevo_usuario), 201
        except IntegrityError:
            db.session.rollback()
            return {"mensaje": "Error al crear el usuario"}, 409


class VistaUsuario(Resource):
    @jwt_required()
    def get(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        return usuario_schema.dump(usuario), 200

    @jwt_required()
    def put(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        usuario.nombre = request.json.get('nombre', usuario.nombre)
        usuario.apellido = request.json.get('apellido', usuario.apellido)
        usuario.email = request.json.get('email', usuario.email)
        usuario.contrasena = request.json.get('contrasena', usuario.contrasena)
        usuario.direccion = request.json.get('direccion', usuario.direccion)
        usuario.telefono = request.json.get('telefono', usuario.telefono)
        usuario.nombre_rol = request.json.get('nombre_rol', usuario.nombre_rol)
        db.session.commit()
        return usuario_schema.dump(usuario), 200

    @jwt_required()
    def delete(self, id_usuario):
        usuario = Usuario.query.get_or_404(id_usuario)
        db.session.delete(usuario)
        db.session.commit()
        return '', 204


# Vistas para gestión de productos
class VistaProductos(Resource):
    @jwt_required()
    def get(self):
        return productos_schema.dump(Producto.query.all()), 200

    @jwt_required()
    def post(self):
        nuevo_producto = Producto(
            nombre_producto=request.json['nombre_producto'],
            descripcion=request.json.get('descripcion'),
            precio=request.json['precio'],
            estado=request.json['estado'],
            categoria_id=request.json['categoria_id']
        )
        db.session.add(nuevo_producto)
        db.session.commit()
        return producto_schema.dump(nuevo_producto), 201


class VistaProducto(Resource):
    @jwt_required()
    def get(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        return producto_schema.dump(producto), 200

    @jwt_required()
    def put(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        producto.nombre_producto = request.json.get('nombre_producto', producto.nombre_producto)
        producto.descripcion = request.json.get('descripcion', producto.descripcion)
        producto.precio = request.json.get('precio', producto.precio)
        producto.estado = request.json.get('estado', producto.estado)
        producto.categoria_id = request.json.get('categoria_id', producto.categoria_id)
        db.session.commit()
        return producto_schema.dump(producto), 200

    @jwt_required()
    def delete(self, id_producto):
        producto = Producto.query.get_or_404(id_producto)
        db.session.delete(producto)
        db.session.commit()
        return '', 204


# Vistas para gestión de pedidos
class VistaPedidos(Resource):
    @jwt_required()
    def get(self):
        return pedidos_schema.dump(Pedido.query.all()), 200

    @jwt_required()
    def post(self):
        nuevo_pedido = Pedido(
            fecha_pedido=request.json['fecha_pedido'],
            estado=request.json['estado'],
            usuario_id=request.json['usuario_id'],
            direccion_entrega=request.json['direccion_entrega']
        )
        db.session.add(nuevo_pedido)
        db.session.commit()
        return pedido_schema.dump(nuevo_pedido), 201


class VistaPedido(Resource):
    @jwt_required()
    def get(self, id_pedido):
        pedido = Pedido.query.get_or_404(id_pedido)
        return pedido_schema.dump(pedido), 200

    @jwt_required()
    def put(self, id_pedido):
        pedido = Pedido.query.get_or_404(id_pedido)
        pedido.estado = request.json.get('estado', pedido.estado)
        pedido.direccion_entrega = request.json.get('direccion_entrega', pedido.direccion_entrega)
        db.session.commit()
        return pedido_schema.dump(pedido), 200

    @jwt_required()
    def delete(self, id_pedido):
        pedido = Pedido.query.get_or_404(id_pedido)
        db.session.delete(pedido)
        db.session.commit()
        return '', 204


# Vistas para gestión de categorías
class VistaCategorias(Resource):
    def get(self):
        return categorias_schema.dump(Categoria.query.all()), 200

    def post(self):
        nueva_categoria = Categoria(
            nombre_categoria=request.json['nombre_categoria'],
            descripcion=request.json.get('descripcion')
        )
        db.session.add(nueva_categoria)
        db.session.commit()
        return categoria_schema.dump(nueva_categoria), 201


class VistaCategoria(Resource):
    def get(self, id_categoria):
        categoria = Categoria.query.get_or_404(id_categoria)
        return categoria_schema.dump(categoria), 200

    def put(self, id_categoria):
        categoria = Categoria.query.get_or_404(id_categoria)
        categoria.nombre_categoria = request.json.get('nombre_categoria', categoria.nombre_categoria)
        categoria.descripcion = request.json.get('descripcion', categoria.descripcion)
        db.session.commit()
        return categoria_schema.dump(categoria), 200

    def delete(self, id_categoria):
        categoria = Categoria.query.get_or_404(id_categoria)
        db.session.delete(categoria)
        db.session.commit()
        return '', 204


# Vistas para gestión de pagos
class VistaPagos(Resource):
    @jwt_required()
    def get(self):
        return pagos_schema.dump(Pago.query.all()), 200

    @jwt_required()
    def post(self):
        nuevo_pago = Pago(
            monto_total=request.json['monto_total'],
            metodo_pago=request.json['metodo_pago'],
            estado_pago=request.json['estado_pago'],
            pedido_id=request.json['pedido_id']
        )
        db.session.add(nuevo_pago)
        db.session.commit()
        return pago_schema.dump(nuevo_pago), 201


class VistaPago(Resource):
    @jwt_required()
    def get(self, id_pago):
        pago = Pago.query.get_or_404(id_pago)
        return pago_schema.dump(pago), 200

    @jwt_required()
    def put(self, id_pago):
        pago = Pago.query.get_or_404(id_pago)
        pago.monto_total = request.json.get('monto_total', pago.monto_total)
        pago.metodo_pago = request.json.get('metodo_pago', pago.metodo_pago)
        pago.estado_pago = request.json.get('estado_pago', pago.estado_pago)
        db.session.commit()
        return pago_schema.dump(pago), 200

    @jwt_required()
    def delete(self, id_pago):
        pago = Pago.query.get_or_404(id_pago)
        db.session.delete(pago)
        db.session.commit()
        return '', 204
    
class VistaDetallesDePedidos(Resource):
    @jwt_required()
    def get(self):
        return detalles_schema.dump(DetallePedido.query.all()), 200

    @jwt_required()
    def post(self):
        nuevo_detallepedido = DetallePedido(
            cantidad=request.json['monto_total'],
            precio_unitario=request.json['precio_unitario'],
            pedido_id=request.json['pedido_id']
        )
        db.session.add(nuevo_detallepedido)
        db.session.commit()
        return detalles_schema.dump(nuevo_detallepedido), 201
    
class VistaDetalleDePedido(Resource):
    @jwt_required()
    def get(self, id_detalle):
        detalle_pedido = DetallePedido.query.get_or_404(id_detalle)
        return detalle_schema.dump(detalle_pedido), 200

    @jwt_required()
    def put(self, id_detalle):
        detalle = DetallePedido.query.get_or_404(id_detalle)
        detalle.monto_total = request.json.get('monto_total', detalle.monto_total)
        detalle.precio_unitario = request.json.get('precio_unitario', detalle.precio_unitario)
        db.session.commit()
        return detalle_schema.dump(detalle), 200

    @jwt_required()
    def delete(self, id_detalle):
        detalle = DetallePedido.query.get_or_404(id_detalle)
        db.session.delete(detalle)
        db.session.commit()
        return '', 204
    
class VistaSeguimientoPedidos(Resource):
    @jwt_required()
    def get(self):
        return seguimiento_schema.dump(SeguimientoPedido.query.all()), 200
    
    @jwt_required()
    def post(self):
        nuevo_seguimientopedido = SeguimientoPedido(
            estado_actual=request.json['estado_actual'],
            fecha_actualizacion=request.json['fecha_actualizacion'],
            pedido_id=request.json['pedido_id']
        )
        db.session.add(nuevo_seguimientopedido)
        db.session.commit()
        return seguimiento_schema.dump(nuevo_seguimientopedido), 201
    
class VistaSeguimientoDePedido(Resource):
    @jwt_required()
    def get(self, id_seguimiento):
        seguimiento_pedido = SeguimientoPedido.query.get_or_404(id_seguimiento)
        return seguimiento_schema.dump(seguimiento_pedido), 200

    @jwt_required()
    def put(self, id_seguimiento):
        seguimiento = SeguimientoPedido.query.get_or_404(id_seguimiento)
        seguimiento.estado_actual = request.json.get('estado_actual', seguimiento.estado_actual)
        seguimiento.fecha_actualizacion = request.json.get('fecha_actualizacion', seguimiento.fecha_actualizacion)
        db.session.commit()
        return seguimiento_schema.dump(seguimiento), 200

    @jwt_required()
    def delete(self, id_seguimiento):
        seguimiento = SeguimientoPedido.query.get_or_404(id_seguimiento)
        db.session.delete(seguimiento)
        db.session.commit()
        return '', 204
