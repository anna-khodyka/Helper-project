import pathlib
import pickle
import json
import re
import os
from datetime import datetime, timedelta, date

# from .classbook import *
# from .clean import *
# from .model import *
# from .view import *
# from .notes_book import NotesBook

from classbook import *
from clean import *
from model import *
from notes_book import NotesBook
from view import *


def error_handler(func):
    def inner(*args):
        try:
            return func(*args)
        except:
            return view.notify_of_error()

    return inner


# @error_handler
def main():  # main относится к контроллеру!
    global view, model
    view = ConsoleView()

    view.greete()
    while True:
        command = view.register_or_authorize()

        for key in AUTHORIZATION_COMMANDS:
            if command in key:
                command = AUTHORIZATION_COMMANDS[key]

        if command == 'load':
            path = view.authorize()
            model = Model(path)  # создаем обїект с заданым значением пути
            try:
                model.load_books()
                break
            except:
                view.notify_of_message('Please write the right path to file!')

        elif command == 'new':
            path = view.register()
            model = Model(path)
            break

        elif command == 'exit':
            view.esc_e = False
            break
        else:
            view.notify_of_error()

    # выполнение основных комманд HELPER-a
    while view.esc_e:
        user_inpu = view.choose_command()
        result = handler(user_inpu)
        if result:
            print(result)
        elif result == None:
            pass
        else:
            break


# @error_handler
def add():
    # Ввод имени
    view.notify_of_message(100*'_')
    name = view.input_name()
    if name in EXIT_DECISION:
        view.esc_e = False
        view.notify_of_message("Not saved")
        return None
    # определение ID
    if len(model.book) > 0:
        id_n = model.book[-1]["Id"]+1
    else:
        id_n = 1
    record1 = Record(name, id_n)

    while True:
        # ввод телефона
        decision = view.ask_to_add_field('phone-number')

        if decision in YES_DECISION:
            phone = view.input_phone()
            # валидация телефона
            if record1.validate_phone(phone):
                record1.add_phone(phone)
            else:
                view.notify_of_message(
                    'Wrong input! Phone may start with + and has from 3 to 12 digits max. Example +380501234567')

        elif decision in EXIT_DECISION:
            model.book.add_record(record1.user)
            view.esc_e = False
            view.say_buy()
            return None
        elif decision in NO_DECISION:
            break
        else:
            view.notify_of_message('Wrong input!')

    while True:
        # ввод дня рождения
        decision = view.ask_to_add_field('Birthday')

        if decision in YES_DECISION:

            birthday = view.input_birthday()
            if record1.validate_birthday(birthday):
                record1.add_birthday(birthday)
                break
            else:
                view.notify_of_message(
                    'Wrong Birthday. Expected day.month.year. Format: dd.mm.yyyy (Example:25.12.1970)')

        elif decision in EXIT_DECISION:
            model.book.add_record(record1.user)
            view.esc_e = False
            view.say_buy()
            return None

        elif decision in NO_DECISION:
            break

        else:
            view.notify_of_message('Wrong input!')

    while True:
        # ввод адреса
        decision = view.ask_to_add_field('address')

        if decision in YES_DECISION:
            address = view.input_address()
            # валидация адреса
            if record1.validate_address(address):
                record1.user['Address'] = address
                break
            else:
                view.notify_of_message(
                    f'Your Address is {len(address)} symbols. Please no more than 30 symbols')
        elif decision in EXIT_DECISION:
            model.book.add_record(record1.user)
            view.esc_e = False
            view.say_buy()
            return None

        elif decision in NO_DECISION:
            break
        else:
            view.notify_of_message('Wrong input!')

    while True:
        # ввод ємейла
        decision = view.ask_to_add_field('e-mail')

        if decision in YES_DECISION:
            email = view.input_email()
            # валидация ємейла
            if record1.validate_email_format(email):
                if record1.validate_email_duration(email):
                    record1.user['E-mail'] = email
                    break
                else:
                    view.notify_of_message(
                        f'Your E-mail is {len(email)} symbols. Please no more than 30 symbols')
            else:
                view.notify_of_message(
                    'Format is wrong. Try again in format: your_nickname@something.domen_name')

        elif decision in EXIT_DECISION:
            model.book.add_record(record1.user)
            view.esc_e = False
            view.say_buy()
            return None

        elif decision in NO_DECISION:
            break

        else:
            view.notify_of_message('Wrong input!')

    while True:
        # ввод ТЄГА
        decision = view.ask_to_add_field('tags')
        if decision in YES_DECISION:
            tags = view.input_tags()
            # валидация тегов
            if record1.validate_tags(tags):
                record1.user['Tags'] = tags
            else:
                view.notify_of_message(
                    f'Your Tags is {len(tags)} symbols. Please no more than 15 symbols')

        elif decision in EXIT_DECISION:
            model.book.add_record(record1.user)
            view.esc_e = False
            view.say_buy()
            return None

        elif decision in NO_DECISION:
            break
        else:
            view.notify_of_message('Wrong input!')

    model.book.add_record(record1.user)
    save()
    return None

