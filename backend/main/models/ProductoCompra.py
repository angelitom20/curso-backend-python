from .. import db


class ProductoCompra(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    productoId = db.Column(db.Integer, db.ForeignKey('producto.id'), nullable = False)
    producto = db.relationship('Producto', back_populates = "productoscompras", uselist = False, single_parent=True)#db.relationship(Clase, atributo,....)
    compraId = db.Column(db.Integer, db.ForeignKey('compra.id'), nullable = False)
    compra = db.relationship('Compra', back_populates="productoscompras", uselist = False, single_parent = True)