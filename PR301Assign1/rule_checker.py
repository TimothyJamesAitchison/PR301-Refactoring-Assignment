import re


class RuleChecker:
    def __init__(self):
        self.my_rules = {}

    def add_rule(self, field, expression):
        self.my_rules[field] = expression

    def check_field(self, field, value):
        if field in self.my_rules:
            return re.match(self.my_rules[field], value)

    def get_fields(self):
        return self.my_rules.keys()