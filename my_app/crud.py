from sqlalchemy.orm import Session
from my_app import models, schemas


def create_distributor(db: Session, distributor: schemas.DistributorCreate):
    db_distributor = models.Distributor(
        title=distributor.title, address=distributor.address)
    db.add(db_distributor)
    db.commit()
    db.refresh(db_distributor)
    return db_distributor


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


def get_all_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

# get all items of a distributor, search by id of distributor


def get_distributor_items(db: Session, distributor_id: int, skip: int = 0, limit: int = 100):
    pass

# Get all items of a distributor, search by ShopName? (rename ShopName enum)


def get_distributor_items_by_distributorID(db: Session, distributor_id: int, skip: int = 0, limit: int = 100):
    pass
