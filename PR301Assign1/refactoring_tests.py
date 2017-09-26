import unittest
from validator import Validator
from file_handler import FileHandler


class SwitchRefactorTests(unittest.TestCase):

    def test_csv(self):
        fh = FileHandler(Validator())
        actual = fh.open('refactoring/csvTest.csv')[0]
        expected = {'EMPID': 'A001',
                    'GENDER': 'F',
                    'AGE': '21',
                    'SALES': '001',
                    'BMI': 'Normal',
                    'SALARY': '12',
                    'BIRTHDAY': '1-1-1996'}
        self.assertEquals(actual, expected)

    def test_txt(self):
        fh = FileHandler(Validator())
        actual = fh.open('refactoring/txtTest.txt')[0]
        expected = {'EMPID': 'A001',
                    'GENDER': 'F',
                    'AGE': '21',
                    'SALES': '001',
                    'BMI': 'Normal',
                    'SALARY': '12',
                    'BIRTHDAY': '1-1-1996'}
        self.assertEquals(actual, expected)

    def test_xlsx(self):
        fh = FileHandler(Validator())
        actual = fh.open('refactoring/testingdata.xlsx')[0]

        expected = {'EMPID': 'A001',
                    'GENDER': 'F',
                    'AGE': '21',
                    'SALES': '001',
                    'BMI': 'Normal',
                    'SALARY': '12',
                    'BIRTHDAY': '1-1-1996'}
        self.assertEquals(actual, expected)

    def test_invalid(self):
        fh = FileHandler(Validator())
        actual = fh.open('refactoring/csvTest.cs2v')
        expected = False
        self.assertEquals(actual, expected)

suite = unittest.TestLoader().loadTestsFromTestCase(SwitchRefactorTests)
unittest.TextTestRunner(verbosity=2).run(suite)
