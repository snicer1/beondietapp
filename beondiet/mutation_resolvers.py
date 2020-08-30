from tartiflette import Resolver
from typing import Any, Dict, Optional

from beondiet.mutation import BeondietDataMutator
from db.db_conn import create_db_session


@Resolver("Mutation.createIngredient")
async def resolve_create_ingredient(parent: Optional[Any], args: Dict[str, Any], ctx: Dict[str, Any],
                                    info: "ResolveInfo",
                                    ) -> Dict[str, Any]:
    name = args["input"]["name"]
    carbs = args["input"]["carbs"]
    protein = args["input"]["protein"]
    fat = args["input"]["fat"]
    kcal = args["input"]["kcal"]
    data_accessor = BeondietDataMutator(create_db_session())
    return await data_accessor.insertIngredient(name, carbs, protein, fat, kcal)


@Resolver("Mutation.updateIngredient")
async def resolve_update_ingredient(parent: Optional[Any], args: Dict[str, Any], ctx: Dict[str, Any],
                                    info: "ResolveInfo",
                                    ) -> Dict[str, Any]:
    fields_to_update = {}
    ingredient_id = 0
    for field in args["input"]:
        if field == "id":
            ingredient_id = args["input"][field]
        else:
            fields_to_update[field] = args["input"][field]

    data_accessor = BeondietDataMutator(create_db_session())
    return await data_accessor.updateIngredient(fields_to_update, ingredient_id)


@Resolver("Mutation.deleteIngredient")
async def resolve_delete_ingredient(parent: Optional[Any], args: Dict[str, Any], ctx: Dict[str, Any],
                                    info: "ResolveInfo",
                                    ) -> Dict[str, Any]:
    ingredient_id = args["id"]
    data_accessor = BeondietDataMutator(create_db_session())
    await data_accessor.deleteIngredient(ingredient_id)
    return {'id': ingredient_id}


@Resolver("Mutation.createRecipe")
async def resolve_create_receipe(parent: Optional[Any], args: Dict[str, Any], ctx: Dict[str, Any], info: "ResolveInfo",
                                 ) -> Dict[str, Any]:
    dict_ingredient = {}
    name = args["input"]["name"]
    meal_type = args["input"]["meal_type"]
    list_of_ingredients = args["input"]["ingredients"]
    for ingredient in list_of_ingredients:
        dict_ingredient[ingredient["ingredient_id"]] = ingredient["grams"]

    data_accessor = BeondietDataMutator(create_db_session())
    return await data_accessor.insertRecipe(name, meal_type, dict_ingredient)

@Resolver("Mutation.updateRecipe")
async def resolve_update_receipe(parent: Optional[Any], args: Dict[str, Any], ctx: Dict[str, Any], info: "ResolveInfo",
                                 ) -> Dict[str, Any]:
    dict_ingredient = {}
    receipe_id = args["input"]["id"]
    name = args["input"]["name"]
    meal_type = args["input"]["meal_type"]
    list_of_ingredients = args["input"]["ingredients"]
    for ingredient in list_of_ingredients:
        dict_ingredient[ingredient["ingredient_id"]] = ingredient["grams"]

    data_accessor = BeondietDataMutator(create_db_session())
    return await data_accessor.updateReceipe(name, meal_type, dict_ingredient, receipe_id)

@Resolver("Mutation.deleteReceipe")
async def resolve_delete_receipe(parent: Optional[Any], args: Dict[str, Any], ctx: Dict[str, Any],
                                    info: "ResolveInfo",
                                    ) -> Dict[str, Any]:
    receipe_id = args["id"]
    data_accessor = BeondietDataMutator(create_db_session())
    await data_accessor.deleteReceipe(receipe_id)
    return {'id': receipe_id}