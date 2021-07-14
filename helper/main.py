import pathlib
import pickle
import json
import re
import os
from datetime import datetime, timedelta, date

# from .classbook import *
# from .clean import *
# from .view import *
# from .notes_book import NotesBook

from classbook import *
from clean import *
from notes_book import NotesBook
from view import *


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


def error_handler(func):
    def inner(*args):
        try:
            result = func(*args)
            return result
        except:
            result = view.notify_of_error()
            return result
    return inner


# @error_handler
def main():  # main относится к контроллеру!
    global path, book, notes_book, view, model, esc_e
    esc_e = True
    view = ConsoleView()

    while True:
        view.greete()
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
            esc_e = False
            break
        else:
            view.notify_of_error()

    while esc_e:
        user_inpu = view.choose_command()
        result = handler(user_inpu)
        if result:
            print(result)
        elif result == None:
            pass
        else:
            break


@error_handler
def add():
    print(100*'_')
    say = 'Successfully changed'
    global esc_e, book
    print('Input Name:')
    name = Name(str(input()))

    if name == 'exit' or name == 'esc' or name == 'close' or name == 'учше':
        esc_e = False
        return "Not saved"
    if len(book) > 0 and len(book) <= 25:
        id_n = book[-1]["Id"]+1
    else:
        id_n = 1
    record1 = Record(name, id_n)

    while True:
        print('Do you want to add phone-number? "y" (YES) or "n" (NO). Type "exit" to exit')
        decision = str(input())
        decision = decision.lower()
        if decision == 'y' or decision == 'yes' or decision == 'нуі' or decision == 'н' or decision == 'да' or decision == 'д':
            print('Input Phone Number. Example: +380501234567')
            phone = str(input())
            if re.fullmatch('[+]?[0-9]{3,12}', phone):
                record1.add_phone(phone)
            else:
                print(
                    'Wrong input! Phone may start with + and has from 3 to 12 digits max. Example +380501234567')

        elif decision == 'exit' or decision == 'esc' or decision == 'close' or decision == 'учше':
            esc_e = False
            return 'Closed'
        elif decision == 'n' or decision == 'not' or decision == 'no' or decision == 'нет' or decision == 'тщ' or decision == 'тще' or decision == 'т':
            break
        else:
            print('Wrong input!')

    while True:
        print('Do you want to add Birthday? "y" (YES) or n (NO). Type "exit" to exit')
        birthday_d = None
        decision = str(input())
        decision = decision.lower()
        if decision == 'y' or decision == 'yes' or decision == 'нуі' or decision == 'н' or decision == 'да' or decision == 'д':
            print('Input Birthday. Expected day.month.year(Example:25.12.1970). If year of birth is not known, type 1111')
            birthday = str(input())
            try:
                birthday_d = datetime.strptime(birthday, "%d.%m.%Y").date()
                record1.user['Birthday'] = birthday
                break
            except:
                print(
                    'Wrong Birthday. Expected day.month.year. Format: dd.mm.yyyy (Example:25.12.1970)')

        elif decision == 'exit' or decision == 'esc' or decision == 'close' or decision == 'учше':
            book.add_record(record1.user)
            esc_e = False
            return 'Closed'

        elif decision == 'n' or decision == 'not' or decision == 'no' or decision == 'нет' or decision == 'тщ' or decision == 'тще' or decision == 'т':
            break

        else:
            print('Wrong input!')

    while True:
        print('Do you want to add Address? "y" (YES) or n (NO). Type "exit" to exit')
        decision = str(input())
        decision = decision.lower()
        if decision == 'y' or decision == 'yes' or decision == 'нуі' or decision == 'н' or decision == 'да' or decision == 'д':
            print('Input Address. Please no more than 30 symbols')
            address = str(input())
            if len(address) > 1 and len(address) <= 30:
                record1.user['Address'] = address
                break
            else:
                print(
                    f'Your Address is {len(address)} symbols. Please no more than 30 symbols')
        elif decision == 'exit' or decision == 'esc' or decision == 'close' or decision == 'учше':
            book.add_record(record1.user)
            esc_e = False
            return 'Closed'

        elif decision == 'n' or decision == 'not' or decision == 'no' or decision == 'нет' or decision == 'тщ' or decision == 'тще' or decision == 'т':
            break
        else:
            print('Wrong input!')

    # START HERE
    while True:
        print('Do you want to add E-mail? "y" (YES) or n (NO). Type "exit" to exit')
        decision = str(input())
        decision = decision.lower()
        if decision == 'y' or decision == 'yes' or decision == 'нуі' or decision == 'н' or decision == 'да' or decision == 'д':
            print('Input E-mail. Please no more than 30 symbols')
            email = str(input())
            if re.match('([a-zA-Z][a-zA-Z0-9\._!#$%^*=\-]{1,}@[a-zA-Z]+\.[a-zA-Z]{2,})', email):
                if len(email) > 1 and len(email) <= 30:
                    record1.user['E-mail'] = email
                    break
                else:
                    print(
                        f'Your E-mail is {len(email)} symbols. Please no more than 30 symbols')
            else:
                print(
                    'Format is wrong. Try again in format: your_nickname@something.domen_name')

        elif decision == 'exit' or decision == 'esc' or decision == 'close' or decision == 'учше':
            book.add_record(record1.user)
            esc_e = False
            return 'Closed'

        elif decision == 'n' or decision == 'not' or decision == 'no' or decision == 'нет' or decision == 'тщ' or decision == 'тще' or decision == 'т':
            break

        else:
            print('Wrong input!')

    while True:
        print('Do you want to add Tags? "y" (YES) or n (NO). Type "exit" to exit')
        decision = str(input())
        decision = decision.lower()
        if decision == 'y' or decision == 'yes' or decision == 'нуі' or decision == 'н' or decision == 'да' or decision == 'д':
            print('Input Tags. Please no more than 15 symbols')
            tags = str(input())
            if len(tags) > 1 and len(tags) <= 15:
                record1.user['Tags'] = tags
                book.add_record(record1.user)
                save()
                return say
            else:
                print(
                    f'Your Tags is {len(tags)} symbols. Please no more than 15 symbols')

        elif decision == 'exit' or decision == 'esc' or decision == 'close' or decision == 'учше':
            book.add_record(record1.user)
            esc_e = False
            return 'Closed'

        elif decision == 'n' or decision == 'not' or decision == 'no' or decision == 'нет' or decision == 'тщ' or decision == 'тще' or decision == 'т':
            book.add_record(record1.user)
            save()
            return say
        else:
            print('Wrong input!')


