
class ViewInterface:
    def greeting(self):
        raise NotImplementedError('Greeting func is not implemented')

    def register_or_authorize(self):
        raise NotImplementedError(
            'register_or_authorize func is not implemented')

    def register(self):
        raise NotImplementedError('register func is not implemented')

    def authorize(self):
        raise NotImplementedError('authorize func is not implemented')


class ConsoleView(ViewInterface):
    def __init__(self):
        super().__init__()
        self.esc_e = True

    def greete(self):
        print(100*'_')
        print('Hello! What do you want to do?')

    def register_or_authorize(self):
        # возвращает команду load / new / exit
        print('You can use commands:')
        print('1.  "load" to load AddressBook and NotesBook\n2.  "new" to create new Book\n3.  "exit"/"close" to close application:')
        return str(input())

    def register(self):
        print(
            r'Please write the full path where to create file. Example: "d:\test\book.txt":')
        return str(input())

    def authorize(self):
        # возвращает путь к файлу
        print(r'Please write the full path to file with addressbook and notebook. Example: "d:\test\book.txt":')
        return str(input())

    def choose_command(self):
        print(100*'_')
        user_inpu = input(
            '   What do you want to do?\n   Type exact command you want to do, \n   "help" for list of commands.\n   "exit" to exit\n')
        return user_inpu.lower()

    def say_buy(self):
        print('The Helper is closing... Buy-buy')

    def notify_of_error(self):
        print('Wrong input! Type exact command you want to do,"exit" to exit or "help" for list of commands.')

    def notify_of_message(self, message):
        print(message)

    def add_note(self):
        # возвращает кортеж (текст заметки, хєштег)
        print('Please input your note (to stop entering note press "ENTER" twice):')
        # ввод многострочной заметки
        lines = []
        flag = True
        while flag:
            line = input()
            if len(line) > 0 and len(line) <= 40:
                lines.append(line)
            elif len(line) > 40:
                print('Please no more than 40 symbols in one line')
            else:
                flag = False
        text = '\n'.join(lines)

        # ввод тєгов
        flag = True
        while flag:
            hashtag = input('Please input the hashtag of your note: \n')
            if len(hashtag) == 0 and len(hashtag) > 30:
                print('Please no more than 30 symbolsa and no empty')
            else:
                flag = False
        return text, hashtag.upper()

    def help(self):
        print(60*'*')
        print(20*'*'+'WORKING WITH ADDRESSBOOK:'+20*'*')
        print('*Type "add"      to add new contact.\n*Type "birthday" to see people that have birthday nearest days.\n*Type "change"   to change contact\'s phone, name or birthday.\n*Type "clear"   to clear terminal window.\n*Type "delete"    to delete information that you don\'t need.\n*Type "find"      to see information that you are looking for.\n*Type "show"      to show you all phonebook.\n*Type "save"      to save and exit.\n*Type "exit"      to exit')
        print(20*'*'+'WORKING WITH NOTESBOOK:'+20*'*')
        print('*Type "add note"    to add new note.\n*Type "delete note"    to delete note.\n*Type "edit note"    to edit note.\n*Type "find note"    to look through notes.\n*Type "sort notes"    to sort notes.\n*Type "show notes"    to show your notes.\n')
        print(20*'*'+'WORKING WITH CLEANFOLDER:'+20*'*')
        print('*Type "clean"    to clean and structurise folder.\n')
        print(60*'*')

    def delete_note(self):
        print("Я внутри delete_note --- view")
        print("Please input a hashtag of note that you would like to delete:")
        return input().upper()

    def edit_note(self):
        print("Please input a hashtag of note that you would like to edit:")
        return input().upper()

    def find_note(self):
        print('Please input keyword for search:')
        keyword = input().upper()
        print('THE RESULTS OF SEARCH:')
        return keyword

    def print_notes_book(self, notesbook):
        print(notesbook)

    def sort_notes(self):
        print("What type of sort would you like? Please input:")
        print("1 - to sort from A to Z")
        print("2 - to sort from Z to A")
        print("3 - to sort from old notes to new notes")
        print("4 - to sort from new notes to old notes")
        search_type = input()
        print('The sorted Notes are:')
        return search_type

    def clarify_command(self, guess_command):
        print(
            f'Maybe you mean {guess_command} command?\nIf YES type "yes" or "y"\nIf NO type "no" or "n"')
        decision = str(input())
        decision = decision.lower()
        if decision in ('y', 'yes', 'нуі', 'н', 'да', 'д'):
            return True
        else:
            return False

    def enter_number_of_page(self):
        number = input('Please input the number of record on 1 page: ')
        try:
            number = int(number)
        except:
            number = 10
        print("The contacts book is following:")
        if number == 0 or number == None:
            number = 10
        return number

    def show_one_page_of_addressbook(self, i):
        print(145*'_')
        print('| ID  |           Name           |     Phones      |  Birthday  |           Address            |              E-mail            |      Tags      |')
        print(145*'-')
        print(i)
        print(63*'_'+'The end of the page. PRESS ENTER'+63*'_')
        input()

    def enter_path_for_clean_lolder(self):
        print(100*"_")
        print('Welcome to clean folder instrument!')
        print(100*"_")
        print('Please enter path to clean and structurise.')
        return str(input())
    ##########Функции for Controller - Add #################

    def ask_to_add_field(self, field_name):
        print(
            f'Do you want to add {field_name.upper()} "y" (YES) or "n" (NO). Type "exit" to exit')
        decision = str(input())
        decision = decision.lower()
        return decision

    def input_name(self):
        print('Input Name:')
        return str(input())

    def input_phone(self):
        print('Input Phone Number. Example: +380501234567')
        return str(input())

    def input_birthday(self):
        print('Input Birthday. Expected day.month.year(Example:25.12.1970). If year of birth is not known, type 1111')
        return str(input())

    def input_address(self):
        print('Input Address. Please no more than 30 symbols')
        return str(input())

    def input_email(self):
        print('Input E-mail. Please no more than 30 symbols')
        return str(input())

    def input_tags(self):
        print('Input Tags. Please no more than 15 symbols')
        return str(input())

    def input_birthday_search_type(self):
        print("1.   If you want to find, who'll have birthday in exact date TYPE 1.\n2.   If you need to know who'll have birthday in period of time TYPE 2.\n3.   If you need to know how many days to somebody's birthday TYPE 3.\n4.   Type 'exit' to exit")
        return int(input())

    def input_for_birthday_1(self):
        print("Please write in how many days will be people's birthday.")
        return int(input())
