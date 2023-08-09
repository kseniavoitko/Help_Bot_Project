from switcher import switcher
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
import pickle
from pathlib import Path
import shutil

notepad = Notepad()

def get_path() -> Path:
    sourse = Path("notes.bin")
    destination = Path.home()
    path = destination.joinpath(sourse)
    open(path, 'a').close()

    return path


path = get_path()

try:
    with open(path, "rb") as f:
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
    title = Title(args[0])
    description = Description(args[1])
    deadline = Deadline(args[2]) if len(args)>2 and args[2]!="" else "" 
    number = notepad.get_number()
    data_create = datetime.now().date().strftime("%d-%m-%Y")
    tag = args[3].strip().split(",") if len(args)>3 else ""
    if len(tag) > 1:
        tags = Tags(tag[0]) 
        rec = Record(number, data_create, title, description, tags, deadline, state="")
        count = 0
        for i in tag:
            if count == 1:
                tags = Tags(i)
                rec.add_tag(tags)
            count = 1
    else:
        tags = Tags(args[3]) if len(args)>3 else ""
        rec = Record(number, data_create, title, description, tags, deadline, state="")
    return notepad.add_record(rec)


@input_error
def change_title_command(*args):
    title = Title(args[1])
    rec: Record = notepad.get(str(args[0]))
    if rec:
        rec.title = title
        return notepad[args[0]]
    return f"No record {args[0]} in notepad"


@input_error
def change_text_command(*args):
    description = Description(args[1])
    rec: Record = notepad.get(str(args[0]))
    if rec:
        rec.description = description
        return notepad[args[0]]
    return f"No record {args[0]} in notepad"


@input_error
def change_deadline_command(*args):
    deadline = Deadline(args[1])
    rec: Record = notepad.get(str(args[0]))
    if rec:
        rec.deadline = deadline
        return notepad[args[0]]
    return f"No record {args[0]} in notepad"


@input_error
def change_state_command(*args):
    state = args[1]
    rec: Record = notepad.get(str(args[0]))
    if rec:
        rec.state = state
        return notepad[args[0]]
    return f"No record {args[0]} in notepad"


@input_error
def change_tag_command(*args):
    old_tag = Tags(args[1].strip())
    new_tag = Tags(args[2].strip()) if len(args)>2 else Tags("")
    rec: Record = notepad.get(str(args[0]))
    if rec:
        return rec.change_tag(old_tag, new_tag)
    return f"No record {args[0]} in notepad"


@input_error
def add_tag_command(*args):
    if args[1] == "":
        return "Give me tag"
    tag = args[1].strip().split(",")
    rec: Record = notepad.get(str(args[0]))
    if rec:
        if len(tag) > 1:
            for i in tag:
                tags = Tags(i)
                text = rec.add_tag(tags)
            return text
        else:
            tags = Tags(args[1])
            return rec.add_tag(tags)
    return f"No record {args[0]} in notepad"


@input_error
def del_command(*args):
    number = args[0]
    rec: Record = notepad.get(str(number))
    if rec:
        return notepad.numerated(number)
    return f"No record {number} in notepad"

def header():
    header = "|{:^6}|{:^12}|{:^18}|{:^60}|{:^12}|{:^9}|{:^6}|{:^18}|".format('Number','Data_create','Title','Description','Deadline','Status','Left','Tags') 
    return header


def str_():
    str_ = "-"*150
    return str_


def show_all_command(*args):
    return f"{str_()}\n{header()}\n{str_()}\n{notepad}\n{str_()}"


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
        print("\n",f"-page {i}-")
        print(f"{str_()}\n{header()}\n{str_()}\n{rec}\n{str_()}") 
    return ""


@input_error
def search_str_command(*args):
    search_str = notepad.search_str(args[0])
    return f"{str_()}\n{header()}\n{str_()}\n{search_str}\n{str_()}"


@input_error
def tag_command(*args):
    tag_list = args[0].strip().split(",")
    tag_str = notepad.tag_str(tag_list)
    if tag_str =="":
        return "Not found"
    return f"{str_()}\n{header()}\n{str_()}\n{tag_str}\n{str_()}" 

def help_command(*args):
    result = ""
    helper = {
            'Допомога': '(help)',
            'Вихід': '(exit, close, bye, good bye, stop)', 
            'Додати запис': '(add) Назва;Зміст;Дедлайн;Тегі,розділені комою',
            'Видалити запис': '(delete, remove) Номер рядка',
            'Перегляд нотатків': '(show all)',
            'Перегляд по сторінкам': '(show pages) Кількість сторінок',
            'Пошук за нотатками': '(search, find) Пошукове слово ',
            'Пошук за тегами': '(tag) Тегі,розділені комою ',
            'Редагувати назву': '(change title) Номер рядка;Нова назва',
            'Редагувати зміст': '(change text) Номер рядка;Новий зміст',
            'Редагувати дедлайн': '(change deadline) Номер рядка;Новий дедлайн',
            'Редагувати статус': '(change state) Номер рядка;примітка',
            'Редагувати тег': '(change tag) Номер рядка;Старий тег;Новий тег',
            'Додати тег': '(+) Номер рядка;Тегі,розділені комою'
            }
    for key,value in helper.items():
        result += f"{key:24}:   {value}\n"
    return result


def exit_command(*args):
    return "Bye"


def unknown_command(*args):
    return "Invalid command"


def hello_command(*args):
    return "How can I help you?>>>"

def switcher_command(*args):
    switcher()


COMMANDS = {
            add_command: ("add", ),
            add_tag_command: ("+", ),
            change_title_command: ("change title", ),
            change_text_command: ("change text", ),
            change_deadline_command: ("change deadline", ),
            change_state_command: ("change state", ),
            change_tag_command: ("change tag", ),
            del_command: ("delete", "remove"),
            hello_command: ("hello", ),
            show_all_command: ("show all", ),
            show_pages_command: ("show pages", ),
            search_str_command: ("search", "find"),
            tag_command: ("tag", "tags"),
            help_command: ("help", "help"),
            exit_command: ("exit", "close", "bye", "good bye", "stop"),
            switcher_command: ("switcher")
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


def parser(text:str):
    for cmd, kwds in COMMANDS.items():
        for kwd in kwds:
            if text.lower().startswith(kwd):
                data = text[len(kwd):].strip().split(";")
                return cmd, data 
    return unknown_command, []


def main():
    print("\033[36m","Hello! Welcome to Notepad! Input help for help\033[0m")


    while True:
        user_input = prompt(">>> ", completer=create_predict())
        cmd, data = parser(user_input)
        result = cmd(*data)
        print(f"\033[36m{result}\033[0m")
        if cmd == exit_command:
            notepad.save_to_file()
            break


if __name__ == "__main__":
    main()
