import pathlib
import pickle
import json
import re
import os
from datetime import datetime, timedelta, date

# from .classbook import *
# from .clean import *
# from .error_handler import error_handler
# from .model import *
# from .view import *
# from .notes_book import NotesBook

from classbook import *
from clean import *
from error_handler import error_handler
from model import *
from notes_book import NotesBook
from view import *

YES_DECISION = {'y', 'yes', 'нуі', 'н', 'да', 'д'}

NO_DECISION = {'n', 'not', 'no', 'нет', 'тщ', 'тще', 'т'}

EXIT_DECISION = {'exit', 'учше', 'esc', 'close'}


AUTHORIZATION_COMMANDS = {('exit', 'учше', 'esc', 'close', '3'): 'exit',
                          ('load', 'дщфв', '1'): 'load',
                          ('new', 'туц', '2'): 'new'}

GUESS_COMMANDS = {('a', 'ad', 'addd', 'asd', 'asdd', 'sdd', 'adf', 'фів', 'івв',
                   'фівв', 'фввв', 'фва', 'вв', 'ыва', 'фвы', 'фыв', 'явв', 'фв'): 'add',

                  ('chane', 'chnge', 'cange', 'chenge', 'hange', 'chng', 'cchenge', 'chhenge',
                  'cheenge', 'chaange', 'сменить', 'chang', 'срутпу', 'срутп', 'менять', 'изменить',
                   'срфтп', 'рсфтпу', 'срутпу', 'cheng'): 'change',

                  ('fnd', 'ind', 'fid', 'fin', 'faind', 'fand', 'ffind', 'fiind', 'finnd', 'findd',
                   'seek', 'look', 'look for', 'атв', 'афтв', 'штв', 'афт', 'поиск', 'искать',
                   'найти', 'шштв'): 'find',

                  ('&', '?', 'hlp', 'what', 'why', 'where', 'how', 'elp', 'hep', 'hel', 'healp',
                   'halp', 'hhelp', 'heelp', 'hellp', 'helpp', 'рфдз', 'рдз', 'руз', 'руд',
                   'помощь'): 'help',

                  ('вуд', '-', 'del', 'вудуеу', 'вуфдуеу', 'dealete', 'elete', 'elet',
                   'delet', 'dlte', 'dlt', 'lete', 'dealete', 'вудуе', 'удалить',
                   'pop'): 'delete',

                  ('lf', 'birsday', 'bersday', 'bezday', 'bethday', 'birzday', 'bearsday',
                  'birthdey', 'beersday', 'brthday', 'иууксвфн', 'ишквфн', 'др',
                   'рождение', 'бездей', 'бирсдей', 'днюха', 'birthday people', 'birthday boy',
                   'birthday girl', 'birthda', 'birtda', 'birth', 'иуервфн', 'иуівфн',
                   'birt'): 'birthday',

                  ('cleen', 'clan', 'clin', 'cleane', 'cleene', 'klin', 'klean', 'lean', 'clen',
                   'kleen', 'суф', 'лдуут', 'лдуфт', 'сдуфту', 'клн', 'клин', 'разобрать',
                   'мусор'): 'clean',

                  ('ырща', 'ырщцу', 'showe', 'schow', 'schove', 'chov', 'shove', 'schov',
                   'schowe', 'how', 'sho', 'shouv', 'шов', 'ірщцу', 'показать', 'рщц',
                   'ірщм'): 'show'}


