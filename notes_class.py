import pickle
from collections import UserDict
from datetime import datetime
from pathlib import Path


class DeadlineError(Exception):
    ...


class Field:
    def __init__(self, value) -> None:
        self.value = value

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other):
        return self.value == other.value


class Tags(Field):
    ...


class Title(Field):
    ...


class Description(Field):
    ...


class Deadline(Field):
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            self.__value = datetime.strptime(value, "%d-%m-%Y")
        except ValueError:
            raise DeadlineError

    def __str__(self) -> str:
        return self.__value.strftime("%d-%m-%Y")


class Record:
    def __init__(
        self,
        number: str,
        date_create: str,
        name: Title,
        description: Description = None,
        tag: Tags = None,
        deadline=None,
        state=bool,
    ) -> None:
        self.number = number
        self.data_create = date_create
        self.name = name
        self.description = description
        self.tags = []
        if tag:
            self.tags.append(tag)
        self.deadline = deadline
        if not deadline:
            self.deadline = ""
        self.state = state

    def days_to_deadline(self):
        if self.deadline:
            day_now = datetime.now().date()
            day_dn = datetime(
                day=self.deadline.value.day,
                month=self.deadline.value.month,
                year=datetime.now().year,
            ).date()
            if day_now > day_dn:
                day_dn = datetime(
                    day=self.deadline.value.day,
                    month=self.deadline.value.month,
                    year=datetime.now().year + 1,
                ).date()
            difference = day_dn - day_now
            return difference.days if difference.days >= 0 else ""
        return ""

    def __str__(self) -> str:
        return "{:>6} {:^12} {:<18} {:<60} {:<12} {:^12} {:^6} {:^6}".format(
            str(self.number),
            str(self.data_create),
            str(self.name),
            str(self.description),
            ", ".join(str(p) for p in self.tags),
            str(self.deadline),
            "+" if self.state == True else "",
            str(self.days_to_deadline()),
        )


class Notepad(UserDict):
    def save_to_file(self):
        sourse = Path("notes.bin")
        destination = Path.home()
        path = destination.joinpath(sourse)
        open(path, 'a').close()
        with open(path, "wb") as f:
            pickle.dump(self, f)

    def number(self):
        result = 0
        for key in self.data:
            result = max(int(key), result)
        result += 1
        return result

    def add_record(self, record: Record):
        self.data[str(record.number)] = record
        self.save_to_file()
        return "added success"

    def iterator(self, n=5):
        result = []
        count = 0
        for rec in self.data:
            result.append(str(self.data[rec]))
            count += 1
            if count >= n:
                yield "\n".join(result)
                count = 0
                result = []
        if result:
            yield "\n".join(result)

    def search_str(self, search):
        result = ""
        for i in self:
            if search.lower() in str(self[i]).lower():
                result += str(self[i]) + "\n"
        return result

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
