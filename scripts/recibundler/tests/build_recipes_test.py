import unittest

from recibundler import build_recipes


class TestCamelToSnakeCase(unittest.TestCase):
    def test_parses_camel_case(self):
        result = build_recipes.camel_to_snake_case("helloEveryOne")
        self.assertEqual("hello-every-one", result)

    def test_parses_with_dots(self):
        result = build_recipes.camel_to_snake_case("helloWorld.json")
        self.assertEqual("hello-world.json", result)

    def test_parses_numbers(self):
        result = build_recipes.camel_to_snake_case("2022-01-30-myFavoriteRecipe.json")
        self.assertEqual("2022-01-30-my-favorite-recipe.json", result)
