import unittest
from app.controller import PredictionBot


class PredictionBotTests(unittest.TestCase):
    bot = PredictionBot()

    def test_name_look_up(self):
        actual = self.bot.name_lookup('Wedding Cake')['_id']
        expected = 440
        self.assertEqual(actual, expected)

    def test_id_lookup(self):
        actual = self.bot.id_lookup(420)['Name']
        expected = 'Godzilla Glue'
        self.assertEqual(actual, expected)

    def test_random(self):
        actual = list(self.bot.random().keys())
        expected = ['_id', 'Name', 'Type', 'Rating', 'Effects', 'Description',
                    'Flavors', 'Nearest']
        self.assertEqual(actual, expected)

    def test_search(self):
        actual = list(self.bot.search('').keys())
        expected = ['_id', 'Name', 'Type', 'Rating', 'Effects', 'Description',
                    'Flavors', 'Nearest']
        self.assertEqual(actual, expected)


if __name__ == '__main__':
    unittest.main()
