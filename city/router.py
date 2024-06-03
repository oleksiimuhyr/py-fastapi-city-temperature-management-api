# from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session
#
# from city import schemas, crud
# from dependencies import get_db
#
# router = APIRouter()
#
#
# @router.get('/cities/', response_model=list[schemas.City])
# def get_all_cities(
#         db: Session = Depends(get_db),
#         limit: int | None = None,
#         skip: int | None = None,
# ) -> list[schemas.City]:
#     return crud.get_list_of_cities(db=db, skip=skip, limit=limit)
#
#
# @router.post('/cities/', response_model=schemas.City)
# def create_city(
#         city: schemas.CityCreate,
#         db: Session = Depends(get_db)
# ) -> schemas.City:
#     db_cities = crud.get_city_by_name(db=db, city_name=city.name)
#
#     if db_cities:
#         raise HTTPException(
#             status_code=400, detail='This city already exist')
#     return crud.create_city(db=db, city=city)
#
#
# @router.get('/cities/{city_id}/', response_model=schemas.City)
# def get_city_by_id(city_id: int,
#                    db: Session = Depends(get_db)) -> schemas.City:
#     db_city = crud.get_city_by_id(db=db, city_id=city_id)
#
#     if db_city is None:
#         raise HTTPException(status_code=404, detail='City not found')
#
#     return db_city
#
#
# @router.put("/cities/{city_id}/", response_model=schemas.City)
# def update_city(
#     city: schemas.CityUpdate, city_id: int, db: Session = Depends(get_db)
# ) -> schemas.City:
#     if not crud.get_city_by_id(db=db, city_id=city_id):
#         raise HTTPException(status_code=404, detail="City not found")
#
#     if existed_city_by_name := crud.get_city_by_name(db=db, city_name=city.name):
#         if existed_city_by_name.id != city_id:
#
#             raise HTTPException(
#                 status_code=404, detail="City with such name already exists"
#             )
#
#     updated_city = crud.update_city(db=db, city_id=city_id, city=city)
#
#     return updated_city
#
#
# @router.delete("/cities/{city_id}/", status_code=204)
# def delete_city(city_id: int, db: Session = Depends(get_db)) -> None:
#     if not crud.get_city_by_id(db=db, city_id=city_id):
#         raise HTTPException(status_code=404, detail="City not found")
#
#     crud.delete_city(db=db, city_id=city_id)

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from city import schemas, crud
from dependencies import get_db

router = APIRouter()


@router.get("/cities/", response_model=list[schemas.City])
async def read_all_cities(db: AsyncSession = Depends(get_db)):
    return await crud.get_all_cities(db)


@router.get("/cities/{city_id}/", response_model=schemas.City)
async def read_city(city_id: int, db: AsyncSession = Depends(get_db)):
    city = await crud.get_city_by_id(db, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City with this ID does not exists")

    return city


@router.post("/cities/", response_model=schemas.City)
async def create_city(city: schemas.CityCreate, db: AsyncSession = Depends(get_db)):
    db_city = await crud.get_city_by_name(db, city.name)

    if db_city:
        raise HTTPException(
            status_code=400, detail="City with this name already exists"
        )

    return await crud.create_city(db, city)


@router.put("/cities/{city_id}/", response_model=schemas.City)
async def update_city(
    new_info: schemas.CityCreate, city_id: int, db: AsyncSession = Depends(get_db)
):
    db_city = await crud.get_city_by_id(db, city_id)

    if db_city is None:
        raise HTTPException(status_code=404, detail="City with this ID does not exists")

    return await crud.update_city_by_id(db, new_info, city_id)


@router.delete("/cities/{city_id}/", response_model=schemas.City)
async def remove_city(city_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.delete_city_by_id(db, city_id)
