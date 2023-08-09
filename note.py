from notes_class import (
    Notepad,
    Deadline,
    Title,
    Description,
    Tags,
    Record,
    DeadlineError,
)
from datetime import datetime
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
import pickle, socket
from pathlib import Path


notepad = Notepad()


def get_path() -> Path:
    hostname = socket.gethostname()
    sourse = Path("notes.bin")
    destination = Path(f"C:\\Users\\{hostname}\\Documents")
    path = destination.joinpath(sourse)
    open(path, "a").close()
    return path


try:
    with open(get_path(), "rb") as f:
        try:
            notepad = pickle.load(f)
        except EOFError:
            print('File "notes.bin" EOFError')
        except pickle.UnpicklingError:
            print('File "notes.bin" pickle.UnpicklingError')
except FileNotFoundError:
    print('File "notes.bin" FileNotFoundError')


def input_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
        except KeyError:
            result = "This name does not exist."
        except DeadlineError:
            result = f'Not added. False deadline format. Input "dd-mm-yyyy"'
        except ValueError:
            result = "ValueError"
        except IndexError:
            result = "Give me parameters please."
        return result

    return wrapper


@input_error
def add_command(*args):
    name = Title(args[0])
    description = Description(args[1])
    tags = Tags(args[2]) if len(args) > 2 else ""
    deadline = Deadline(args[3]) if len(args) > 3 else ""
    number = notepad.number()
    data_create = datetime.now().date().strftime("%d-%m-%Y")
    rec = Record(number, data_create, name, description, tags, deadline, state=False)
    return notepad.add_record(rec)


def show_all_command(*args):
    header = "{:^6} {:^12} {:^18} {:^60} {:^12} {:^12} {:^6} {:^6}".format(
        "Number",
        "Data_create",
        "Title",
        "Description",
        "Tags",
        "Deadline",
        "Status",
        "Left",
    )
    return f"{header}\n{notepad}"


def show_pages_command(*args):
    try:
        page = int(args[0])
    except ValueError:
        page = 5
    except IndexError:
        page = 5

    i = 0
    for rec in notepad.iterator(page):
        i += 1
        print("\n", f"-page {i}-")
        print(rec)
    return ""


@input_error
def search_str_command(*args):
    search_str = notepad.search_str(args[0])
    return search_str


def help_command(*args):
    result = ""
    helper = {
        "Допомога": "(help)",
        "Додати запис": "(add, +) Назва;Зміст;Тег;Дедлайн",
        "Перегляд нотатків": "(show all)",
        "Перегляд по сторінкам": "(show pages) Кількість сторінок",
        "Пошук за нотатками": "(search, find) Рядок",
        "Вихід": "(exit, close, bye, good bye, stop)",
    }
    for key, value in helper.items():
        result += f"{key:24}:   {value}\n"
    return result


def exit_command(*args):
    return "Bye"


def unknown_command(*args):
    return "Invalid command"


def hello_command(*args):
    return "How can I help you?>>>"


COMMANDS = {
    add_command: ("add", "+"),
    hello_command: ("hello",),
    show_all_command: ("show all",),
    show_pages_command: ("show pages",),
    search_str_command: ("search", "find"),
    help_command: ("help",),
    exit_command: ("exit", "close", "bye", "good bye", "stop"),
}


def create_predict() -> None:
    list_for_predict = []
    for values in COMMANDS.values():
        if values == 1:
            list_for_predict.append(values)
        else:
            for value in values:
                list_for_predict.append(value)

    list_for_predict = WordCompleter(list_for_predict)

    return list_for_predict


def parser(text: str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd) :].strip().split(";")
                return cmd, data
    return unknown_command, []


def main():
    print("Hello!")

    while True:
        user_input = prompt(">>> ", completer=create_predict())
        cmd, data = parser(user_input)
        result = cmd(*data)
        print(result)

        if cmd == exit_command:
            notepad.save_to_file()
            break


if __name__ == "__main__":
    main()