@error_handler
def change():
    print(100*"_")
    global book, esc_e
    say = 'Successfully changed'
    print('Type name of record you want to change')
    old_name = str(input())
    old_name = old_name.lower()
    result = book.find_value(old_name)

    if len(result) > 0 and len(result) != None:
        show_find(result)

        print(100*"_")
        print('1.   To change Name: type "name".\n2.   To change Phone: type "phone".\n3.   To change Birthday: type "birthday".\n4.   To change Address: type "address".\n5.   To change E-mail: type "email".\n6.   To change Tags: type "tags"\n7.   To exit: type "exit".\n')
        decision = str(input())
        decision = decision.lower()

        if decision == 'name' or decision == 'тфьу' or decision == '1':
            print('Type new name')
            new_name = str(input())

            if len(result) > 1:
                print(f"I've found {len(result)} notes with this Name")
                show_find(result)
                print('Please enter Id to change the right name')

                del_input = int(input())
                for i in result:
                    if i["Id"] == del_input:
                        i['Name'] = new_name
                        save()
                        return say

            elif len(result) == 1:
                for i in result:
                    i['Name'] = new_name
                    save()
                    return say

            else:
                print(f'{old_name} not in Adress Book')

        elif decision == 'phone' or decision == 'зрщту' or decision == '2':
            print(
                'Type phone you want to change.If there are no phones - just press "enter".')

            if len(result) > 1:
                print(f"I've found {len(result)} notes with this Name")
                show_find(result)
                print('Please enter Id to change the phone of proper name')
                del_input = int(input())
                for i in result:
                    if i["Id"] == del_input:
                        old_name = str(input())
                        print('Type new phone')
                        new_name = str(input())
                        for i in result:
                            if len(i['Phones']) > 1:
                                for j in i['Phones']:
                                    if j == old_name:
                                        i['Phones'].remove(j)
                                        i['Phones'].append(new_name)
                                        save()
                                        return say
                                    else:
                                        print(f'{old_name} not in Adress Book')

                            elif len(i['Phones']) == 1:
                                i['Phones'].remove(old_name)
                                i['Phones'].append(new_name)
                                return say
                            elif len(i['Phones']) == 0:
                                i['Phones'].append(new_name)
                                save()
                                return say

            elif len(result) == 1:
                old_name = str(input())
                print('Type new phone')
                new_name = str(input())
                for i in result:
                    if len(i['Phones']) > 1:
                        for j in i['Phones']:
                            if j == old_name:
                                i['Phones'].remove(j)
                                i['Phones'].append(new_name)
                                save()
                                return say
                        else:
                            print(f'{old_name} not in Adress Book')

                    elif len(i['Phones']) == 1:
                        i['Phones'].remove(old_name)
                        i['Phones'].append(new_name)
                        return say
                    elif len(i['Phones']) == 0:
                        i['Phones'].append(new_name)
                        save()
                        return say
            else:
                print(f'{old_name} not in Adress Book')

        elif decision == 'birthday' or decision == 'ишкервфн' or decision == '3':
            print('Type birthday you want to change. Expected day.month.year(Example:25.12.1970). If there is no birthday - just press "enter".')
            if len(result) > 1:
                print(f"I've found {len(result)} notes with this Name")
                show_find(result)
                print('Please enter Id to change birthday of proper name')
                del_input = int(input())
                for i in result:
                    if i["Id"] == del_input:
                        old_name = str(input())
                        print(
                            'Type new birthday. Expected day.month.year(Example:25.12.1970). If year of birth is not known, type 1111')
                        new_name = str(input())
                        try:
                            new_name = datetime.strptime(
                                new_name, "%d.%m.%Y").date()
                        except:
                            print(
                                'Wrong input. Expected day.month.year(Example:25.12.1970)')
                        for i in result:
                            if i['Birthday'] == old_name:
                                i['Birthday'] = new_name
                                save()
                                return say
                            elif i['Birthday'] == None:
                                i['Birthday'] = new_name
                                save()
                                return say
                            else:
                                print(f'{old_name} not in Adress Book')
            elif len(result) == 1:
                old_name = str(input())
                print('Type new birthday. Expected day.month.year(Example:25.12.1970)')
                new_name = str(input())
                try:
                    new_name = datetime.strptime(new_name, "%d.%m.%Y").date()
                except:
                    print('Wrong input. Expected day.month.year(Example:25.12.1970)')
                for i in result:
                    if i['Birthday'] == old_name:
                        i['Birthday'] = new_name
                        save()
                        return say
                    elif i['Birthday'] == None:
                        i['Birthday'] = new_name
                        save()
                        return say
                    else:
                        print(f'{old_name} not in Adress Book')

        elif decision == 'address' or decision == 'adress' or decision == 'adres' or decision == 'фввкуіі' or decision == 'фвкуі' or decision == '4':
            print(
                'Type address you want to change. If there is no address - just press "enter".')
            old_name = str(input())
            print('Type new address.')
            new_name = str(input())
            for i in result:
                if i['Address'] == old_name:
                    i['Address'] = new_name
                    save()
                    return say
                elif i['Address'] == None:
                    i['Address'] = new_name
                    save()
                    return say
                else:
                    print(f'{old_name} not in Adress Book')

        elif decision == 'email' or decision == 'e-mail' or decision == 'уьфшд' or decision == '5':
            print(
                'Type E-mail you want to change. If there are no E-mail - just press "enter".')
            old_name = str(input())
            print('Type new E-mail.')
            new_name = str(input())
            for i in result:
                if i['E-mail'] == old_name:
                    i['E-mail'] = new_name
                    save()
                    return say
                elif i['E-mail'] == None:
                    i['E-mail'] = new_name
                    save()
                    return say
                else:
                    print(f'{old_name} not in Adress Book')

        elif decision == 'tags' or decision == 'tag' or decision == 'ефп' or decision == '6':
            print(
                'Type Tags you want to change. If there are no Tags - just press "enter"')
            old_name = str(input())
            print('Type new Tags.')
            new_name = str(input())
            for i in result:
                if i['Tags'] == old_name:
                    i['Tags'] = new_name
                    save()
                    return say
                elif i['Tags'] == None:
                    i['Tags'] = new_name
                    save()
                    return say
                else:
                    print(f'{old_name} not in Adress Book')

        elif decision == 'exit' or decision == 'esc' or decision == 'close' or decision == 'учше' or decision == '7':
            esc_e = False
            return esc_e

    else:
        print(f'{old_name} not in Adress Book')


