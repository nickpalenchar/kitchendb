import unittest
from pprint import pprint as print
from recibundler import reciparcer


class TestParseIngredients(unittest.TestCase):
    def test_can_parse_sections(self):
        recipe = """(scones)
1 cup flour
1 dash salt

(glaze)
1 squeeze of lemon juice
0.5 cups confectioners sugar, sifted
"""
        result = reciparcer.parse_ingredients(recipe)
        self.assertEqual(
            2,
            len(result[0]["ingredients"]),
            f"first section should have 2 ingredients. But got {result[0]['ingredients']}",
        )
        self.assertEqual(
            2,
            len(result),
            f"Result list should have length 2 (for 2 sections)\n result was {result}",
        )
        self.assertEqual("scones", result[0]["sectionTitle"])
        self.assertEqual("glaze", result[1]["sectionTitle"])

    def test_can_parse_sections_2(self):
        recipe = """(Meat)
Steak or Beef Steak

(Puree Marinade)
1 pear, chopped
0.5 onion, chopped
Thumbnail size of ginger, zested
1 tbsp minced garlic

(Soy Marinade)
2 cups soy sauce
2 cups water
1 cup Mirin
1 cup Sugar"""
        result = reciparcer.parse_ingredients(recipe)
        self.assertDictEqual(
            {
                "ingredients": [{"ingredient": "Steak or Beef Steak"}],
                "sectionTitle": "Meat",
            },
            result[0],
        )
        self.assertDictEqual(
            {
                "ingredients": [
                    {
                        "amount": [1.0],
                        "customUnit": "",
                        "ingredient": "pear",
                        "modifier": "chopped",
                    },
                    {
                        "amount": [0.5],
                        "customUnit": "",
                        "ingredient": "onion",
                        "modifier": "chopped",
                    },
                    {"ingredient": "Thumbnail size of ginger, zested"},
                    {"amount": [1.0], "ingredient": "minced garlic", "unit": "tbsp"},
                ],
                "sectionTitle": "Puree Marinade",
            },
            result[1],
        )
        self.assertDictEqual(
            {
                "ingredients": [
                    {"amount": [2.0], "ingredient": "soy sauce", "unit": "cup"},
                    {"amount": [2.0], "ingredient": "water", "unit": "cup"},
                    {"amount": [1.0], "ingredient": "Mirin", "unit": "cup"},
                    {"amount": [1.0], "ingredient": "Sugar", "unit": "cup"},
                ],
                "sectionTitle": "Soy Marinade",
            },
            result[2],
        )


class TestParseSection(unittest.TestCase):
    def test_should_return_text_without_parenths(self):
        result = reciparcer.parse_section("(scones)")
        self.assertEqual("scones", result)

    def test_should_strip_whitespace(self):
        result = reciparcer.parse_section(" ( onion soup )   ")
        self.assertEqual("onion soup", result)

    def test_should_return_none_if_invalid(self):
        result = reciparcer.parse_section("3 cup instant noodles, (dry)")
        self.assertIsNone(result)

    def test_should_update_section_if_its_first(self):
        result = reciparcer.parse_ingredients(
            """(scones)
1 cup flour
1 tsp salt
"""
        )
        self.assertEqual("scones", result[0]["sectionTitle"])
        self.assertEqual(1, len(result))
