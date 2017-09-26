from __future__ import print_function
import sys
from abc import ABCMeta, abstractmethod
import datetime as date
from rule_checker import RuleChecker


# Tim
class IFileValidator(metaclass=ABCMeta):
    @abstractmethod
    def check_data_set(self, data_set):
        pass

    @abstractmethod
    def check_line(self, employee_attributes):
        pass

    @abstractmethod
    def check_all(self, employee_attributes):
        pass

    @abstractmethod
    def check_id(self, emp_id):
        pass

    @abstractmethod
    def check_age(self, age):
        pass

    @abstractmethod
    def check_sales(self, sales):
        pass

    @abstractmethod
    def check_bmi(self, bmi):
        pass

    @abstractmethod
    def check_salary(self, salary):
        pass

    @abstractmethod
    def check_birthday(self, birthday):
        pass

    @abstractmethod
    def check_gender(self, gender):
        pass

    @abstractmethod
    def check_birthday_against_age(self, birthday, age):
        pass


class Validator(IFileValidator):

    # Tim
    def __init__(self):
        self.rules = RuleChecker()
        self.rules.add_rule('EMPID', "^[A-Z][0-9]{3}$")
        self.rules.add_rule('GENDER', "^(M|F)$")
        self.rules.add_rule('AGE', "^[0-9]{2}$")
        self.rules.add_rule('SALES', "^[0-9]{3}$")
        self.rules.add_rule('BMI', "^(Normal|Overweight|Obesity|Underweight)$")
        self.rules.add_rule('SALARY', "^[0-9]{2,3}$")
        self.rules.add_rule('BIRTHDAY', "^[1-31]-[1-12]-[0-9]{4}$")

        self.attributes = self.rules.get_fields()
        self.number_of_attributes = len(self.attributes)

    # Tim
    def check_data_set(self, data_set):
        # Should be of form [{EMPID: B12, GENDER: M, AGE: 22, etc}, {EMPID: 55Y, GENDER: F, etc}]
        if len(data_set) == 0:
            print('The data was empty', file=sys.stderr)
            return False
        else:
            for employee in data_set:
                if not self.check_line(employee):
                    print('One or more of the lines of data was invalid', file=sys.stderr)
                    return False
        # Failing to invalidate is a success
        return True

    # Tim
    def check_line(self, employee_attributes):
        # Should be of form {EMPID: B12, GENDER: M, AGE: 22, etc}
        for attribute in self.attributes:
            if attribute not in employee_attributes:
                print('Missing attribute: {}'.format(attribute), file=sys.stderr)
                return False
        try:
            if not self.check_all(employee_attributes):
                return False
        except TypeError:
            print('The data was not bundled correctly', file=sys.stderr)
            return False
        # Failing to invalidate is a success
        return True

    # Rosemary
    def check_all(self, employee_attributes):
        for attribute in employee_attributes:
            if not self.check_field(attribute, employee_attributes[attribute]):
                return False
        return True

    # Rosemary
    def check_id(self, emp_id):
        # Tim
        """
        >>> v = Validator()
        >>> v.check_id('M000')
        True
        >>> v.check_id('F999')
        True
        >>> v.check_id('m000')
        False
        >>> v.check_id('F9999')
        False
        >>> v.check_id('MMMM')
        False
        >>> v.check_id('0000')
        False
        >>> v.check_id('000')
        False
        >>> v.check_id('M00')
        False
        >>> v.check_id(None)
        False
        >>> v.check_id(1)
        False
        >>> v.check_id(True)
        False
        >>> v.check_id({'M00'})
        False
        """
        return self.check_field("EMPID", emp_id)

    # Tim
    def check_age(self, age):
        return self.check_field("AGE", age)

    # Hasitha
    def check_gender(self, gender):
        # Tim
        """
        >>> v = Validator()
        >>> v.check_gender('M')
        True
        >>> v.check_gender('F')
        True
        >>> v.check_gender('MF')
        False
        >>> v.check_gender('m')
        False
        >>> v.check_gender('f')
        False
        >>> v.check_gender(1)
        False
        >>> v.check_gender(True)
        False
        >>> v.check_gender(None)
        False
        """
        return self.check_field("GENDER", gender)

    # Rosemary
    def check_sales(self, sales):
        # Tim
        """
        >>> v = Validator()
        >>> v.check_sales(-1)
        False
        >>> v.check_sales('000')
        True
        >>> v.check_sales('001')
        True
        >>> v.check_sales(2.5)
        False
        >>> v.check_sales('999')
        True
        >>> v.check_sales('1000')
        False
        >>> v.check_sales("1")
        False
        >>> v.check_sales(1)
        False
        >>> v.check_sales(999)
        False
        """
        return self.check_field("SALES", sales)

    # Hasitha
    def check_bmi(self, bmi):
        return self.check_field("BMI", bmi)

    # Hasitha
    def check_salary(self, salary):
        return self.check_field("SALARY", salary)

    # Tim
    def check_birthday(self, birthday):
        try:
            day_month_year = birthday.split("-")
            day = int(day_month_year[0])
            month = int(day_month_year[1])
            year = int(day_month_year[2])
            date.datetime(year, month, day)
            return True
        except ValueError:
            print('The date was invalid', file=sys.stderr)
            return False
        except AttributeError:
            print('The date was in an invalid format', file=sys.stderr)
            return False

    def check_field(self, field, value):
        try:
            if not self.rules.check_field(field, value):
                print('{0} is invalid {1}!'.format(value, field), file=sys.stderr)
                return False
        except TypeError:
            return False
        else:
            return True

    # Tim
    def check_birthday_against_age(self, birthday, age):
        # Tim
        """
        >>> v = Validator()
        >>> v.check_birthday_against_age('19-06-1988', 28)
        False
        >>> v.check_birthday_against_age('19-06-1988', 29)
        True
        >>> v.check_birthday_against_age('19-06-1988', 30)
        False
        >>> v.check_birthday_against_age('19-12-1988', 27)
        False
        >>> v.check_birthday_against_age('19-12-1988', 28)
        True
        >>> v.check_birthday_against_age('19-12-1988', 29)
        False
        >>> v.check_birthday_against_age('19-12-1988', 30)
        False
        """
        if not self.check_birthday(birthday):
            return False
        else:
            day_month_year = birthday.split("-")
            day = int(day_month_year[0])
            month = int(day_month_year[1])
            year = int(day_month_year[2])
            # adding age because we just want to compare month and day
            birth = date.datetime(year, month, day)
            today = date.datetime.today()
            if birth.month < today.month:
                # Had a birthday already this year
                return int(age) == today.year - year
            elif birth.month == today.month and birth.day < today.day:
                # Had a birthday already this year (this month)
                return int(age) == today.year - year
            else:
                # Hasn't had a birthday yet this year.
                return int(age) == today.year - year - 1

    # Tim
    def check_in_attributes(self, query_attribute):
        # Tim
        """
        >>> v = Validator()
        >>> v.check_in_attributes("EMPID")
        True
        >>> v.check_in_attributes("GENDER")
        True
        >>> v.check_in_attributes("AGE")
        True
        >>> v.check_in_attributes("SALES")
        True
        >>> v.check_in_attributes("BMI")
        True
        >>> v.check_in_attributes("SALARY")
        True
        >>> v.check_in_attributes("BIRTHDAY")
        True
        >>> v.check_in_attributes("Salary")
        True
        >>> v.check_in_attributes("SALE")
        False
        >>> v.check_in_attributes(1)
        False
        """
        try:
            return query_attribute.upper() in self.attributes
        except AttributeError:
            return False

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=0)
