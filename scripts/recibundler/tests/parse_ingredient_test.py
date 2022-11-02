import unittest

from recibundler import reciparcer

class TestParseIngredient(unittest.TestCase):
    def test_parses_with_number(self):
        line = "2 Granny Smith or other tart cooking apples (15 oz.), peeled, cored, and thinly sliced"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            {
                "amount": 2.0,
                "customUnit": "",
                "ingredient": "Granny Smith or other tart cooking apples (15 oz.)",
                "modifier": "peeled, cored, and thinly sliced",
            },
            result,
        )

    def test_parses_fraction_unicode_and_extra_whitespace(self):
        line = "    ¾ cup all-purpose flour  "
        result = reciparcer.parse_ingredient(line)
        # TB: this will probably fail once customUnit is better established. That is a fail we WANT and this should be
        # updated to pass with the new stuff
        self.assertDictEqual(
            {
                "amount": 0.75,
                "unit": "cup",
                "ingredient": "all-purpose flour",  # (expect-error) cup should be in "unit"
            },
            result,
        )

    def test_parses_decimal(self):
        line = "2.5 cup cinnamon"
        result = reciparcer.parse_ingredient(line)
        self.assertDictEqual(
            result, {"amount": 2.5, "unit": "cup", "ingredient": "cinnamon"}
        )

    @unittest.skip("todo")
    def test_trims_long_decimal(self):
        line = "1.5304 cup ginger"
        result = reciparcer.parse_ingredient(line)
        self.assertDictContainsSubset(
            {"amount": 1.5, "ingredient": "cup ginger"}, result
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
