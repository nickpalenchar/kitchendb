import unittest

from recibundler.json_writing import util
from collections import namedtuple

partialreciperow = namedtuple('partialreciperow', ['name'])

class TestGetsFilename(unittest.TestCase):
    def test_strips_punctuation_allows_double_quotes(self):
        result = util.get_recipe_filename(partialreciperow('Mock "clif" bars!!'))
        self.assertEqual('mock-"clif"-bars.json', result)
    
    def test_allows_single_quotes(self):
      result = util.get_recipe_filename(partialreciperow("Mom's Famous Pie"))
      self.assertEqual("mom's-famous-pie.json", result)

    def test_handle_whitespace(self):
      result = util.get_recipe_filename(partialreciperow(" apple  pie "))
      self.assertEqual('apple--pie.json', result)