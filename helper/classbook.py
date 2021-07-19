import re

from collections import UserList
from datetime import datetime, timedelta, date


class AddressBook(UserList):

    data = []

    def add_record(self, record):
        self.data.append(record)

    def find_value(self, f_value):
        f_value = f_value.lower()
        result = AddressBook()

        for record_user in self:
            for value in record_user.values():
                if (isinstance(value, str)):
                    value = value.lower()
                    if value.find(f_value) != -1:
                        if record_user not in result:
                            result.append(record_user)
                            break
                elif value != None:
                    if (isinstance(value, list)):
                        for j in value:
                            j = j.lower()
                            if j.find(f_value) != -1:
                                result.append(record_user)
                                break
        return result

    def iterator(self, n):
        # возвращает текстовое представление объекта для консольного интерфейса
        counter = 0
        result = ""
        for i in self:
            result += f'|{i["Id"]:<5}| {i["Name"]:<25}| { i["Phones"][0] if len(i["Phones"])>=1 else " ":<15} | {str(i["Birthday"]) if i["Birthday"] else " ":<11}|{i["Address"]if i["Address"] else " ":<30}|  {i["E-mail"]if i["E-mail"] else " ":<30}| {i["Tags"] if i["Tags"] else " ":<15}|\n'
            if len(i["Phones"]) > 1:
                for elem in i["Phones"][1:]:
                    result += f'|     |                          | {elem: <15} |            |                              |                                |                | \n'
            result += f"{145*'_'}\n"
            # конец записи строки с описанием 1 контакта
            counter += 1
            if counter == n:
                result = result.rstrip("\n")
                yield result
                result = ""
                counter = 0
        if result:
            result = result.rstrip("\n")
            yield result

    def find_persons_with_birthday_in_n_days(self, n):
        # ищет людей с др в data
        # возвращает объект AdressBook

        if n >= 365:
            n = n % 365

        birthday_book = AddressBook()

        today_d = datetime.now().date()
        d = timedelta(days=n)
        bday = today_d+d
        for record_user in self.data:
            if record_user["Birthday"] != 0 and record_user["Birthday"] != None:
                if Birthday.days_to_birthday(record_user["Birthday"]) == n:
                    birthday_book.append(record_user)
        return bday, birthday_book

    def find_persons_with_birthday_during_n_days(self, n):
        birthday_book = AddressBook()
        for record_user in self.data:
            if record_user["Birthday"] != 0 and record_user["Birthday"] != None:
                if Birthday.days_to_birthday(record_user["Birthday"]) <= n:
                    birthday_book.append(record_user)
        return birthday_book

    def find_persons_birthday(self, name):
        # возвращает список кортежей (имя, дней до ДР)
        birthday_book = self.find_value(name)
        result = []
        for record_user in birthday_book.data:
            if record_user['Birthday']:
                name = record_user['Name']
                days = Birthday.days_to_birthday(record_user['Birthday'])
                result.append((name, days))
        print(result)
        return result


class Birthday:
    def __init__(self, value):
        self.birthday = value

    @staticmethod
    def days_to_birthday(bday):
        today_d = datetime.now().date()
        bday = bday.replace(year=today_d.year)
        if today_d > bday:
            bday = date(today_d.year+1, bday.month, bday.day)
            days_left = (bday-today_d)
        else:
            days_left = (bday-today_d)
        return days_left.days


class Record:
    def __init__(self, name, id_n, phones=None, birthday=None, address=None, email=None, tags=None):
        self.id_n = id_n
        self.name = name
        self.phones = []
        self.birthday = birthday  # хранится дата без времени в формате datetime
        self.address = address
        self.email = email
        self.tags = tags
        self.user = {'Id': self.id_n,
                     'Name': self.name,
                     'Phones': self.phones,
                     'Birthday': self.birthday,
                     'Address': self.address,
                     'E-mail': self.email,
                     'Tags': self.tags}

    def __str__(self) -> str:
        result = ""
        for i in self.user:
            result += f'|{i["Id"]:<5}| {i["Name"]:<25}| { i["Phones"][0] if len(i["Phones"])>=1 else " ":<15} | {str(i["Birthday"]) if i["Birthday"] else " ":<11}|{i["Address"]if i["Address"] else " ":<30}|  {i["E-mail"]if i["E-mail"] else " ":<30}| {i["Tags"] if i["Tags"] else " ":<15}|\n'
            if len(i["Phones"]) > 1:
                for elem in i["Phones"][1:]:
                    result += f'|     |                          | {elem: <15} |            |                              |                                |                | \n'
            result += f"{145*'_'}\n"
        return result

    def add_address(self, address):
        self.address = address

    def add_birthday(self, birthday):
        self.birthday = datetime.strptime(
            birthday, "%d.%m.%Y").date()
        self.user['Birthday'] = self.birthday

    def add_email(self, email):
        self.email = email

    def add_id(self, id_n):
        self.id_n = id_n

    def add_phone(self, phone):
        phone = str(phone)
        try:
            num = re.fullmatch('[+]?[0-9]{3,12}', phone)
            if num:
                self.phones.append(phone)
        except:
            print('Phone must start with + and have 12 digits. Example +380501234567 ADD')

    def remove_phone(self, phone):
        for i in range(len(self.phones)):
            if self.phones[i].phone == phone:
                self.phones.pop(i)

    def edit_phone(self, phone, new_phone):
        self.remove_phone(phone)
        self.add_phone(new_phone)

    def validate_phone(self, phone):
        return re.fullmatch('[+]?[0-9]{3,12}', phone)

    def validate_address(self, address):
        return len(address) > 1 and len(address) <= 30

    def validate_tags(self, tags):
        return len(tags) > 1 and len(tags) <= 15

    def validate_email_format(self, email):
        return re.match('([a-zA-Z][a-zA-Z0-9\._!#$%^*=\-]{1,}@[a-zA-Z]+\.[a-zA-Z]{2,})', email)

    def validate_email_duration(self, email):
        return (len(email) > 1 and len(email) <= 30)

    def validate_birthday(self, birthday):
        try:
            datetime.strptime(birthday, "%d.%m.%Y").date()
            return True
        except:
            return False
