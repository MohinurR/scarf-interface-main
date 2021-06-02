from app import db


class Scarf(db.Model):
    """"""
    __tablename__ = "scarves"

    id = db.Column(db.Integer, primary_key=True)
    material = db.Column(db.String)
    price = db.Column(db.Integer)
    manufacturer = db.Column(db.String)
    colour = db.Column(db.String)
    width = db.Column(db.Integer)
    length = db.Column(db.Integer)
    size = db.Column(db.Integer)

    def __init__(self, material, price, manufacturer, colour, width, length):
        """"""
        self.material = material
        self.price = price
        self.manufacturer = manufacturer
        self.colour = colour
        self.width = width
        self.length = length
        self.size = int(length / width)
