from __future__ import print_function
from file_reader import *


class FileHandler:
    def __init__(self, new_validator):
        self.validator = new_validator
        self.file_types = {'.csv': CSVReader(self.validator),
                           '.txt': TXTReader(self.validator),
                           '.xlsx': XLSXReader(self.validator)}

    def open(self, file_path):
        file_extension = re.search(r'\..+$', file_path).group()
        if file_extension in self.file_types:
            return self.file_types[file_extension].read_file(file_path)
        else:
            print('Invalid file extension', file=sys.stderr)
            return False


    # Rosemary
    def open_help(self, help_command):
        """
        >>> f = FileHandler(new_validator=Validator)
        >>> print(f.open_help('line'))
        line command vitualize the data.
        >>> print(f.open_help('help'))
        help command brings out all command.
        >>> print(f.open_help('helpp'))
        No such command.
        """
        try:
            file = open("help.txt", "r")
            for line in file:
                if len(line.split("=")) == 2:
                    entries = line.split("=")
                    if help_command == entries[0]:
                        return entries[1].rstrip('\n')
                else:
                    print("Invalid help file format!")
        except FileNotFoundError:
            print('The help file was not found', file=sys.stderr)
        return "No such command."

