import pathlib
import pickle

# from .classbook import *
# from .notes_book import NotesBook

from classbook import *
from notes_book import NotesBook


class Model:
    def __init__(self, path):
        self.book = AddressBook()
        self.notes_book = NotesBook()
        self.path = path

    def load_books(self):
        with open(self.path, 'rb') as fh:
            self.book = pickle.load(fh)
            self.notes_book = pickle.load(fh)

    def save_books(self):
        with open(self.path, 'wb') as fh:
            pickle.dump(self.book, fh)
            pickle.dump(self.notes_book, fh)