def clear():
    os.system('cls' if os.name == 'nt'else 'clear')

# START CHaNGE


@error_handler
def clean_folder():

    print(100*"_")
    print('Welcome to clean folder instrument!')
    print(100*"_")
    print('Please enter path to clean and structurise.')
    user_input = str(input())

    path = pathlib.Path(user_input)
    print_recursive(path, user_input)
    delete_dir(user_input)
    # D:\Tresh
    return 'Everything done! Please check yor folder!'


@error_handler
def birthday():
    global esc_e
    print(100*'_')
    print("1.   If you want to find, who'll have birthday in exact date TYPE 1.\n2.   If you need to know who'll have birthday in period of time TYPE 2.\n3.   If you need to know how many days to somebody's birthday TYPE 3.\n4.   Type 'exit' to exit")
    decision = int(input())
    result = []

    if decision == 1:
        print("Please write in how many days will be people's birthday.")
        n = int(input())
        if n >= 365:
            n = n % 365

        today_d = datetime.now().date()
        d = timedelta(days=n)
        bday = today_d+d
        bday = bday.strftime("%d.%m.%Y")
        for i in book:
            if i["Birthday"] != 0 and i["Birthday"] != None:
                if days_to_birthday(i["Birthday"]) == n:
                    result.append(i)
        print(
            f'On {bday} you need to congratulate {len(result)} people from your Addressbook')

        show_find(result)

    elif decision == 2:
        print("Please write how many days in advance to warn you about people's birthday.")
        n = int(input())
        for i in book:
            if i["Birthday"] != 0 and i["Birthday"] != None:
                if days_to_birthday(i["Birthday"]) <= n:
                    result.append(i)

        if len(result) > 0:
            print(
                f'In future {n} days you need to congratulate {len(result)} people from your Addressbook')
            show_find(result)
        else:
            print(
                f'In future {n} days nobody from your Addressbook will have birthday')

    elif decision == 3:
        print("Please write name to know how many days left to birthday.")
        name = input()
        result = book.find_value(name)
        if len(result) > 1:
            print(f"I've found {len(result)} notes with this Name")
            show_find(result)
            print(
                'Please enter Id to know how many days left to birthday the exact person')
            id_input = int(input())
            for i in result:
                if i["Id"] == id_input:
                    days = days_to_birthday(i['Birthday'])
                    print(
                        f'{i["Name"]} from your Addressbook will have birthday in {days} days. Do not forget to congratulate!')

        elif len(result) == 1:
            for i in result:
                days = days_to_birthday(i['Birthday'])
                print(
                    f'{i["Name"]} from your Addressbook will have birthday in {days} days. Do not forget to congratulate!')
        else:
            print(f'No information about birthday. Please enter valid information using command "change" or add new person to Addressbook')

    elif decision == 4 or decision == 'exit':
        esc_e = False
        return "Closed"

    else:
        print('Not found this Name!')


