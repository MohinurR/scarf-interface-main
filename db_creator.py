from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///cloth-shop.db', echo=True)
Base = declarative_base()


class Scarf(Base):
    """"""
    __tablename__ = "scarves"

    id = Column(Integer, primary_key=True)
    material = Column(String)
    price = Column(Integer)
    manufacturer = Column(String)
    colour = Column(String)
    width = Column(Integer)
    length = Column(Integer)
    size = Column(Integer)

    def __init__(self, material, price, manufacturer, colour, width, length):
        """"""
        self.material = material
        self.price = price
        self.manufacturer = manufacturer
        self.colour = colour
        self.width = width
        self.length = length
        self.size = int(length/width)


# create tables
Base.metadata.create_all(engine)