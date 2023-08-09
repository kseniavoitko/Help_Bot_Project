def switcher(*args):
    from note import main as note_mode
    from sorter import main as sorter_mode
    from help_bot import main as contacts_mode

    print("Print switch [mode] to choose your mode:\n [1]: contacts \n [2]: notes \n [3]: sorter")

    while True:
        mode = int(input('>>> '))
        if mode == 1:
            print("Contact mode enabled")
            contacts_mode()
        elif mode == 2:
            print("Notes mode enabled")
            note_mode()
        elif mode == 3:
            print("Sorter mode enabled")
            sorter_mode()
        else:
            print("Invalid mode argument")
            
            
if __name__ == "__main__":
    switcher()