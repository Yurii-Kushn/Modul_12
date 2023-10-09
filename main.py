import re
import json
from collections import UserDict
from datetime import date


class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self) -> str:
        return self._value

    def __str__(self):
        return str(self.value)

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)
        self.value = value

    @Field.value.setter
    def value(self, value):
        self._value = value


class Phone(Field):
    @Field.value.setter
    def value(self, value: str) -> None:
        if 10 <= len(value) < 11 and re.search(r"\d{10}", value):
            self._value = value
        else:
            raise ValueError("It isn't phone number")


class Birthday(Field):
    @Field.value.setter
    def value(self, value: str) -> None:
        print(value)
        if re.search(r"\d{4}-\d{2}-\d{2}", value):
            self._value = value
        else:
            raise ValueError("It's a wrong date format. Correct date format: yyyy-mm-dd")


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = birthday

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p for p in self.phones)}"

    def add_phone(self, phone):
        phone2 = Phone(phone)
        if phone2.value:
            self.phones.append(phone2.value)

    def remove_phone(self, phone):
        self.phones.remove(phone)

    def edit_phone(self, phone_1, phone_2):
        if phone_1 not in self.phones:
            pass
        phone_2 = Phone(phone_2)
        if phone_2.value:
            for phone_obj in self.phones:
                if phone_obj == phone_1:
                    index = self.phones.index(phone_1)
                    self.phones.remove(phone_1)
                    self.phones.insert(index, phone_2.value)

    def find_phone(self, phone):
        phone = Phone(phone)
        for phone_obj in self.phones:
            if phone_obj == phone.value:
                return Phone(phone_obj)

    def days_to_birthday(self, birthday):
        birthday = Birthday(birthday)
        current_day = date.today()
        birthday_day = date.fromisoformat(birthday.value)
        return (birthday_day - current_day).days


class AddressBook(UserDict):

    def add_record(self, book_record):
        phone_list = self.data.get(book_record.name.value, [])
        for phone in book_record.phones:
            phone_list.append(phone)
        self.data[book_record.name.value] = phone_list

    def find(self, find_name):
        phones = self.data.get(find_name, None)
        if phones:
            f_record = Record(find_name)
            f_record.name.value = find_name
            f_record.phones = phones
            return f_record
        return None

    # def __iter__(self):
    #     return self

    def iterator(self, n):
        current_iter = 0
        records_for_print = []
        for key, value in self.data.items():
            current_iter += 1
            if current_iter > n:
                break
            if self.find(key):
                records_for_print.append(self.find(key).__str__())
        return records_for_print

    # def __next__(self):
    #     raise StopIteration

    def delete(self, del_name):
        ty = self.data.pop(del_name, None)

    # упакування у відкритий файл та розпакування з файлу

    def pack_to_file(self, file_name):
        with open(file_name, "w") as fh:
            json.dump(self.data, fh)

    def unpack_from_file(self, file_name):
        with open(file_name, "r") as fh:
            self.data = json.load(fh)

    # пошук вмісту книги контактів

    def search_by_content(self, content):
        list_found_contacts = []
        for key, phones in self.data.items():
            if key.find(content) != -1:
                list_found_contacts.append(self.find(key).__str__())
                continue
            for value in phones:
                if value.find(content) != -1:
                    list_found_contacts.append(self.find(key).__str__())
                    break
        if not list_found_contacts:
            list_found_contacts = ["Nothing found"]
        return list_found_contacts

if __name__ == '__main__':
    # Створення нової адресної книги
    book = AddressBook()

    # Створення запису для John
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("1234598760")
    book.add_record(john_record)
    print(john_record)

    # Створення запису для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9934567890")
    jane_record.add_phone("8834598760")
    book.add_record(jane_record)

    # Створення запису для Jane2
    jane2_record = Record("Jane2")
    jane2_record.add_phone("9934567890")
    jane2_record.add_phone("8834598760")
    book.add_record(jane2_record)


    # Виведення всіх записів у книзі book
    for name, record in book.data.items():
        print(f'{name}: {record}')

    print("test: упакування у відкритий файл та розпакування з файлу")

    book.pack_to_file("data.json")

    book2 = AddressBook()
    book2.unpack_from_file("data.json")

    # Виведення всіх записів нової адресної книги book2
    for name, record in book2.data.items():
        print(f'{name}: {record}')

    print("test: пошук списку контактів за вмістом книги контактів")

    list_search = book.search_by_content("Jan")
    print("content = Jan")
    for value in list_search:
        print(value)

    list_search = book.search_by_content("90")
    print("content = 90")
    for value in list_search:
        print(value)

    list_search = book.search_by_content("9999")
    print("content = 9999")
    for value in list_search:
        print(value)