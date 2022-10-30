import unittest
from pprint import pprint as print
import reciparcer


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
            2, len(result), "Result list should have length 2 (for 2 sections)"
        )
        self.assertEqual("scones", result[0])
        self.assertEqual("glaze", result[1])


class TestParseSection(unittest.TestCase):
    def test_should_return_text_without_parenths(self):
        result = reciparcer.parse_section("(scones)")
        self.assertEqual("scones", result)

    def test_should_strip_whitespace(self):
      result = reciparcer.parse_section(' ( onion soup )   ')
      self.assertEqual('onion soup', result)
    
    def test_should_return_none_if_invalid(self):
      result = reciparcer.parse_section('3 cup instant noodles, (dry)')
      self.assertIsNone(result)