import pickle
from collections import UserDict
from datetime import datetime


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
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        self.__value =  value
        
    def __str__(self) -> str:
        return self.__value
    
    
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
    def __init__(self, number: str, date_create: str, title: Title, description: Description = None, tag: Tags = None, deadline = None, state="") -> None:
        self.number = number
        self.data_create = date_create
        self.title = title
        self.description = description
        self.tags = []
        if tag:
            self.tags.append(tag) 
        self.deadline = deadline
        if not deadline:
            self.deadline = ""
        self.state = state


    def add_tag(self, new_tag:Tags):
        if new_tag in self.tags:
            return f"Tag {new_tag} alredy exists at record {self.number}, all tags: {self.tags}" 
        self.tags.append(new_tag)
        return f"Record {self.number} tags: {self.tags} "
      

    def change_tag(self, old_tag:Tags, new_tag:Tags):
        if new_tag in self.tags:
            return f"Tag {new_tag} alredy exists at record {self.number}" 
        if old_tag in self.tags:
            self.tags[self.tags.index(old_tag)] = new_tag
            return f"Record {self.number} tags: {self.tags}"
        return f"Tag {str(old_tag)} does not exist at record {self.number}"
        

    def days_to_deadline(self):
        if self.deadline:
            day_now = datetime.now().date()
            day_dn = datetime(day=self.deadline.value.day, month=self.deadline.value.month, year=datetime.now().year).date()
            difference = day_dn-day_now
            return difference.days if difference.days>=0 else "-"
        return ""

    def __str__(self) -> str:
        return "|{:>6}|{:^12}|{:<18}|{:<60}|{:^12}|{:^9}|{:^6}|{:<18}|".format(str(self.number), str(self.data_create), str(self.title), str(self.description), 
                                                                         str(self.deadline), str(self.state),str(self.days_to_deadline()),', '.join(str(p) for p in self.tags))
         
 
class Notepad(UserDict):
    def save_to_file(self):
        with open("notes.bin", "wb") as f:
            pickle.dump(self, f)

    def get_number(self):
        result = 0
        for key in self.data:
            result = max(int(key),result)
        result += 1
        return str(result)

    def numerated(self,num):
        for i in range(int(num)+1,len(self)+1):
            rec: Record = self.get(str(i))
            rec.number = str(i-1)
            self.data[str(rec.number)] = rec
        i = self.pop(str(len(self)))
        return f"record {num} deleted success"

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
                result = result + str(self[i]) if result == "" else result + "\n"+str(self[i])
        return result               

    def tag_str(self, search):
        result = ""
        for rec in self.values():
            while True:
                for val in search:
                    if val.strip().lower() in str(rec.tags).lower():
                        result = result + str(rec) if result == "" else result + "\n"+str(rec)
                        break
                break
        return result

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
