from abc import ABCMeta, abstractmethod
import sys
import csv
import re
import openpyxl
from validator import Validator

class FileReader(metaclass=ABCMeta):
    @abstractmethod
    def read_file(self, filename):
        pass


class CSVReader(FileReader):
    def __init__(self, new_validator):
        self.validator = new_validator

    def read_file(self, filename):
        """
        >>> f = CSVReader(Validator())
        >>> result = f.read_file("data.csv")
        >>> print(result[0]['EMPID'])
        A001
        >>> print(result[0]['GENDER'])
        F
        >>> print(result[0]['AGE'])
        21
        >>> print(result[0]['SALES'])
        001
        >>> print(result[0]['BMI'])
        Normal
        >>> print(result[0]['BIRTHDAY'])
        1-1-1996
        >>> print(result[0]['SALARY'])
        12
        """
        try:
            with open(filename) as f_obj:
                reader = csv.DictReader(f_obj, delimiter=',')
                the_list = []
                for line in reader:
                    employee = dict()
                    employee["EMPID"] = str(line["emp_id"])
                    employee["GENDER"] = str(line["gender"])
                    employee["AGE"] = str(line["age"])
                    employee["SALES"] = str(line["sales"])
                    employee["BMI"] = str(line["bmi"])
                    employee["SALARY"] = str(line["salary"])
                    employee["BIRTHDAY"] = str(line["birthday"])

                    if self.validator.check_line(employee):
                        the_list.append(employee)
                    else:
                        print('Entry failed validation', file=sys.stderr)
                if self.validator.check_data_set(the_list):
                    return the_list
                else:
                    print("There were no valid entries in the file", file=sys.stderr)
                    return False
        except FileNotFoundError:
            print('The file was not found', file=sys.stderr)
            return False


class TXTReader(FileReader):
    def __init__(self, new_validator):
        self.validator = new_validator

    def read_file(self, filename):
        try:
            file = open(filename, "r")
        except FileNotFoundError:
            print('The file was not found', file=sys.stderr)
            return False
        the_list = []
        for line in file:
            dictionary = {}
            entries = line.split(";")
            for entry in entries:
                if len(entry.split("=")) == 2:
                    key = entry.split("=")[0]
                    value = entry.split("=")[1]
                    value = value.rstrip('\n')
                    dictionary[key] = value
                else:
                    print('The file was in an invalid format', file=sys.stderr)
                    return False
            if self.validator.check_line(dictionary):
                the_list.append(dictionary)
            else:
                print('Entry failed validation', file=sys.stderr)
        if self.validator.check_data_set(the_list):
            return the_list
        else:
            print("There were no valid entries in the file", file=sys.stderr)
            return False


class XLSXReader(FileReader):
    def __init__(self, new_validator):
        self.validator = new_validator

    def read_file(self, filename):
        """
        >>> f = XLSXReader(Validator())
        >>> result = f.read_file("testingdata.xlsx")
        >>> print(result[0]['EMPID'])
        A001
        >>> print(result[0]['GENDER'])
        F
        >>> print(result[0]['AGE'])
        21
        >>> print(result[0]['SALES'])
        001
        >>> print(result[0]['BMI'])
        Normal
        >>> print(result[0]['BIRTHDAY'])
        1-1-1996
        >>> print(result[0]['SALARY'])
        12
        """
        try:
            wb = openpyxl.load_workbook(filename)
            sheet = wb.active
            the_list = []
            for x in range(1, 29):
                employee = dict()
                employee["EMPID"] = str(sheet.cell(column=1, row=x).value)
                employee["GENDER"] = str(sheet.cell(column=2, row=x).value)
                employee["AGE"] = str(sheet.cell(column=3, row=x).value)
                employee["SALES"] = str(sheet.cell(column=4, row=x).value)
                employee["BMI"] = str(sheet.cell(column=5, row=x).value)
                employee["SALARY"] = str(sheet.cell(column=6, row=x).value)
                employee["BIRTHDAY"] = str(sheet.cell(column=7, row=x).value)
                if self.validator.check_line(employee):
                    the_list.append(employee)
                else:
                    print('Entry failed validation', file=sys.stderr)
            if self.validator.check_data_set(the_list):
                return the_list
            else:
                print("There were no valid entries in the file", file=sys.stderr)
                return False
        except FileNotFoundError:
            print("File not found!", file=sys.stderr)
            return False

if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=1)