def days_to_birthday(bday):
    today_d = datetime.now().date()
    bday = datetime.strptime(bday, "%d.%m.%Y").date()
    bday = date(today_d.year, bday.month, bday.day)

    if today_d > bday:
        bday = date(today_d.year+1, bday.month, bday.day)
        days_left = (bday-today_d)
    else:
        days_left = (bday-today_d)

    return days_left.days


@error_handler
def delete():
    print(100*'_')
    print('Put Name, you want to find and delete from your addressbook')
    find_v = str(input())
    find_v = find_v.lower()
    result = book.find_value(find_v)
    for i in result:
        if i["Name"].lower() != find_v:
            result.remove(i)

    if len(result) > 1:
        print(f"I've found {len(result)} notes with this Name")
        show_find(result)
        print('Please enter Id to delete the right note')

        del_input = int(input())
        for i in book:
            if i["Name"].lower() == find_v and i["Id"] == del_input:
                book.remove(i)
                print(f"You've deleted {find_v}")
                save()

    elif len(result) == 1:
        for i in result:
            if i["Name"].lower() == find_v:
                book.remove(i)
                print(f"You've deleted {find_v}")
                save()

    else:
        print(f"{find_v} not found")

# end


@error_handler
def find():
    print(100*'_')
    print('Put word, half of word or digits you want to find')
    find_v = str(input())
    result = book.find_value(find_v)
    show_find(result)


