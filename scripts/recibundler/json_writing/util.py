from recibundler.schema.reciperow import reciperow

def get_recipe_filename(recipe: reciperow) -> str:
    return f"{recipe.name.replace(' ', '-').lower()}.json"
  