from tartiflette import Resolver
from typing import Any, Dict, List, Optional

from beondiet.queries import BeondietDataAccessor
from db.db_conn import create_db_session

@Resolver("Query.ingredients")
async def resolve_query_ingredients(parent: Optional[Any], args: Dict[str, Any], ctx: Dict[str, Any], info: "ResolveInfo",
) -> List[Dict[str, Any]]:
    data_accessor = BeondietDataAccessor(create_db_session())
    return await data_accessor.get_all_ingredient()

@Resolver("Query.ingredient")
async def resolve_query_ingredient_by_id(parent: Optional[Any], args: Dict[str, Any], ctx: Dict[str, Any], info: "ResolveInfo",
) -> Dict[str, Any]:
    ingredient_id = args["id"]
    data_accessor = BeondietDataAccessor(create_db_session())
    return await data_accessor.get_ingredient_by_id(ingredient_id)

@Resolver("Query.recipes")
async def resolve_query_recipes(parent: Optional[Any], args: Dict[str, Any], ctx: Dict[str, Any], info: "ResolveInfo",
) -> List[Dict[str, Any]]:
    data_accessor = BeondietDataAccessor(create_db_session())
    return await data_accessor.get_all_recipes()

@Resolver("Query.recipe")
async def resolve_query_recipe_by_id(parent: Optional[Any], args: Dict[str, Any], ctx: Dict[str, Any], info: "ResolveInfo",
) -> Dict[str, Any]:
    receipe_id = args["id"]
    data_accessor = BeondietDataAccessor(create_db_session())
    return await data_accessor.get_receipe_by_id(receipe_id)