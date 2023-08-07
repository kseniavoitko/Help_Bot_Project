from help_bot_classes import (
    AddressBook,
    Name,
    Phone,
    Record,
    Birthday,
    PhoneError,
    BirthdayError,
)
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from rich.console import Console
from rich.table import Table
from prompt_toolkit.styles import Style


address_book = AddressBook("address_book.dat")
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

    return inner


def hello(args):
    return "How can I help you?"


@input_error
@save_to_file
def add(args):
    name = Name(args[0])
    phone = None
    birthday = None
    for a in args[1:]:
        if a.isdigit():
            phone = Phone(a)
        else:
            birthday = Birthday(a)
    rec: Record = address_book.get(str(name))
    if rec:
        return rec.add_phone(phone)
    rec = Record(name, birthday, phone)
    return address_book.add_record(rec)


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
def phone(args):
    result = "No contacts"
    for rec in address_book.search_record(args[0]):
        print(rec)
        result = ""
    return result


@input_error
@read_from_file
def show_all(args):
    page = 0
    result = "No contacts"
    for rec in address_book.iterator(int(args[0]) if len(args) else 5):
        page += 1
        print(f"page {page}")
        print(rec)
        result = "END"

    return result


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
            str(rec.name), str(rec.birthday), ", ".join(str(p) for p in rec.phones)
        )

    console = Console()
    console.print(table)

    return ""


def no_command(args):
    return "Unknown command"


COMMANDS = {
    "hello": hello,
    "add": add,
    "change": change,
    "phone": phone,
    "show all": show_all,
    "birthdays": birthdays,
    "good bye": exit,
    "close": exit,
    "exit": exit,
}


def parser(text: str) -> tuple[callable, list[str]]:
    for key in COMMANDS:
        if text.lower().startswith(key):
            return COMMANDS[key], text.replace(key, "").strip().split()
    return no_command, ""


def main():
    while True:
        user_input = prompt(">>> ", completer=list_for_predict, style=style)
        command, data = parser(user_input)
        if command == exit:
            print("Buy!")
            break
        result = command(data)
        print(result)


if __name__ == "__main__":
    list_for_predict = WordCompleter([command for command in COMMANDS.keys()])
    style = Style.from_dict({"": "ansicyan underline"})
    main()
