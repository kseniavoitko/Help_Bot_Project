from collections import UserDict
from datetime import datetime
import pickle, re


class PhoneError(Exception):
    pass


class BirthdayError(Exception):
    pass


class EmailError(Exception):
    pass


class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    ...


class Phone(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if (len(new_value) == 10 and new_value.startswith("0")) or (
            len(new_value) == 12 and new_value.startswith("380")
        ):
            self.__value = new_value

        else:
            raise PhoneError


class Birthday(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        try:
            self.__value = datetime.strptime(new_value, "%d.%m.%Y")
        except:
            raise BirthdayError

    def __str__(self) -> str:
        return self.value.strftime("%d.%m.%Y")


class Email(Field):
    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if re.match(pattern, new_value):
            self.__value = new_value
        else:
            raise EmailError


class Address(Field):
    ...


class Record:
    def __init__(
        self,
        name: Name,
        phone: Phone = None,
        birthday: Birthday = None,
        email: Email = None,
        address: Address = None,
    ) -> None:
        self.name = name
        self.birthday = birthday
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.email = email
        self.address = address

    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} add to contact {self.name}"
        return f"{phone} present in phones of contact {self.name}"

    def add_email(self, email: Email):
        self.email = email
        return "The email has been changed"

    def add_birthday(self, birthday: Birthday):
        self.birthday = birthday
        return "The birthday has been changed"

    def add_address(self, address: Address):
        self.address = address
        return "The adrress has been changed"

    def change_phone(self, old, new):
        old_ind = [i.value for i in self.phones].index(old)
        self.phones[old_ind] = new
        return "Contact changed"

    def remove_phone(self, phone):
        phone_index = [i.value for i in self.phones].index(phone)
        self.phones.pop(phone_index)
        return "Contact remove"

    def __str__(self) -> str:
        return f"{str(self.name)}"

    def __repr__(self) -> str:
        return str(self)


class AddressBook(UserDict):
    def __init__(self, filename: str):
        UserDict.__init__(self)
        self.filename = filename

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"

    def del_record(self, record: Record) -> str:
        del_rec = self.pop(str(record.name))
        return f"contact {del_rec} has been deleted"

    def show_all_records(self):
        if not len(self):
            return "No contacts"
        return "\n".join([str(i) for i in self.values()])

    def search_record_by_name(self, key):
        return self[key]

    def search_record(self, key):
        result = []
        key = key.lower()
        for rec in self.values():
            found_phones = [str(p) for p in rec.phones if key in str(p)]
            if len(found_phones) > 0:
                result.append(rec)
            if (
                key in str(rec.name).lower()
                or key in str(rec.address).lower()
                or key in str(rec.email).lower()
                or key in str(rec.birthday).lower()
            ):
                result.append(rec)
        return result

    def birthdays(self, days: int):
        current_datetime = datetime.now()
        current_year = current_datetime.year
        result = []
        for rec in self.values():
            if not rec.birthday:
                continue
            birthday = rec.birthday.value
            birthday = birthday.replace(year=current_year)
            if birthday < current_datetime:
                birthday = birthday.replace(year=current_year + 1)
            if 0 <= (birthday - current_datetime).days < days:
                result.append(rec)

        return result

    def iterator(self, n):
        header = "|{:<30}|{:^12}|{:>40}|".format("Name", "Birthday", "Phones") + "\n"
        result = header
        count = 0
        for rec in self.values():
            result += str(rec) + "\n"
            count += 1
            if count >= n:
                yield result
                count = 0
                result = header
        if result:
            yield result

    def save_to_file(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self, file)

    def read_from_file(self):
        with open(self.filename, "rb") as file:
            try:
                self.data = pickle.load(file)
            except:
                pass
