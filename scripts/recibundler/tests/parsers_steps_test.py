import unittest

import reciparcer


class TestStepsParser(unittest.TestCase):
    def test_parses_steps_into_list(self):
        line = """
Chop ingredients
Place ingredients in a bowl
Mix"""
        result = reciparcer.parse_steps(line)
        self.assertListEqual(
            [
                {
                    "sectionTitle": "",
                    "steps": ["Chop ingredients", "Place ingredients in a bowl", "Mix"],
                }
            ],
            result,
        )

    def test_removes_unnecessary_lines(self):
        line = """start the thing


next thing"""
        result = reciparcer.parse_steps(line)
        self.assertListEqual(
            [{"sectionTitle": "", "steps": ["start the thing", "next thing"]}], result
        )

    def test_removes_step_numbers(self):
        line = "1. the first step\n2. the second step\n3. the third step"
        result = reciparcer.parse_steps(line)
        self.assertListEqual(
            [
                {
                    "sectionTitle": "",
                    "steps": ["the first step", "the second step", "the third step"],
                }
            ],
            result,
        )
