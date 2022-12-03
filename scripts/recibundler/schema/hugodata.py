"""
builds the jsonschemas into a python class for easy
class construction that will be valid to the schema

Used in add_new_recipes.py to write now json files of recipes
submitted by users.
"""
import warlock
import pathlib
import os
import json

with open(
    os.path.join(
        pathlib.Path(__file__).parent.absolute(), "../../../data/schemas/recipes.json"
    )
) as fh:
    recipe_schema = json.loads(fh.read())
    Recipe = warlock.model_factory(recipe_schema)

with open(
    os.path.join(
        pathlib.Path(__file__).parent.absolute(),
        "../../../data/schemas/ingredient.json",
    )
) as fh:
    ingredient_schema = json.loads(fh.read())
    Ingredient = warlock.model_factory(ingredient_schema)
