from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from my_app import crud, models, schemas
from my_app.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create distributor if it doesnt already exist (checked by title and address)
# Works

@app.get("/distributors/{distributor_id}/", response_model= schemas.DistributorBase)
def read_distributor_by_id(distributor_id: int, db: Session = Depends(get_db)):
    return crud.get_distributor_by_id(db=db,id=distributor_id)


@app.post("/distributors/", response_model=schemas.Distributor)
def create_distributor(distributor: schemas.DistributorCreate, db: Session = Depends(get_db)):
    db_distributor = crud.get_distributor(
        db=db, title=distributor.title, address=distributor.address)
    if db_distributor:
        raise HTTPException(
            status_code=400, detail="Distributor already registered")
    return crud.create_distributor(db=db, distributor=distributor)

# Create an item for a distributor specified by the distributor's id.
# Works


@app.post("/distributors/{distributor_id}/items/", response_model=schemas.Item)
def create_item_for_distributor(distributor_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_distributor_item(db=db, item=item, distributor_id=distributor_id)


# Get a Distributor specified by its address
# Works
@app.get("/distributors/{distributor_address}/", response_model=schemas.Distributor)
def read_distributor_on_address(distributor_address: str, db: Session = Depends(get_db)):
    db_distributor = crud.get_distributor_by_address(
        db, address=distributor_address)
    if db_distributor is None:
        raise HTTPException(status_code=404, detail="Distributor not found")
    return db_distributor

# Get all distributors
# Works


@app.get("/distributors/", response_model=list[schemas.Distributor])
def read_distributors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    distributors = crud.get_distributors(db, skip=skip, limit=limit)
    return distributors

# Get all distributor addresses - This only gives back the name of the distributor and the address of it. (only difference is in the response_model)
# Works


@app.get("/distributors/addresses", response_model=list[schemas.DistributorCreate])
def read_distributor_addresses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    distributors = crud.get_distributors(db, skip=skip, limit=limit)
    return distributors

# Works


@app.get("/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, sort: bool = False , db: Session = Depends(get_db)):
    items = crud.get_all_items(db, skip, limit,sort_by_price_asc= sort)
    return items

# @app.get("/itemtypes/",response_model=list[schemas.ItemType])
# def read_itemtypes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     itemtypes = crud.get_itemtypes(db, skip=skip, limit=limit)
#     return itemtypes

@app.get("/itemtypes/", response_model=list[str])
async def read_enum_values():
    return crud.get_enum_values(models.ItemType)

@app.get("/items-sorted/", response_model=list[schemas.Item])
def read_items_sorted(sort: bool = False, price_sort: str = "", name_sort: str = "", item_type_sort: str = "", distributor_sort: str = "" , db: Session = Depends(get_db)):
    items = crud.get_all_items_sorted(db, sort= sort, price_sort=price_sort, name_sort=name_sort, item_type_sort=item_type_sort, distributor_sort=distributor_sort)
    return items