# @error_handler


def change():
    pass
    # для дальнейшего рефакторинга#####################

    # print(100*"_")
    # say = 'Successfully changed'
    # print('Type name of record you want to change')
    # old_name = str(input())
    # old_name = old_name.lower()
    # result = model.book.find_value(old_name)

    # if len(result) > 0 and len(result) != None:
    #     show_find(result)

    #     print(100*"_")
    #     print('1.   To change Name: type "name".\n2.   To change Phone: type "phone".\n3.   To change Birthday: type "birthday".\n4.   To change Address: type "address".\n5.   To change E-mail: type "email".\n6.   To change Tags: type "tags"\n7.   To exit: type "exit".\n')
    #     decision = str(input())
    #     decision = decision.lower()

    #     if decision == 'name' or decision == 'тфьу' or decision == '1':
    #         print('Type new name')
    #         new_name = str(input())

    #         if len(result) > 1:
    #             print(f"I've found {len(result)} notes with this Name")
    #             show_find(result)
    #             print('Please enter Id to change the right name')

    #             del_input = int(input())
    #             for i in result:
    #                 if i["Id"] == del_input:
    #                     i['Name'] = new_name
    #                     save()
    #                     return say

    #         elif len(result) == 1:
    #             for i in result:
    #                 i['Name'] = new_name
    #                 save()
    #                 return say

    #         else:
    #             print(f'{old_name} not in Adress Book')

    #     elif decision == 'phone' or decision == 'зрщту' or decision == '2':
    #         print(
    #             'Type phone you want to change.If there are no phones - just press "enter".')

    #         if len(result) > 1:
    #             print(f"I've found {len(result)} notes with this Name")
    #             show_find(result)
    #             print('Please enter Id to change the phone of proper name')
    #             del_input = int(input())
    #             for i in result:
    #                 if i["Id"] == del_input:
    #                     old_name = str(input())
    #                     print('Type new phone')
    #                     new_name = str(input())
    #                     for i in result:
    #                         if len(i['Phones']) > 1:
    #                             for j in i['Phones']:
    #                                 if j == old_name:
    #                                     i['Phones'].remove(j)
    #                                     i['Phones'].append(new_name)
    #                                     save()
    #                                     return say
    #                                 else:
    #                                     print(f'{old_name} not in Adress Book')

    #                         elif len(i['Phones']) == 1:
    #                             i['Phones'].remove(old_name)
    #                             i['Phones'].append(new_name)
    #                             return say
    #                         elif len(i['Phones']) == 0:
    #                             i['Phones'].append(new_name)
    #                             save()
    #                             return say

    #         elif len(result) == 1:
    #             old_name = str(input())
    #             print('Type new phone')
    #             new_name = str(input())
    #             for i in result:
    #                 if len(i['Phones']) > 1:
    #                     for j in i['Phones']:
    #                         if j == old_name:
    #                             i['Phones'].remove(j)
    #                             i['Phones'].append(new_name)
    #                             save()
    #                             return say
    #                     else:
    #                         print(f'{old_name} not in Adress Book')

    #                 elif len(i['Phones']) == 1:
    #                     i['Phones'].remove(old_name)
    #                     i['Phones'].append(new_name)
    #                     return say
    #                 elif len(i['Phones']) == 0:
    #                     i['Phones'].append(new_name)
    #                     save()
    #                     return say
    #         else:
    #             print(f'{old_name} not in Adress Book')

    #     elif decision == 'birthday' or decision == 'ишкервфн' or decision == '3':
    #         print('Type birthday you want to change. Expected day.month.year(Example:25.12.1970). If there is no birthday - just press "enter".')
    #         if len(result) > 1:
    #             print(f"I've found {len(result)} notes with this Name")
    #             show_find(result)
    #             print('Please enter Id to change birthday of proper name')
    #             del_input = int(input())
    #             for i in result:
    #                 if i["Id"] == del_input:
    #                     old_name = str(input())
    #                     print(
    #                         'Type new birthday. Expected day.month.year(Example:25.12.1970). If year of birth is not known, type 1111')
    #                     new_name = str(input())
    #                     try:
    #                         new_name = datetime.strptime(
    #                             new_name, "%d.%m.%Y").date()
    #                     except:
    #                         print(
    #                             'Wrong input. Expected day.month.year(Example:25.12.1970)')
    #                     for i in result:
    #                         if i['Birthday'] == old_name:
    #                             i['Birthday'] = new_name
    #                             save()
    #                             return say
    #                         elif i['Birthday'] == None:
    #                             i['Birthday'] = new_name
    #                             save()
    #                             return say
    #                         else:
    #                             print(f'{old_name} not in Adress Book')
    #         elif len(result) == 1:
    #             old_name = str(input())
    #             print('Type new birthday. Expected day.month.year(Example:25.12.1970)')
    #             new_name = str(input())
    #             try:
    #                 new_name = datetime.strptime(new_name, "%d.%m.%Y").date()
    #             except:
    #                 print('Wrong input. Expected day.month.year(Example:25.12.1970)')
    #             for i in result:
    #                 if i['Birthday'] == old_name:
    #                     i['Birthday'] = new_name
    #                     save()
    #                     return say
    #                 elif i['Birthday'] == None:
    #                     i['Birthday'] = new_name
    #                     save()
    #                     return say
    #                 else:
    #                     print(f'{old_name} not in Adress Book')

    #     elif decision == 'address' or decision == 'adress' or decision == 'adres' or decision == 'фввкуіі' or decision == 'фвкуі' or decision == '4':
    #         print(
    #             'Type address you want to change. If there is no address - just press "enter".')
    #         old_name = str(input())
    #         print('Type new address.')
    #         new_name = str(input())
    #         for i in result:
    #             if i['Address'] == old_name:
    #                 i['Address'] = new_name
    #                 save()
    #                 return say
    #             elif i['Address'] == None:
    #                 i['Address'] = new_name
    #                 save()
    #                 return say
    #             else:
    #                 print(f'{old_name} not in Adress Book')

    #     elif decision == 'email' or decision == 'e-mail' or decision == 'уьфшд' or decision == '5':
    #         print(
    #             'Type E-mail you want to change. If there are no E-mail - just press "enter".')
    #         old_name = str(input())
    #         print('Type new E-mail.')
    #         new_name = str(input())
    #         for i in result:
    #             if i['E-mail'] == old_name:
    #                 i['E-mail'] = new_name
    #                 save()
    #                 return say
    #             elif i['E-mail'] == None:
    #                 i['E-mail'] = new_name
    #                 save()
    #                 return say
    #             else:
    #                 print(f'{old_name} not in Adress Book')

    #     elif decision == 'tags' or decision == 'tag' or decision == 'ефп' or decision == '6':
    #         print(
    #             'Type Tags you want to change. If there are no Tags - just press "enter"')
    #         old_name = str(input())
    #         print('Type new Tags.')
    #         new_name = str(input())
    #         for i in result:
    #             if i['Tags'] == old_name:
    #                 i['Tags'] = new_name
    #                 save()
    #                 return say
    #             elif i['Tags'] == None:
    #                 i['Tags'] = new_name
    #                 save()
    #                 return say
    #             else:
    #                 print(f'{old_name} not in Adress Book')

    #     elif decision == 'exit' or decision == 'esc' or decision == 'close' or decision == 'учше' or decision == '7':
    #         view.esc_e = False
    #         return view.esc_e

    # else:
    #     print(f'{old_name} not in Adress Book')


