from recibundler.schema.reciperow import reciperow
import string


def get_recipe_filename(recipe: reciperow) -> str:

    return f"{recipe.name.strip().translate(str.maketrans('', '', '!@#$%^*()[]{}~`;:')).replace(' ', '-').lower()}.json"
