# # Help Bot

Help bot is a Python library for saving your phone contacts and notes.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Help Bot.

```bash
# pip install help_bot - вписать правильную команду, после pip-intstaller`а
```

## Usage

```python
from switcher import switcher

#Switcher allows you to pick one of 3 modes to work in.

#The contacts mode
contacts

#The notes mode
notes

#The sorter mode
sorter


Contatcs Mode


# We have a polite bot that will welcome you
hello

# Creating a record
add (name of the contact you wish without spaces)

# Adding phone to the record
add_phone (phone number must contain 10 digits and starts with 0 or 12 digits and starts with 380)

# Adding or chaneging birthday
add_birthday (use format dd.mm.yyyy)

# Adding or chaneging email
add_email (the email)

# Adding or chaneging address
add_address (the address)

# Chaging the phone number
change (the previous phone number) (new phone number)

# Allows you to delete contact by its name
del_contact (name)

# Searching for the contacts according to your input
search (name, phone, email, birthday or address)

# Will show all information for all contacts
show all

# Will show you the contacts that will have a birthday within the period in days that you will input
birthdays (period in days)

# Allows you to switch the mode
switcher

# Closing the programm
exit


Notes Mode


# Showing all the functions and their short description
help

# Allowing you to add a note with all the needed information
add (Name; Text; Tags; Deadline)

#Showing all the notes
show all

# Showing all the notes by pages
show pages (amount of notes per page)

# Searching for the notes by the text in it
search (text)

# Searching for the notes by their tags
tag (tags spaced with ,)

# Allows to change the title of the note
change title (note number; new title)

# Allows to change the text of the note
change text (note number; new text)

# Allows to change the deadline of the note
change deadline (note number; new deadline)

# Allows to change the state of the note
change state (note number; new state)

# Allows to add tag to the note
+ (note number; new tags divided by ,)

# Allows to change the tag of the note
change tag (note number; old tag; new tag)

# Deleting the note
delete (Note number)

# Allows you to switch the mode
switcher

# Closing the programm
exit


Sorter Mode


At this moment he has only one function. All you need to do, is to the enter the directory folder.

```

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

[MIT](https://choosealicense.com/licenses/mit/)