# def clear():
#     os.system('cls' if os.name == 'nt'else 'clear')


# @error_handler
def clean_folder():
    user_input = view.enter_path_for_clean_lolder()
    path = pathlib.Path(user_input)
    CleanFolder().print_recursive(path, user_input)
    CleanFolder().delete_dir(user_input)
    view.notify_of_message('Everything done! Please check your folder!')


# @error_handler
def birthday():

    view.notify_of_message(100*'_')
    decision = view.input_birthday_search_type()
    result = []

    if decision == 1:
        n = view.input_for_birthday_1()
        bday, result = model.book.find_persons_with_birthday_in_n_days(n)
        if result:
            view.notify_of_message(
                f'On {bday} you need to congratulate {len(result)} people from your Addressbook')
            show_find(result)
        else:
            view.notify_of_message(f'You need to congratulate noone on {bday}')

    elif decision == 2:
        n = view.input_for_birthday_2()
        result = model.book.find_persons_with_birthday_during_n_days(n)
        if len(result) > 0:
            print(
                f'In future {n} days you need to congratulate {len(result)} people from your Addressbook')
            show_find(result)
        else:
            print(
                f'In future {n} days nobody from your Addressbook will have birthday')

    elif decision == 3:
        name = view.input_for_birthday_3()
        result = model.book.find_persons_birthday(name)
        if result:
            view.print_persons_and_their_birthday(result)
        else:
            view.notify_of_message(
                'No information about birthday. Please enter valid information using command "change" or add new person to Addressbook')

    elif decision == 4 or decision in EXIT_DECISION:
        view.esc_e = False
        view.say_buy()

    else:
        view.notify_of_message('This Name is not found!')

