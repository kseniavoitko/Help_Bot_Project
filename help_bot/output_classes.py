from abc import ABC


class Telegram:
    def __init__(self, token):
        self.token = token

    def send_message(self, text):
        print(text)


class ConsoleOutputAbstract(ABC):
    def output(self, text: str, *args) -> str:
        ...


class TerminalOutput(ConsoleOutputAbstract):
    def output(self, text: str, *args) -> None:
        print(text)


class TelegramOutput(ConsoleOutputAbstract):
    def __init__(self, token) -> None:
        self.telegram_client = Telegram(token)

    def output(self, text: str, *args) -> None:
        self.telegram_client.send_message(text)


class Commands_Handler:
    def __init__(self, command_output: ConsoleOutputAbstract):
        self.__output_processor = command_output

    def send_message(self, message) -> None:
        self.__output_processor.output(message)