class Controller:

    def __init__(self):
        self.model = Model('')
        self.view = ConsoleView()

    @error_handler
    def add(self):
        # Ввод имени
        self.view.notify_of_message(100*'_')
        name = self.view.input_name()
        if name in EXIT_DECISION:
            self.view.esc_e = False
            self.view.notify_of_message("Not saved")
            return None
        # определение ID
        if len(self.model.book) > 0:
            id_n = self.model.book[-1]["Id"]+1
        else:
            id_n = 1
        record1 = Record(name, id_n)

        while True:
            # ввод телефона
            decision = self.view.ask_to_add_field('phone-number')

            if decision in YES_DECISION:
                phone = self.view.input_phone()
                # валидация телефона
                if record1.validate_phone(phone):
                    record1.add_phone(phone)
                else:
                    self.view.notify_of_message(
                        'Wrong input! Phone may start with + and has from 3 to 12 digits max. Example +380501234567')

            elif decision in EXIT_DECISION:
                self.model.book.add_record(record1.user)
                self.view.esc_e = False
                self.view.say_buy()
                return None
            elif decision in NO_DECISION:
                break
            else:
                self.view.notify_of_message('Wrong input!')

        while True:
            # ввод дня рождения
            decision = self.view.ask_to_add_field('Birthday')

            if decision in YES_DECISION:

                birthday = self.view.input_birthday()
                if record1.validate_birthday(birthday):
                    record1.add_birthday(birthday)
                    break
                else:
                    self.view.notify_of_message(
                        'Wrong Birthday. Expected day.month.year. Format: dd.mm.yyyy (Example:25.12.1970)')

            elif decision in EXIT_DECISION:
                self.model.book.add_record(record1.user)
                self.view.esc_e = False
                self.view.say_buy()
                return None

            elif decision in NO_DECISION:
                break

            else:
                self.view.notify_of_message('Wrong input!')

        while True:
            # ввод адреса
            decision = self.view.ask_to_add_field('address')

            if decision in YES_DECISION:
                address = self.view.input_address()
                # валидация адреса
                if record1.validate_address(address):
                    record1.user['Address'] = address
                    break
                else:
                    self.view.notify_of_message(
                        f'Your Address is {len(address)} symbols. Please no more than 30 symbols')
            elif decision in EXIT_DECISION:
                self.model.book.add_record(record1.user)
                self.view.esc_e = False
                self.view.say_buy()
                return None

            elif decision in NO_DECISION:
                break
            else:
                self.view.notify_of_message('Wrong input!')

        while True:
            # ввод ємейла
            decision = self.view.ask_to_add_field('e-mail')

            if decision in YES_DECISION:
                email = self.view.input_email()
                # валидация ємейла
                if record1.validate_email_format(email):
                    if record1.validate_email_duration(email):
                        record1.user['E-mail'] = email
                        break
                    else:
                        self.view.notify_of_message(
                            f'Your E-mail is {len(email)} symbols. Please no more than 30 symbols')
                else:
                    self.view.notify_of_message(
                        'Format is wrong. Try again in format: your_nickname@something.domen_name')

            elif decision in EXIT_DECISION:
                self.model.book.add_record(record1.user)
                self.view.esc_e = False
                self.view.say_buy()
                return None

            elif decision in NO_DECISION:
                break

            else:
                self.view.notify_of_message('Wrong input!')

        while True:
            # ввод ТЄГА
            decision = self.view.ask_to_add_field('tags')
            if decision in YES_DECISION:
                tags = self.view.input_tags()
                # валидация тегов
                if record1.validate_tags(tags):
                    record1.user['Tags'] = tags
                else:
                    self.view.notify_of_message(
                        f'Your Tags is {len(tags)} symbols. Please no more than 15 symbols')

            elif decision in EXIT_DECISION:
                self.model.book.add_record(record1.user)
                self.view.esc_e = False
                self.view.say_buy()
                return None

            elif decision in NO_DECISION:
                break
            else:
                self.view.notify_of_message('Wrong input!')

        self.model.book.add_record(record1.user)
        self.save()
        return None

    @error_handler
    def change(self):
        # определяем id контакта что надо изменить
        self.view.notify_of_message(100*'_')
        find_v = self.view.input_name(
            message="Put Name, you want to change")
        find_v = find_v.lower()
        result = self.model.book.find_value(find_v)

        if len(result) == 1:
            for i in result:
                edited_id = i["Id"]
        elif len(result) > 1:
            # если найдены несколько результатов поиска
            self.view.notify_of_message(
                f"I've found {len(result)} notes with this Name")
            self.show_find(result)
            # ввод id для изменения
            edited_id = self.view.input_id(
                message='Please enter Id of contact that you want to change')
        else:
            self.view.notify_of_message(
                f"The contact with name {find_v.upper()} is not found")
            return None
        # изменение контакта с определенным id = edited_id
        for contact in self.model.book:
            if contact['Id'] == edited_id:
                self.view.notify_of_message(
                    "You are editing the following contact:")
                print(contact)

                record = Record(contact['Name'], edited_id, contact['Phones'],
                                contact['Birthday'], contact['Address'], contact['E-mail'], contact['Tags'])
                record.user['Phones'] = contact['Phones']

                fields = {1: 'Name', 2: 'Phones', 3: 'Birthday',
                          4: 'Address', 5: 'E-mail', 6: 'Tags'}

                inputing_command = {1: self.view.input_name,
                                    2: self.view.input_phone,
                                    3: self.view.input_birthday,
                                    4: self.view.input_address,
                                    5: self.view.input_email,
                                    6: self.view.input_tags}

                changed_field = self.view.input_field_to_edit()

                field_value = inputing_command[changed_field]()

                if changed_field == 1:  # Name
                    record.user[fields[changed_field]] = field_value
                elif changed_field == 2:  # Phones
                    record.phones = []
                    record.add_phone(field_value)
                elif changed_field == 3:  # Birthday
                    record.add_birthday(field_value)
                elif changed_field == 4:  # address
                    record.add_address(field_value)
                elif changed_field == 5:  # Email
                    record.add_email(field_value)
                elif changed_field == 6:  # Tag
                    record.user[fields[changed_field]] = field_value
                break

        # удаление изменяемого контакта
        self.model.book.remove(contact)
        # добавление обновленного контакта
        self.model.book.add_record(record.user)
        self.save()

    @error_handler
    def clean_folder(self):
        user_input = self.view.enter_path_for_clean_lolder()
        path = pathlib.Path(user_input)
        CleanFolder().print_recursive(path, user_input)
        CleanFolder().delete_dir(user_input)
        self.view.notify_of_message(
            'Everything done! Please check your folder!')

    @error_handler
    def birthday(self):

        self.view.notify_of_message(100*'_')
        decision = self.view.input_birthday_search_type()
        result = []

        if decision == 1:
            n = self.view.input_for_birthday_1()
            bday, result = self.model.book.find_persons_with_birthday_in_n_days(
                n)
            if result:
                self.view.notify_of_message(
                    f'On {bday} you need to congratulate {len(result)} people from your Addressbook')
                self.show_find(result)
            else:
                self.view.notify_of_message(
                    f'You need to congratulate noone on {bday}')

        elif decision == 2:
            n = self.view.input_for_birthday_2()
            result = self.model.book.find_persons_with_birthday_during_n_days(
                n)
            if len(result) > 0:
                print(
                    f'In future {n} days you need to congratulate {len(result)} people from your Addressbook')
                self.show_find(result)
            else:
                print(
                    f'In future {n} days nobody from your Addressbook will have birthday')

        elif decision == 3:
            name = self.view.input_for_birthday_3()
            result = self.model.book.find_persons_birthday(name)
            if result:
                self.view.print_persons_and_their_birthday(result)
            else:
                self.view.notify_of_message(
                    'No information about birthday. Please enter valid information using command "change" or add new person to Addressbook')

        elif decision == 4 or decision in EXIT_DECISION:
            self.view.esc_e = False
            self.view.say_buy()

        else:
            self.view.notify_of_message('This Name is not found!')

    @error_handler
    def delete(self):
        self.view.notify_of_message(100*'_')
        find_v = self.view.input_name(
            message="Put Name, you want to find and delete from your addressbook")
        find_v = find_v.lower()
        result = self.model.book.find_value(find_v)

        if len(result) == 1:
            for i in result:
                if i["Name"].lower() == find_v:
                    self.model.book.remove(i)
                    self.view.notify_of_message(f"You've deleted {find_v}")
                    self.save()
        elif len(result) > 1:
            # если найдены несколько результатов поиска
            self.view.notify_of_message(
                f"I've found {len(result)} notes with this Name")
            self.show_find(result)
            # ввод id для удаления
            del_input = self.view.input_id()
            # удаление
            for i in self.model.book:
                if i["Id"] == del_input:
                    self.model.book.remove(i)
                    self.view.notify_of_message(
                        f"You've deleted {find_v.upper()}")
                    self.model.save_books()
        else:
            self.view.notify_of_message(
                f"The contact with name {find_v.upper()} is not found")

    @error_handler
    def find(self):
        self.view.notify_of_message(100*'_')
        find_v = self.view.input_name(
            message="Put word, half of word or digits you want to find")
        result = self.model.book.find_value(find_v)
        self.view.notify_of_message("I've found following:")
        self.show_find(result)

    @error_handler
    def show_find(self, result):
        # выводит результаты поиска по объекту класса AdressBook
        number = len(result)
        iter = result.iterator(number)
        for i in iter:
            self.view.show_one_page_of_addressbook(i)

    @error_handler
    def exit(self):
        self.model.save_books()
        self.view.esc_e = False
        self.view.say_buy()

    @error_handler
    def save(self):
        self.model.save_books()

    @error_handler
    def show(self):
        number = self.view.enter_number_of_page()
        iter = self.model.book.iterator(number)

        for i in iter:
            self.view.show_one_page_of_addressbook(i)

        self.view.notify_of_message("The end of the contacts book")

    ##############################################################
    # Команды для Handler для работы с NotesBook

    @error_handler
    def add_note(self):
        text, hashtag = self.view.add_note()
        self.model.notes_book.add_note(text, hashtag)
        self.view.notify_of_message("Your note is successfully saved")

    @error_handler
    def delete_note(self):
        hashtag = self.view.delete_note()
        self.model.notes_book.delete_note(hashtag)
        self.view.notify_of_message(
            f"The note with hashtag '{hashtag}' is deleted")

    @error_handler
    def edit_note(self):
        hashtag = self.view.input_hashtag_to_edit_notes()
        for note in self.model.notes_book:
            if note[0] == hashtag:
                # находим нужную заметку с заданным ключевым словом
                # и изменяем текст заметки
                new_note = self.view.edit_note(note)
                self.model.notes_book.edit_note(new_note)
                self.view.notify_of_message(
                    f'The note with tag {new_note[0].upper()} is edited')

    @error_handler
    def find_note(self):
        keyword = self.view.find_note()
        result = self.model.notes_book.find_note(keyword)
        print(result)
        if result:
            self.view.print_notes_book(result)
            self.view.notify_of_message("The search is sucessfully finished")
        else:
            self.view.notify_of_message("Keyword is not found")

    @error_handler
    def sort_notes(self):
        search_type = self.view.sort_notes()
        self.view.print_notes_book(
            self.model.notes_book.sort_notes(search_type))

    @error_handler
    def show_notes(self):
        self.view.notify_of_message('Your Notes Book:')
        self.view.print_notes_book(self.model.notes_book)

    # Конец конец команд для NotesBook
    @error_handler
    def help_func(self):
        self.view.help()

    @error_handler
    def handler(self, user_inpu):

        COMMANDS = {'add': self.add, 'ad': self.add, '+': self.add, 'фвв': self.add, 'change': self.change, 'срфтпу': self.change, 'close': self.exit, 'exit': self.exit, 'учше': self.exit,
                    'find': self.find, 'аштв': self.find, 'help': self.help_func, 'рудз': self.help_func, 'хелп': self.help_func, 'save': self.save, 'іфму': self.save, 'ыфму': self.save, 'show': self.show, 'ырщц': self.show, 'ірщц': self.show,
                    'delete': self.delete, 'del': self.delete, 'вуд': self.delete, 'вудуеу': self.delete, 'birthday': self.birthday, 'ишкервфн': self.birthday, 'clean': self.clean_folder, 'сдуфт': self.clean_folder,
                    'add note': self.add_note, 'фвв тщеу': self.add_note, 'delete note': self.delete_note, 'вудуеу тщеу': self.delete_note, 'edit note': self.edit_note, 'увше тщеу': self.edit_note,
                    'find note': self.find_note, 'аштв тщеу': self.find_note, 'sort notes': self.sort_notes, 'ыщке тщеуы': self.sort_notes, 'show notes': self.show_notes, 'ырщц тщеуы': self.show_notes}

        if user_inpu in COMMANDS.keys():
            # если ввод команды понятный:
            return COMMANDS[user_inpu]()
        else:
            # если ввод команды не понятен - мы уточняем у пользователядщф
            for key, value in GUESS_COMMANDS.items():
                if user_inpu in key:
                    guess_command = value
                    if self.view.clarify_command(guess_command):
                        return COMMANDS[guess_command]()
            return self.view.notify_of_error()
