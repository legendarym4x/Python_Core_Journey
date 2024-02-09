from collections import UserDict
from datetime import datetime
import json


class Field:
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):

    @Field.value.setter
    def value(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must consist of 10 digits")
        else:
            self._value = value


class Birthday(Field):

    @Field.value.setter
    def value(self, value):
        today = datetime.now().date()
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            print("Invalid birthday format. Please use YYYY-MM-DD")
        self._value = value


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        for p in self.phones:
            if phone == p.value:
                self.phones.remove(p)

    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones:
            if phone.value == old_phone:
                phone.value = new_phone
                return
        raise ValueError("This phone number not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            next_birthday = datetime(today.year + 1, self.birthday.value.month, self.birthday.value.day).date()
        days_until_birthday = (next_birthday - today).days
        return days_until_birthday

    def __str__(self):
        if self.birthday.value:
            return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}" \
                   f"Birthday: {self.birthday}, days to birthday: {self.days_until_birthday}"
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, n):
        list_data = list(self.data.items)
        while len(list_data) > n:
            yield list_data[0:n]
            list_data = list_data[n:]
        yield list_data

    def save_to_file(self, filename):
        with open('address_book.json', 'w') as file:
            json.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open('address_book.json', 'r') as file:
                self.data = json.load(file)
        except FileNotFoundError:
            print('No data found')
            self.data = {}

    def search_contacts(self, request):
        result = []
        for name, record in self.data.items():
            if request.lower() in name.lower():
                result.append(record)
            else:
                for phone in record.phones:
                    if request in phone.value:
                        result.append(record)
                        break
        return result

