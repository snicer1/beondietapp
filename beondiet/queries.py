from typing import Any, Dict, List
from sqlalchemy.orm import Query, Session
from sqlalchemy.orm.exc import NoResultFound

from beondiet import models



class BeondietDataAccessor:
    def __init__(self, session: Session):
        self._session = session

    @property
    def queryIngredient(self) -> Query:
        return self._session.query(
            models.Ingredients.id,
            models.Ingredients.name,
            models.Ingredients.carbs,
            models.Ingredients.protein,
            models.Ingredients.fat,
            models.Ingredients.kcal,
        )

    @property
    def queryRecipe(self) -> Query:
        return self._session.query(
            models.Receipts.id,
            models.Receipts.version,
            models.Receipts.name,
            models.Receipts.last_update,
            models.Receipts.meal_type,
            models.Receipts.grams,
            models.Receipts.carbs,
            models.Receipts.protein,
            models.Receipts.fat,
            models.Receipts.kcal,
        )

    @staticmethod
    def format_ingredient(
            id: int,
            name: str,
            carbs: float,
            protein: float,
            fat: float,
            kcal: int,
    ) -> Dict[str, Any]:
        ingredient = {
            "id": id,
            "name": name,
            "carbs": carbs,
            "protein": protein,
            "fat": fat,
            "kcal": kcal,
        }
        return ingredient

    @staticmethod
    def format_receipe(
            id: int,
            version: int,
            name: str,
            last_update: str,
            meal_type: models.meal_type,
            grams: int,
            carbs: float,
            protein: float,
            fat: float,
            kcal: int,
    ) -> Dict[str, Any]:
        recipe = {
            "id": id,
            "version": version,
            "name": name,
            "last_update": last_update,
            "meal_type": meal_type.value,
            "grams": grams,
            "carbs": carbs,
            "protein": protein,
            "fat": fat,
            "kcal": kcal,
        }
        return recipe

    async def get_all_ingredient(self)-> List[Dict[str, Any]]:
        result = [
            self.format_ingredient(id = id, name= name, carbs=carbs, protein=protein, fat=fat, kcal=kcal)
        for id, name, carbs, protein, fat, kcal in self.queryIngredient
        ]

        return result

    # async def get_ingredient_by_id(self, ingredient_id: int) -> Dict[str, Any]:
    #     ingredient = self.session.query(models.Ingredients).get(ingredient_id)
    #     result = self.format_ingredient(id=ingredient.id, name=ingredient.name, carbs=ingredient.carbs, protein=ingredient.protein, fat=ingredient.fat, kcal=ingredient.kcal)
    #     print(result)
    #     return result


    async def get_ingredient_by_id(self, ingredient_id: int) -> Dict[str, Any]:
        ingredient = await self.get_ingredient(ingredient_id)
        result = self.format_ingredient(id=ingredient.id, name=ingredient.name, carbs=ingredient.carbs, protein=ingredient.protein, fat=ingredient.fat, kcal=ingredient.kcal)
        return result

    async def get_ingredient(self, ingredient_id: int) -> models.Ingredients:
        qry = self.queryIngredient.filter_by(id= ingredient_id)
        try:
            ingredient = qry.one()
        except NoResultFound:
           raise RuntimeWarning(f"Error. No ingredient with id number = {ingredient_id}.")

        return ingredient

    async def get_all_recipes(self)-> List[Dict[str, Any]]:
        result = [
            self.format_receipe(id = id, version=version, name= name, last_update=last_update , meal_type=meal_type, grams=grams, carbs=carbs, protein=protein, fat=fat, kcal=kcal)
        for id, version, name, last_update, meal_type, grams, carbs, protein, fat, kcal in self.queryRecipe
        ]

        return result

    async def get_receipe_by_id(self, receipe_id: int) -> Dict[str, Any]:
        receipe = await self.get_receipe(receipe_id)
        result = self.format_receipe(id= receipe.id, version=receipe.version, name= receipe.name, last_update=receipe.last_update ,
                                     meal_type=receipe.meal_type, grams=receipe.grams, carbs=receipe.carbs, protein=receipe.protein, fat=receipe.fat, kcal=receipe.kcal)
        return result

    async def get_receipe(self, receipe_id: int) -> models.Receipts:
        qry = self.queryRecipe.filter_by(id=receipe_id)
        try:
            receipe = qry.one()
        except NoResultFound:
            raise RuntimeWarning(f"Error. No receipe with id number = {receipe_id}.")
        print(receipe)
        return receipe

    async def get_receipe_id_by_name_and_version(self, name: str, version: int) -> int:
        qry = self.queryRecipe.filter_by(name= name,version=version)
        try:
            receipe = qry.one()
        except NoResultFound:
            raise RuntimeWarning(f"Error with inserting new receipe. Rollback")

        return receipe.id
