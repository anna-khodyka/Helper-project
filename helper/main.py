import pathlib
import pickle
import json
import re
import os
from datetime import datetime, timedelta, date

# from .classbook import *
# from .clean import *
# from .controller import *
# from .error_handler import error_handler
# from .model import *
# from .view import *
# from .notes_book import NotesBook

from classbook import *
from clean import *
from controller import *
from error_handler import error_handler
from model import *
from notes_book import NotesBook
from view import *


@error_handler
def main():
    controller = Controller()
    view = ConsoleView()
    controller.view = view
    view.greete()
    while True:
        command = view.register_or_authorize()

        for key in AUTHORIZATION_COMMANDS:
            if command in key:
                command = AUTHORIZATION_COMMANDS[key]

        if command == 'load':
            path = view.authorize()
            model = Model(path)  # создаем обїект с заданым значением пути
            controller.model = model
            try:
                model.load_books()
                break
            except:
                view.notify_of_message('Please write the right path to file!')

        elif command == 'new':
            path = view.register()
            model = Model(path)
            controller.model = model
            break

        elif command == 'exit':
            view.esc_e = False
            break
        else:
            view.notify_of_error()

    # выполнение основных комманд HELPER-a
    while view.esc_e:
        user_inpu = view.choose_command()
        result = controller.handler(user_inpu)
        if result:
            print(result)
        elif result == None:
            pass
        else:
            break


if __name__ == '__main__':
    main()
