from typing import Any, Dict
from beondiet.queries import BeondietDataAccessor
from beondiet.models import Ingredients, meal_type, Receipts, Ingredients_Recipe
from datetime import date

class BeondietDataMutator(BeondietDataAccessor):
    @staticmethod
    def format_macros(grams:int, carbs:float, protein:float, fat:float, kcal: int) -> Dict[str, Any]:
        macros = {"grams": grams,"carbs": carbs, "protein": protein, "fat":fat, "kcal": kcal}
        return macros

    async def insertIngredient(self, name:str, carbs:float , protein:float, fat:float, kcal:int) -> Dict[str, Any]:
        ingredient = Ingredients(name=name, carbs=carbs, protein=protein, fat=fat, kcal=kcal)
        self._session.add(ingredient)
        self._session.commit()
        self._session.refresh(ingredient)

        return ingredient

    async def updateIngredient(self, updatedfields, ingredient_id) -> Dict[str, Any]:
        self._session.query(Ingredients).filter_by(id= ingredient_id).update(updatedfields)
        self._session.commit()

        ingredient = await self.get_ingredient(ingredient_id)
        return ingredient

    async def deleteIngredient(self, ingredient_id):
        await self.get_ingredient(ingredient_id)
        self._session.query(Ingredients).filter_by(id= ingredient_id).delete(synchronize_session=False)
        self._session.commit()

    async def insertRecipe(self, name:str, meal_type:meal_type, ingredients:dict) -> Dict[str, Any]:
        receipe = Receipts(version= 1, name=name, last_update= date.today(), meal_type=meal_type, grams=None, carbs=None, protein=None, fat=None, kcal=None)
        self._session.add(receipe)
        self._session.commit()
        self._session.refresh(receipe)

        receipe_id = await self.get_receipe_id_by_name_and_version(name,1)

        macros = await self.addIngredientsToReceipe(ingredients, receipe_id)

        receipe = await self.updateReceipeTable(macros, receipe_id)

        return receipe

    async def updateReceipe(self, name:str, meal_type:meal_type, ingredients:dict, receipe_id:int,  name_or_meal_changed = True, ingredients_changed = True):
        #name_or_meal_changed, ingredients_changed - to communicate with client, if both False no action elif one of them False - block not needed insert.
        if (name_or_meal_changed == False and ingredients_changed == False):
            receipe = self.get_receipe(receipe_id)
        else:
            updatedfields = {}
            macros = {}
            if name_or_meal_changed == True:
                updatedfields['name'] = name
                updatedfields['meal_type'] = meal_type
            if ingredients_changed == True:
                macros = await self.addIngredientsToReceipe(ingredients, receipe_id)

            updatedfields['last_update'] = date.today()
            updatedfields.update(macros)
            receipe = await self.updateReceipeTable(updatedfields, receipe_id)

        return receipe

    async def updateReceipeTable(self, updatedfields, receipe_id) -> Dict[str, Any]:

        self._session.query(Receipts).filter_by(id= receipe_id).update(updatedfields)
        self._session.commit()

        receipe = await self.get_receipe_by_id(receipe_id)

        # problem z tym czy zwracamy recipe z ingredientami czy bez
        return receipe

    async def addIngredientsToReceipe(self,ingredients:dict, receipe_id:int):
        macros = [0, 0.0, 0.0, 0.0, 0]
        for ingredient_id in ingredients:
            ingr_rec = Ingredients_Recipe(receipts_id=receipe_id, ingred_id=ingredient_id, grams=ingredients[ingredient_id])
            self._session.add(ingr_rec)

            ingredient = await self.get_ingredient(ingredient_id)
            gr_ingr_rat = ingredients[ingredient_id]/100
            macros_ingredient = [ingredients[ingredient_id], ingredient.carbs*gr_ingr_rat, ingredient.protein*gr_ingr_rat, ingredient.fat*gr_ingr_rat, ingredient.kcal*gr_ingr_rat]
            macros = [x + y for x, y in zip(macros, macros_ingredient)]


        self._session.commit()
        result = self.format_macros(grams=macros[0], carbs=macros[1] , protein=macros[2], fat=macros[3], kcal=macros[4])
        return result

    async def deleteReceipe(self, receipe_id):
        await self.get_receipe(receipe_id)
        self._session.query(Ingredients_Recipe).filter_by(receipts_id=receipe_id).delete(synchronize_session=False)
        self._session.commit()

        self._session.query(Receipts).filter_by(id= receipe_id).delete(synchronize_session=False)
        self._session.commit()

