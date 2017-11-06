from __future__ import print_function
import plotly
import plotly.graph_objs
import pygal
import sys
from abc import abstractmethod, ABCMeta


class Observer(metaclass=ABCMeta):
    def __init__(self):
        self.subject = None

    @abstractmethod
    def update(self):
        pass

    def set_subject(self, subject):
        self.subject = subject


class View(Observer):
    def __init__(self):
        Observer.__init__(self)
        self.employees = []

    def update(self):
        self.employees = self.subject.get_state()

    def display(self):
        count = 0
        for employee in self.employees:
            count += 1
            print("======== Employee {0} ==========".format(count))
            for key in employee:
                print("{0} = {1}".format(key, employee[key]))

    # Tim
    @staticmethod
    def plot_bar(data):
        values = []
        keys = []
        for employee in data:
            keys.append(employee[0])
            print(employee[0])
            values.append(employee[1])
            print(employee[1])
        chart = {"data": [plotly.graph_objs.Bar(x=keys, y=values)]}
        plotly.offline.plot(chart)

    # Tim
    @staticmethod
    def plot_pie_gender(data):
        males = 0
        females = 0
        others = 0
        for employee in data:
            if employee[1] == "M":
                males += 1
            elif employee[1] == "F":
                females += 1
            else:
                others += 1

        fig = {
            'data': [{'labels': ['Male', 'Female', 'Other'],
                      'values': [males, females, others],
                      'type': 'pie'}],
            'layout': {
                'title': 'Gender diversity in organisation'}
        }

        plotly.offline.plot(fig)

    # Hasitha
    @staticmethod
    def pygal_line_salebased(sales, ages):
        data_points = []
        sales = dict(sales)
        ages = dict(ages)
        for employee in sales:
            data_point = (ages[employee], sales[employee])
            data_points.append(data_point)
        xy_chart = pygal.XY(stroke=False)
        xy_chart.title = 'Correlction between Sales and Age'
        xy_chart.add('Sales', data_points)
        # Tim
        try:
            xy_chart.render_in_browser()
        except ImportError:
            print('Could not display chart on this computer as does not have lxml installed', file=sys.stderr)

    # Rosemary
    # age vs salary
    @staticmethod
    def age_salary(ages, salarys):
        data_points = []
        ages = dict(ages)
        salarys = dict(salarys)
        for employee in ages:
            data_point = (salarys[employee], ages[employee])
            data_points.append(data_point)
        xy_chart = pygal.XY(stroke=False)
        xy_chart.title = 'Correlction between Ages and Sales'
        xy_chart.add('Ages', data_points)
        # Tim
        try:
            xy_chart.render_in_browser()
        except ImportError:
            print('Could not display chart on this computer as does not have lxml installed', file=sys.stderr)
