from switcher import switcher
from help_bot_classes import (
    AddressBook,
    Name,
    Phone,
    Email,
    Address,
    Record,
    Birthday,
    PhoneError,
    BirthdayError,
    EmailError,
)
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.table import Table
from prompt_toolkit.styles import Style
from pathlib import Path
import shutil


def load_ab() -> AddressBook:
    destination = Path.home()
    sourse = Path("address_book.dat")
    path = destination.joinpath(sourse)
    open(path, "a").close()

    return path


address_book = AddressBook(load_ab())

try:
    address_book.read_from_file()
except:
    pass

table = Table(title="Address book")
console = Console()


def reset_table():
    global table

    table = Table(title="Address book")

    table.add_column("Name", justify="right", style="cyan", no_wrap=True)
    table.add_column("Birthday", style="magenta")
    table.add_column("Phones", justify="right", style="green")
    table.add_column("E-mail", justify="right", style="green")
    table.add_column("Address", justify="right", style="green")


def save_to_file(func):
    def inner(args):
        result = func(args)
        address_book.save_to_file()
        return result

    return inner


def read_from_file(func):
    def inner(args):
        result = func(args)
        address_book.read_from_file()
        return result

    return inner


def input_error(func):
    def inner(args):
        try:
            result = func(args)
            return result
        except IndexError:
            if func.__name__ == "add" or func.__name__ == "change":
                return "Give me name and phone please"
            elif func.__name__ == "phone":
                return "Give me phone please"
            elif func.__name__ == "birthdays":
                return "Give me a number of days please!"
            else:
                return "Wrong parameters!"
        except KeyError:
            if func.__name__ == "phone" or func.__name__ == "change":
                return "Contact doesn't exist"
        except ValueError:
            if func.__name__ == "change":
                return "Contact doesn't exist"
            elif func.__name__ == "birthdays":
                return "Give me a number of days please!"
            else:
                return "Wrong parameters"
        except PhoneError:
            return "Phone must contain 10 digits and starts with 0 or 12 digits and starts with 380"
        except BirthdayError:
            return "Birthday format is dd.mm.yyyy"
        except EmailError:
            return "Please enter your email correctly"

    return inner


def hello(args):
    return "How can I help you?"


@input_error
@save_to_file
def add(args):
    name = Name(args[0])
    rec = Record(name)
    return address_book.add_record(rec)


@input_error
@save_to_file
def add_phone(args):
    name = Name(args[0])
    phone = Phone(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, phone)
    return address_book.add_record(rec)


@input_error
@save_to_file
def add_email(args):
    name = Name(args[0])
    email = Email(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_email(email)
    rec = Record(name, email)
    return address_book.add_record(rec)


@input_error
@save_to_file
def add_birthday(args):
    name = Name(args[0])
    birthday = Birthday(args[1])
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_birthday(birthday)
    rec = Record(name, birthday)
    return address_book.add_record(rec)


@input_error
@save_to_file
def add_address(args):
    name = Name(args[0])
    address_str = "".join(x for x in args[1:])
    address = Address(address_str)
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_address(address)
    rec = Record(name, address)
    return address_book.add_record(rec)


@input_error
@save_to_file
def del_contact(args: str) -> str:
    name = Name(args[0])
    rec: Record = address_book.get(str(name))
    if rec:
        return address_book.del_record(rec)
    return f"No contact {name} in address book"


@input_error
@save_to_file
def change(args):
    """Get 2 phones to change
    or 1 phone to remove"""
    record = address_book.search_record_by_name(args[0])
    try:
        new_phone = Phone(args[2])
        return record.change_phone(args[1], new_phone)
    except:
        return record.remove_phone(args[1])


@input_error
@read_from_file
def search(args):
    reset_table()
    records = address_book.search_record(args[0])
    if not records:
        return f"Contacts not found"
    for rec in records:
        table.add_row(
            str(rec.name),
            str(rec.birthday),
            ", ".join(str(p) for p in rec.phones),
            str(rec.email),
            str(rec.address),
        )

    console = Console()
    console.print(table)

    return ""


@input_error
@read_from_file
def show_all(args):
    page = 0
    count = 0
    count_of_records = int(args[0]) if len(args) else 5
    records = address_book.values()
    if not records:
        return f"No contacts"
    for rec in records:
        if not count:
            page += 1
            print(f"page {page}")
            reset_table()
        if count == count_of_records:
            console = Console()
            console.print(table)
            page += 1
            print(f"page {page}")
            reset_table()
            count = 0
        count += 1
        table.add_row(
            str(rec.name),
            str(rec.birthday),
            ", ".join(str(p) for p in rec.phones),
            str(rec.email),
            str(rec.address),
        )

    console = Console()
    console.print(table)

    return ""


@read_from_file
@input_error
def birthdays(args):
    reset_table()
    days = int(args[0])
    birthdays_list = address_book.birthdays(days)
    if not birthdays_list:
        return f"No birthdays in the next {days} days"
    for rec in birthdays_list:
        table.add_row(
            str(rec.name),
            str(rec.birthday),
            ", ".join(str(p) for p in rec.phones),
            str(rec.email),
            str(rec.address),
        )

    console = Console()
    console.print(table)

    return ""


def no_command(args):
    return "Unknown command"


COMMANDS = {
    "hello": hello,
    "add_phone": add_phone,
    "add_email": add_email,
    "add_birthday": add_birthday,
    "add_address": add_address,
    "add": add,
    "change": change,
    "del contact": del_contact,
    "search": search,
    "show all": show_all,
    "birthdays": birthdays,
    "good bye": exit,
    "close": exit,
    "exit": exit,
    "switcher": switcher,

}


def get_list_predict() -> list:
    list_for_predict = WordCompleter([command for command in COMMANDS.keys()])
    return list_for_predict


def get_style():
    style = Style.from_dict({"": "ansicyan underline"})
    return style


def parser(text: str) -> tuple[callable, list[str]]:
    for key in COMMANDS:
        if text.lower().startswith(key):
            return COMMANDS[key], text.replace(key, "").strip().split()
    return no_command, ""


def main():
    list_for_predict = WordCompleter([command for command in COMMANDS.keys()])
    style = Style.from_dict({"": "ansicyan underline"})
    while True:
        user_input = prompt(">>> ", completer=get_list_predict(), style=get_style())
        command, data = parser(user_input)
        if command == exit:
            print("Buy!")
            break
        result = command(data)
        print(result)


if __name__ == "__main__":
    main()
