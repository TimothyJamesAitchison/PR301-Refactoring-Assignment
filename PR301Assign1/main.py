from command import Command
from file_handler import FileHandler
from validator import Validator
from view import View
from db import DatabaseHandler
import pickle
import sys

# hasitha
try:
    database_name = sys.argv[1]
except IndexError:
    database_name = "db"
try:
    database = pickle.load(open(database_name + ".p", "rb"))
except FileNotFoundError:
    database = DatabaseHandler(Validator(), database_name)
    database.load()
    try:
        pickle.dump(database, open(database_name+".p", "wb"))
    except TypeError:
        pass
except EOFError:
    database = DatabaseHandler(Validator(), database_name)
    database.load()
    try:
        pickle.dump(database, open(database_name+".p", "wb"))
    except TypeError:
        pass
view = View()
cli = Command(FileHandler(Validator()), database, view)
cli.cmdloop()
