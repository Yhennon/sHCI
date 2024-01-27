from enum import Enum
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from my_app.database import Base


class ShopName(str, Enum):
    rema = "Rema 1000"
    netto = "Netto"
    ikea = "IKEA"
    bilka = "Bilka"
    fotex = "føtex"

class PantType(str, Enum):
    pant_a = "Pant A"  # (less than 1L glass bottles and aluminium cans
    pant_b = "Pant B"  # (less than 1L plastic bottles)
    pant_c = "Pant C"  # (1-20L bottles and cans)


class ItemType(str, Enum):
    bakery_product = "Bakery product"
    dairy_product = "Dairy"
    spice = "Spice"
    fruit_and_vegetable = "Fruit and vegetable"
    meat = "Meat"


class Distributor(Base):
    __tablename__ = "distributors"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    address = Column(String, unique=True, index=True)

    items = relationship("Item", back_populates="distributor")


class Item(Base):
    __tablename__ = "itemsv3"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    itemtype = Column(String)
    price = Column(Float)
    # Foreign key points to an other table's column
    distributor_id = Column(Integer, ForeignKey("distributors.id"))

    distributor = relationship("Distributor", back_populates="items")
