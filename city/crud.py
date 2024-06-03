# from sqlalchemy import delete, update
# from sqlalchemy.orm import Session
#
# from city import models, schemas
# from city.models import DBCity
#
#
# def get_list_of_cities(
#         db: Session,
#         skip: int | None,
#         limit: int | None
# ) -> list[models.DBCity]:
#
#     queryset = db.query(models.DBCity)
#     if skip:
#         queryset = queryset.offset(skip)
#     if limit:
#         queryset = queryset.limit(limit)
#     return queryset.all()
#
#
# def get_city_by_id(db: Session, city_id: int) -> models.DBCity:
#     return (
#         db.query(models.DBCity).filter(
#             models.DBCity.id == city_id).first()
#     )
#
#
# def get_city_by_name(db: Session, city_name: int) -> models.DBCity:
#     return (
#         db.query(models.DBCity).filter(
#             models.DBCity.name == city_name).first()
#     )
#
# def create_city(db: Session, city: schemas.CityCreate) -> models.DBCity:
#     db_city = DBCity(
#         name=city.name,
#         additional_info=city.additional_info
#     )
#     db.add(db_city)
#     db.commit()
#     db.refresh(db_city)
#     return db_city
#
#
# def update_city(
#     db: Session, city_id: int, city: schemas.CityUpdate
# ) -> models.DBCity:
#     query = update(models.DBCity).where(models.DBCity.id == city_id).values(**city.dict())
#     db.execute(query)
#     db.commit()
#     updated_city = get_city_by_id(db=db, city_id=city_id)
#     return updated_city
#
#
# def delete_city(db: Session, city_id: int) -> None:
#     query = delete(models.DBCity).where(models.DBCity.id == city_id)
#     db.execute(query)
#     db.commit()
from fastapi import HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from city import models, schemas


async def get_all_cities(db: AsyncSession):
    query = select(models.DBCity)
    cities = await db.execute(query)
    return [city[0] for city in cities.fetchall()]


async def get_city_by_id(db: AsyncSession, city_id: int):
    query = select(models.DBCity).filter(models.DBCity.id == city_id)
    city = await db.execute(query)
    return city.first()[0]


async def get_city_by_name(db: AsyncSession, name: str):
    query = select(models.DBCity).filter(models.DBCity.name == name)
    city = await db.execute(query)
    return city.first()


async def update_city_by_id(db: AsyncSession, city: schemas.CityCreate, city_id: int):
    query = (
        update(models.DBCity).
        where(models.DBCity.id == city_id).
        values(name=city.name, additional_info=city.additional_info)
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": city_id}
    return resp


async def create_city(db: AsyncSession, city: schemas.CityCreate):
    query = insert(models.DBCity).values(
        name=city.name,
        additional_info=city.additional_info
    )
    result = await db.execute(query)
    await db.commit()
    resp = {**city.model_dump(), "id": result.lastrowid}
    return resp


async def delete_city_by_id(db: AsyncSession, city_id: int):
    city = await db.get(models.DBCity, city_id)

    if city is None:
        raise HTTPException(status_code=404, detail="City with this ID does not exists")

    query = delete(models.DBCity).where(
        models.DBCity.id == city_id
    )

    await db.execute(query)
    await db.commit()

    resp = {"name": city.name, "additional_info": city.additional_info, "id": city_id}
    return resp