def show_find(v_list):

    print("I've found following:")
    # Печать шапки с названием столбцов
    print(145*'_')
    print('| ID  |           Name           |     Phones      |  Birthday  |           Address            |              E-mail            |       Tags     |')
    print(145*'-')

    for i in v_list:
        print(f'|{i["Id"]:<5}| {i["Name"]:<25}| { i["Phones"][0] if len(i["Phones"])>=1 else " ":<15} | {i["Birthday"]if i["Birthday"] else " ":<11}|{i["Address"]if i["Address"] else " ":<30}|  {i["E-mail"]if i["E-mail"] else " ":<30}| {i["Tags"] if i["Tags"] else " ":<15}|')
        if len(i["Phones"]) > 1:
            for elem in i["Phones"][1:]:
                print(
                    f'|     |                          | {elem: <15} |            |                              |                                |                |')
        print(f"{145*'_'}")


def exit():
    global esc_e
    save()
    esc_e = False
    return "Good Bye"


def save():
    with open(path, 'wb') as fh:
        model.save_books()

# @error_handler


def show():
    number = input('Please input the number or record on 1 page: ')
    try:
        number = int(number)
    except:
        number = 10
    print("The contacts book is following:")
    if number == 0 or number == None:
        number = 10
    iter = book.iterator1(number)
    for i in iter:
        # Печать шапки с названием столбцов
        print(145*'_')
        print('| ID  |           Name           |     Phones      |  Birthday  |           Address            |              E-mail            |      Tags      |')
        print(145*'-')
        print(i)
        print(63*'_'+'The end of the page. PRESS ENTER'+63*'_')
        input()
    return "The end of the contacts book"
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


@error_handler
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
        else:
            return view.notify_of_error()


COMMANDS = {'add': add, 'ad': add, '+': add, 'фвв': add, 'change': change, 'срфтпу': change, 'close': exit, 'exit': exit, 'учше': exit, 'clear': clear, 'сдуфк': clear,
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
