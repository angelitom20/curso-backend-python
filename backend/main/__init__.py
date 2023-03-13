import os
from flask import Flask
from dotenv import load_dotenv

#importo el modulo para crear la api-rest
from flask_restful import Api
#importo el modulo para conectarme a base de datos
from flask_sqlalchemy import SQLAlchemy
#importo el modulo para trabajar con JWT - Jason Web Tokens
from flask_jwt_extended import JWTManager
#importo el modulo para trabajar con email
from flask_mail import Mail

api = Api()

db = SQLAlchemy()

jwt = JWTManager()

mailsender = Mail()

def create_app():

    app = Flask(__name__)
    #cargo las varibles de entorno
    load_dotenv()    

    #configuracion de la base de datos
    PATH = os.getenv("DATABASE_PATH")
    DB_NAME = os.getenv("DATABASE_NAME")

    if not os.path.exists(f'{PATH}{DB_NAME}'):#checa si no existe la base de datos
        os.chdir(f'{PATH}')#chdir cambiar de directorio
        file = os.open(f'{DB_NAME}', os.O_CREAT)#creamos la base de datos

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #verifica que no haya modificaciones 
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{PATH}{DB_NAME}'#nos conectamos a la base de datos
    db.init_app(app) #inicializamos la base de datos
    

    

    import main.resources as resources
    api.add_resource(resources.ClientesResource, '/clientes')
    api.add_resource(resources.ClienteResource, '/cliente/<id>')
    api.add_resource(resources.UsuariosResource, '/usuarios')
    api.add_resource(resources.UsuarioResource, '/usuario/<id>')
    api.add_resource(resources.ComprasResource, '/compras')
    api.add_resource(resources.CompraResource, '/compra/<id>')
    api.add_resource(resources.ProductosResource, '/productos')
    api.add_resource(resources.ProductoResource, '/producto/<id>')
    api.add_resource(resources.ProductosComprasResource, '/productos-compras')
    api.add_resource(resources.ProductoCompraResource, '/producto-compra/<id>')

    api.init_app(app)

    #Configurar JWT

    app.config['JWT_SECRET_KEY'] = os.getenv("JWT_SECRET_KEY")
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES"))
    jwt.init_app(app)

    from main.auth import routes
    app.register_blueprint(auth.routes.auth)
    from main.mail import functions
    app.register_blueprint(mail.functions.mail)

    #configurar mail
    #app.config['MAIL_HOSTNAME'] = os.getenv('MAIL_HOSTNAME')
    app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
    app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
    app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
    app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
    app.config['FLASKY_MAIL_SENDER'] = os.getenv('FLASKY_MAIL_SENDER')
 
    mailsender.init_app(app)
    return app

