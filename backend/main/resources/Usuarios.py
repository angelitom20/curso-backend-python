from flask_restful import Resource
from flask import request, jsonify
from .. import db
from main.models import UsuarioModel
from main.mail.functions import send_mail

class Usuario(Resource):
    
    def get(self, id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        try: 
            return usuario.to_json()
        except: 
            return "Recurso no encontrado error 404"

    def put(self,id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        data = request.get_json().items()
        for key, value in data:
            setattr(usuario, key, value)
        try: 
            usuario = UsuarioModel
            send_mail([usuario.email], "Bienvenido", 'register', usuario = usuario)
            db.session.add(usuario)
            db.session.commit()
            return usuario.to_json(), 201
        except:
            return 404

    def delete(self,id):
        usuario = db.session.query(UsuarioModel).get_or_404(id)
        try: 
            db.session.delete(usuario)
            db.session.commit()
        except:
            return '',404

class Usuarios(Resource):
     
    def get(self):
        pagina = 1
        paginado = 2
        usuarios = db.session.query(UsuarioModel)

        if request.get_json(silent=True):   #silent =True   para ignorar el hecho de que no recibimos un json
            filters = request.get_json().items()
            for key, value in filters:
                if key == 'page':
                    pagina = int(value)
                elif key == 'per_page':
                    paginado = int(value)

        usuarios = usuarios.paginate(page = pagina, per_page = paginado, error_out = True, max_per_page=15)

        return jsonify({
            "Usuarios": [usuario.to_json() for usuario in usuarios.items],
            "total": usuarios.total,
            "pages": usuarios.pages,
            "page": pagina
        })