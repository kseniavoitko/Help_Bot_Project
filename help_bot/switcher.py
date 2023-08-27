def main(*args):
    import sys
    from help_bot.note import main as note_mode
    from help_bot.sorter import main as sorter_mode
    from help_bot.help_bot import main as contacts_mode
    from help_bot.output_classes import (
        TerminalOutput,
        TelegramOutput,
        Commands_Handler,
    )

    terminal_out = TerminalOutput()

    terminal_handler = Commands_Handler(terminal_out)

    terminal_handler.send_message(
        "Print [number] or [name] of mode to choose your one:\n [1]: [contacts] \n [2]: [notes] \n [3]: [sorter]"
    )

    while True:
        mode = input(">>> ")
        if mode == "1" or mode == "contacts":
            terminal_handler.send_message("Contact mode enabled")
            contacts_mode()
            sys.exit()
        elif mode == "2" or mode == "notes":
            terminal_handler.send_message("Notes mode enabled")
            note_mode()
            sys.exit()
        elif mode == "3" or mode == "sorter":
            terminal_handler.send_message("Sorter mode enabled")
            sorter_mode()
            sys.exit()
        else:
            terminal_handler.send_message("Invalid mode argument")


if __name__ == "__main__":
    main()
