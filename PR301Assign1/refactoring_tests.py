import unittest
from validator import Validator
from file_handler import FileHandler


class RefactorTests(unittest.TestCase):

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

    def test_check_field_id(self):
        v = Validator()
        self.assertTrue(v.check_field('EMPID', 'A001'))
        self.assertFalse(v.check_field('EMPID', 'A0501'))

    def test_check_field_gender(self):
        v = Validator()
        self.assertTrue(v.check_field('GENDER', 'M'))
        self.assertTrue(v.check_field('GENDER', 'F'))
        self.assertFalse(v.check_field('GENDER', 'A0501'))

    def test_check_field_age(self):
        v = Validator()
        self.assertTrue(v.check_field('AGE', '21'))
        self.assertFalse(v.check_field('AGE', 21))
        self.assertFalse(v.check_field('AGE', 'A0501'))

    def test_check_field_sales(self):
        v = Validator()
        self.assertTrue(v.check_field('SALES', '221'))
        self.assertFalse(v.check_field('SALES', 'A0501'))

    def test_check_field_bmi(self):
        v = Validator()
        self.assertTrue(v.check_field('BMI', 'Normal'))
        self.assertTrue(v.check_field('BMI', 'Overweight'))
        self.assertTrue(v.check_field('BMI', 'Obesity'))
        self.assertTrue(v.check_field('BMI', 'Underweight'))
        self.assertFalse(v.check_field('BMI', 21))
        self.assertFalse(v.check_field('BMI', 'A0501'))

    def test_check_field_salary(self):
        v = Validator()
        self.assertTrue(v.check_field('SALARY', '12'))
        self.assertTrue(v.check_field('SALARY', '132'))
        self.assertFalse(v.check_field('SALARY', 21))
        self.assertFalse(v.check_field('SALARY', 'A0501'))

    def test_check_field_birthday(self):
        v = Validator()
        self.assertTrue(v.check_field('BIRTHDAY', '1-1-1996'))
        self.assertFalse(v.check_field('BIRTHDAY', 21))
        self.assertFalse(v.check_field('BIRTHDAY', 'A0501'))

    def test_check_all_valid(self):
        v = Validator()
        self.assertTrue(v.check_all({'EMPID': 'A001',
                                     'GENDER': 'F',
                                     'AGE': '21',
                                     'SALES': '001',
                                     'BMI': 'Normal',
                                     'SALARY': '12',
                                     'BIRTHDAY': '1-1-1996'}))

    def test_check_all__id_invalid(self):
        v = Validator()
        self.assertFalse(v.check_all({'EMPID': 'A0e01',
                                     'GENDER': 'F',
                                     'AGE': '21',
                                     'SALES': '001',
                                     'BMI': 'Normal',
                                     'SALARY': '12',
                                     'BIRTHDAY': '1-1-1996'}))

    def test_check_all_gender_invalid(self):
        v = Validator()
        self.assertFalse(v.check_all({'EMPID': 'A001',
                                     'GENDER': 'eF',
                                     'AGE': '21',
                                     'SALES': '001',
                                     'BMI': 'Normal',
                                     'SALARY': '12',
                                     'BIRTHDAY': '1-1-1996'}))

    def test_check_all__age_invalid(self):
        v = Validator()
        self.assertFalse(v.check_all({'EMPID': 'A001',
                                     'GENDER': 'F',
                                     'AGE': 'f21',
                                     'SALES': '001',
                                     'BMI': 'Normal',
                                     'SALARY': '12',
                                     'BIRTHDAY': '1-1-1996'}))

    def test_check_all_sales_invalid(self):
        v = Validator()
        self.assertFalse(v.check_all({'EMPID': 'A001',
                                     'GENDER': 'F',
                                     'AGE': '21',
                                     'SALES': '0f01',
                                     'BMI': 'Normal',
                                     'SALARY': '12',
                                     'BIRTHDAY': '1-1-1996'}))

    def test_check_all__bmi_invalid(self):
        v = Validator()
        self.assertFalse(v.check_all({'EMPID': 'A001',
                                     'GENDER': 'F',
                                     'AGE': '21',
                                     'SALES': '001',
                                     'BMI': 'Nofrmal',
                                     'SALARY': '12',
                                     'BIRTHDAY': '1-1-1996'}))

    def test_check_all_salary_invalid(self):
        v = Validator()
        self.assertFalse(v.check_all({'EMPID': 'A001',
                                     'GENDER': 'F',
                                     'AGE': '21',
                                     'SALES': '001',
                                     'BMI': 'Normal',
                                     'SALARY': '1f2',
                                     'BIRTHDAY': '1-1-1996'}))

    def test_check_all_birthday_invalid(self):
        v = Validator()
        self.assertFalse(v.check_all({'EMPID': 'A001',
                                     'GENDER': 'F',
                                     'AGE': '21',
                                     'SALES': '001',
                                     'BMI': 'Normal',
                                     'SALARY': '12',
                                     'BIRTHDAY': '1-1-19296'}))

suite = unittest.TestLoader().loadTestsFromTestCase(RefactorTests)
unittest.TextTestRunner(verbosity=1).run(suite)
