import enum
from typing import Any
from sqlalchemy import Column, Date, Enum, Float, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from db.db_conn import engine

Base: Any = declarative_base()
metadata = Base.metadata

class meal_type(enum.Enum):
    breakfast = "breakfast"
    lunch = "lunch"
    dinner = "dinner"

class Ingredients(Base):
    __tablename__ = "ingredients"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True)
    carbs = Column(Float, nullable=False)
    protein = Column(Float, nullable=False)
    fat = Column(Float, nullable=False)
    kcal = Column(Integer, nullable=False)

class Receipts(Base):
    __tablename__ = "receipts"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    version = Column(Integer, nullable=False)
    name = Column(String, nullable=False, unique=True)
    last_update = Column(Date, nullable=False)
    meal_type = Column("meal_type", Enum(meal_type), nullable=False)
    grams = Column(Integer, nullable=True)
    carbs = Column(Float, nullable=True)
    protein = Column(Float, nullable=True)
    fat = Column(Float, nullable=True)
    kcal = Column(Integer, nullable=True)


class Ingredients_Recipe(Base):
    __tablename__ = "ingr_rec"
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    receipts_id = Column(Integer, ForeignKey("receipts.id"))
    ingred_id = Column(Integer, ForeignKey("ingredients.id"))
    grams = Column(Integer, nullable=False)

metadata.create_all(engine)