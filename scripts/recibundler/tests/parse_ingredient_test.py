import unittest

from recibundler import reciparcer


class TestParseIngredient(unittest.TestCase):
    def test_parses_with_number(self):
        line = "2 Granny Smith or other tart cooking apples (15 oz.), peeled, cored, and thinly sliced"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            {
                "amount": [2.0],
                "customUnit": "",
                "ingredient": "Granny Smith or other tart cooking apples (15 oz.)",
                "modifier": "peeled, cored, and thinly sliced",
            },
            result,
        )

    def test_parses_number_no_modifier(self):
        line = "1 cup flour"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            {"amount": [1.0], "unit": "cup", "ingredient": "flour"}, result
        )

    def test_parses_fraction_unicode_and_extra_whitespace(self):
        line = "    ¾ cup all-purpose flour  "
        result = reciparcer.parse_ingredient(line)
        # TB: this will probably fail once customUnit is better established. That is a fail we WANT and this should be
        # updated to pass with the new stuff
        self.assertDictEqual(
            {
                "amount": [0.75],
                "unit": "cup",
                "ingredient": "all-purpose flour",  # (expect-error) cup should be in "unit"
            },
            result,
        )

    def test_parses_decimal(self):
        line = "2.5 cup cinnamon"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            result, {"amount": [2.5], "unit": "cup", "ingredient": "cinnamon"}
        )

    @unittest.skip("todo")
    def test_trims_long_decimal(self):
        line = "1.5304 cup ginger"
        result = reciparcer.parse_ingredient(line)
        self.assertDictContainsSubset(
            {"amount": 1.5, "ingredient": "cup ginger"}, result
        )

    def test_parses_fractions(self):
        line = "1/8 tbsp salt"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            {"amount": [0.12], "unit": "tbsp", "ingredient": "salt"}, result
        )

    def test_parses_modifiers(self):
        """
        modifiers explain how the ingredient in prepped, after the ingredient is listed
        """
        line = "3 cup onions, chopped, then mashed"

        result = reciparcer.parse_ingredient(line)
        self.assertDictContainsSubset(
            {"modifier": "chopped, then mashed"}, result, msg=result
        )

    def test_handles_plurals(self):
        line1 = "3 cups onion"
        line2 = "3 tbsps ginger, minced"

        result1 = reciparcer.parse_ingredient(line1)
        result2 = reciparcer.parse_ingredient(line2)

        self.assertDictEqual(
            {"amount": [3.0], "unit": "cup", "ingredient": "onion"}, result1
        )
        self.assertDictEqual(
            {
                "amount": [3.0],
                "unit": "tbsp",
                "ingredient": "ginger",
                "modifier": "minced",
            },
            result2,
        )

    def test_handle_range(self):
        line = "6-7 gals milk"
        result = reciparcer.parse_ingredient(line)
        self.assertIsNotNone(result)
        self.assertDictEqual(
            {"amount": [6.0, 7.0], "unit": "gal", "ingredient": "milk"}, result
        )

    def test_parse_unit_handles_caps(self):
        line = "1 TSP baking soda"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            {"amount": [1.0], "unit": "tsp", "ingredient": "baking soda"}, result
        )

    def test_parse_with_alias_unit(self):
        line = "1 tablespoon ginger"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            {"amount": [1.0], "unit": "tbsp", "ingredient": "ginger"}, result
        )

    def test_parse_with_alias_unit2(self):
        line = "1 ounces butternut squash"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            {"amount": [1.0], "unit": "oz", "ingredient": "butternut squash"}, result
        )

    def test_parse_with_ingredient_aliases(self):
        line = "10 cup frozen corn kernals"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            {"amount": [10.0], "unit": "cup", "ingredient": "frozen corn"},
            result
        )

    def test_parses_whole_number_and_fraction(self):
        line = "1 1/2 cup frozen corn"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            {"amount": [1.5], "unit": "cup", "ingredient": "frozen corn"}, result
        )

    def test_parse_ingredient2(self):
        line = "4 oz medium shallots (about 2-3 bulbs, cut into quarters)"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            {
                "amount": [4.0],
                "unit": "oz",
                "ingredient": "medium shallots (about 2-3 bulbs",
                "modifier": "cut into quarters)"
            },
            result,
        )

    def test_strip_alternate_measurements(self):
        """This will be added programmatically"""
        line = "8-10 oz (227g -283g) chicken breast"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            {
                "amount": [8.0, 10.0],
                "unit": "oz",
                "ingredient": "chicken breast",
            },
            result,
        )

    def test_strip_alternate_measurements2(self):
        """This will be added programmatically"""
        line = "1/4 cup (60 mL) original soy sauce"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            {
                "amount": [0.25],
                "unit": "cup",
                "ingredient": "soy sauce", # alias to original soy sauce
            },
            result,
        )