# @error_handler


def delete():
    view.notify_of_message(100*'_')
    find_v = view.input_name(
        message="Put Name, you want to find and delete from your addressbook")
    find_v = find_v.lower()
    result = model.book.find_value(find_v)

    if len(result) == 1:
        for i in result:
            if i["Name"].lower() == find_v:
                model.book.remove(i)
                view.notify_of_message(f"You've deleted {find_v}")
                save()
    elif len(result) > 1:
        # если найдены несколько результатов поиска
        view.notify_of_message(
            f"I've found {len(result)} notes with this Name")
        show_find(result)
        # ввод id для удаления
        del_input = view.input_id()
        # удаление
        for i in model.book:
            if i["Id"] == del_input:
                model.book.remove(i)
                view.notify_of_message(f"You've deleted {find_v.upper()}")
                model.save_books()
    else:
        view.notify_of_message(
            f"The contact with name {find_v.upper()} is not found")


# @error_handler
def find():
    view.notify_of_message(100*'_')
    find_v = view.input_name(
        message="Put word, half of word or digits you want to find")
    result = model.book.find_value(find_v)
    view.notify_of_message("I've found following:")
    show_find(result)


def show_find(result):
    # выводит результаты поиска по объекту класса AdressBook
    number = len(result)
    iter = result.iterator(number)
    for i in iter:
        view.show_one_page_of_addressbook(i)


def exit():
    model.save_books()
    view.esc_e = False
    view.say_buy()


def save():
    model.save_books()

# @error_handler


def show():
    number = view.enter_number_of_page()
    iter = model.book.iterator(number)

    for i in iter:
        view.show_one_page_of_addressbook(i)

    view.notify_of_message("The end of the contacts book")

##############################################################
# Команды для Handler для работы с NotesBook


# @error_handler
def add_note():
    text, hashtag = view.add_note()
    model.notes_book.add_note(text, hashtag)
    view.notify_of_message("Your note is successfully saved")


# @error_handler
def delete_note():
    hashtag = view.delete_note()
    model.notes_book.delete_note(hashtag)
    view.notify_of_message(f"The note with hashtag '{hashtag}' is deleted")


# @error_handler
def edit_note():
    hashtag = view.edit_note()
    model.notes_book.edit_note(hashtag)


# @error_handler
def find_note():
    keyword = view.find_note()
    result = model.notes_book.find_note(keyword)
    print(result)
    if result:
        view.print_notes_book(result)
        view.notify_of_message("The search is sucessfully finished")
    else:
        view.notify_of_message("Keyword is not found")


# @error_handler
def sort_notes():
    search_type = view.sort_notes()
    view.print_notes_book(model.notes_book.sort_notes(search_type))


# @error_handler
def show_notes():
    view.notify_of_message('Your Notes Book:')
    view.print_notes_book(model.notes_book)

# Конец конец команд для NotesBook


def help_func():
    view.help()


# @ error_handler
def handler(user_inpu):
    if user_inpu in COMMANDS.keys():
        # если ввод команды понятный:
        return COMMANDS[user_inpu]()
    else:
        # если ввод команды не понятен - мы уточняем у пользователядщф
        for key, value in GUESS_COMMANDS.items():
            if user_inpu in key:
                guess_command = value
                if view.clarify_command(guess_command):
                    return COMMANDS[guess_command]()
        return view.notify_of_error()


YES_DECISION = {'y', 'yes', 'нуі', 'н', 'да', 'д'}

NO_DECISION = {'n', 'not', 'no', 'нет', 'тщ', 'тще', 'т'}

EXIT_DECISION = {'exit', 'учше', 'esc', 'close'}

COMMANDS = {'add': add, 'ad': add, '+': add, 'фвв': add, 'change': change, 'срфтпу': change, 'close': exit, 'exit': exit, 'учше': exit,
            'find': find, 'аштв': find, 'help': help_func, 'рудз': help_func, 'хелп': help_func, 'save': save, 'іфму': save, 'ыфму': save, 'show': show, 'ырщц': show, 'ірщц': show,
            'delete': delete, 'del': delete, 'вуд': delete, 'вудуеу': delete, 'birthday': birthday, 'ишкервфн': birthday, 'clean': clean_folder, 'сдуфт': clean_folder,
            'add note': add_note, 'фвв тщеу': add_note, 'delete note': delete_note, 'вудуеу тщеу': delete_note, 'edit note': edit_note, 'увше тщеу': edit_note,
            'find note': find_note, 'аштв тщеу': find_note, 'sort notes': sort_notes, 'ыщке тщеуы': sort_notes, 'show notes': show_notes, 'ырщц тщеуы': show_notes}

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


if __name__ == '__main__':
    main()
