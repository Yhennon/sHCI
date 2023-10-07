from pydantic import BaseModel
from my_app.models import ShopName, PantType, ItemType
# Rework this to proper classess so it makes sense for the operations im doing


class ItemBase(BaseModel):
    name: str
    itemtype: ItemType
    price: float


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    distributor_id: int

    class Config:
        orm_mode = True

# A Base class for Distributors


class DistributorBase(BaseModel):
    title: ShopName
    address: str


class DistributorCreate(DistributorBase):
    address: str


# class DistributorAddress(BaseModel):
#     address: str


class Distributor(DistributorBase):
    id: int
    items: list[Item] = []

    class Config:
        orm_mode = True
