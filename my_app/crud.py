from sqlalchemy.orm import Session
from my_app import models, schemas
from enum import Enum
from sqlalchemy import asc, desc

def create_distributor(db: Session, distributor: schemas.DistributorCreate):
    db_distributor = models.Distributor(
        title=distributor.title, address=distributor.address)
    db.add(db_distributor)
    db.commit()
    db.refresh(db_distributor)
    return db_distributor

def get_distributor_by_id(db:Session, id: int):
    return db.query(models.Distributor).filter(models.Distributor.id==id).first()

def get_distributor_by_title(db: Session, title: str):
    return db.query(models.Distributor).filter(models.Distributor.title == title).first()


# Need a "get distributor" for checking if one already exists. Check for both title and address!! Only title is not enough
def get_distributor(db: Session, title: str, address: str):
    return db.query(models.Distributor).filter(models.Distributor.title == title).filter(models.Distributor.address == address).first()


def get_distributors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Distributor).offset(skip).limit(limit).all()
# TODO


def get_distributor_by_address(db: Session, address: str):
    return db.query(models.Distributor).filter(models.Distributor.address == address).first()


def create_distributor_item(db: Session, item: schemas.ItemCreate, distributor_id: int):
    # first distributor id is the items, the second is the parameter from input
    db_item = models.Item(**item.model_dump(), distributor_id=distributor_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_enum_values(enum_class: Enum):
    return [item.value for item in enum_class]

def get_all_items(db: Session, skip: int = 0, limit: int = 100, sort_by_price_asc: bool = False):
    if sort_by_price_asc:
        return db.query(models.Item).order_by(models.Item.price.asc()).offset(skip).limit(limit).all()
    else:
        return db.query(models.Item).order_by(models.Item.price.desc()).offset(skip).limit(limit).all()

def get_all_items_by_price(db: Session, sort_by_price_asc: bool = False):
    sort_by_price_asc: bool = False
    pass

def get_all_items_by_price():
    pass

def get_all_items_by_distributor():
    pass

def get_all_items_sorted(db: Session, sort: bool = False, price_sort: str = "", name_sort: str = "", item_type_sort: str = "", distributor_sort: str = ""):
    # Dictionary mapping parameter names to database attributes
    sort_attributes = {
        'price_sort': 'price',  
        'name_sort': 'name',
        'item_type_sort': 'item_type',
        'distributor_sort': 'distributor'
    }
    print(item_type_sort)
    query = db.query(models.Item) 

    itemTypes = [item.value for item in models.ItemType]
    # print(itemTypes)

    if sort:
        order_criteria = []
        for param, attribute in sort_attributes.items():
            sort_value = getattr(locals()[param], 'lower')() 
            if sort_value in ['asc', 'desc', itemTypes]:
                order_criteria.append(asc(attribute) if sort_value == 'asc' else desc(attribute))

        if order_criteria:
            query = query.order_by(*order_criteria)

    items = query.all()    
    return items

def get_distributor_items(db: Session, distributor_id: int, skip: int = 0, limit: int = 100):
    pass

def get_distributor_items_by_distributorID(db: Session, distributor_id: int, skip: int = 0, limit: int = 100):
    pass
