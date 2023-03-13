from flask_restful import Resource 
from flask import jsonify, request
from main.models import UsuarioModel
from .. import db
from main.auth.decorators import role_required
from flask_jwt_extended import get_jwt_identity
from main.mail.functions import send_mail

clientes = [
    {
        "id":1,
        "nombre": "Angel",
        "apellido": "Meza"
    },
    {
        "id":2,
        "nombre": "Isaac",
        "apellido": "Ix"
    }
]

class Cliente(Resource):
    @role_required(roles=["admin", "cliente"])
    def get(self, id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        current_user = get_jwt_identity()
        if cliente.role == 'cliente' or cliente.role == 'admin': 
          if current_user['usuarioId'] == cliente.id or current_user['role'] == 'admin':
            return cliente.to_json()
          else:
            return 'Sin acceso', 401
        else: 
            return 'H', 404

    @role_required(roles=["cliente"])
    def put(self,id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        current_user = get_jwt_identity()
        usuario = UsuarioModel
        if cliente.role == 'cliente' and current_user['usuarioId'] == cliente.id:
            data = request.get_json().items()
            for key, value in data:
                setattr(cliente, key, value)
            try: 
                send_mail([usuario.email], "Bienvenido", 'register', usuario = usuario)
                db.session.add(cliente)
                db.session.commit()
                return cliente.to_json(), 201
            except:
                return 404
        else:
            return 'Solo te pedes editar a ti mismo', 404

    @role_required(roles=["cliente"])
    def delete(self,id):
        cliente = db.session.query(UsuarioModel).get_or_404(id)
        current_user = get_jwt_identity()
        if cliente.role == 'cliente' and current_user['usuarioId'] == cliente.id:
            try: 
                db.session.delete(cliente)
                db.session.commit()
            except:
                return 404
        else:
            return 'Solo puedes eliminarte a ti mismo', 404
            
        

class Clientes(Resource):
    @role_required(roles=['admin'])
    def get(self):
        pagina = 1
        paginado = 2
        clientes = db.session.query(UsuarioModel).filter(UsuarioModel.role == 'cliente')

        if request.get_json(silent=True):   #silent =True   para ignorar el hecho de que no recibimos un json
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    pagina = int(value)
                elif key == 'per_page':
                    paginado = int(value)

        clientes = clientes.paginate(page = pagina, per_page = paginado, error_out = True, max_per_page=15)

        return jsonify(
            {"cliente": [cliente.to_json() for cliente in clientes.items],
            "total": clientes.total,
            "pages": clientes.pages,
            "page": pagina}
        )

    def post(self):
        cliente = UsuarioModel.from_json(request.get_json())
        cliente.role = 'cliente'
        db.session.add(cliente)
        db.session.commit()
        return cliente.to_json(), 201
    