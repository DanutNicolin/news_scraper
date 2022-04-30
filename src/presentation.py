
from src.scraper import Digi24
from src.commands import Command
from src.business import option_choice_is_valid, get_option_choice
from typing import Optional, Callable, Union






scrapers = {  'A': 'Adevarul',
              'B': Digi24(),
              'C': 'Mediafax',
              'D': 'Stirile ProTv',
              'E': 'Libertatea'
            }

class Option:
    def __init__(
        self,
        name: str,
        command: Command,
        prep_call: Optional[Callable]=None
    ):
        self.name = name
        self.command = command
        self.prep_call = prep_call

    def _handle_message(self, message: Union[str, list]):
        if isinstance(message, list):
            for entry in message:
                print(entry)
        else:
            print(message)

    def choose(self):
        data = None
        if self.prep_call:
            data = self.prep_call()
        if data:
            try:
                message = self.command.execute(data)
            except:
                message = self.command.execute(data[0], data[1])
        else:
            message = self.command.execute()
        print()

    def __str__(self):
        return self.name




def print_websites():
    for website in scrapers.items():
        print(website[0], website[1])
    print()


def print_menu(menu: dict):
    print('')
    for (option, name) in zip(menu.keys(), menu.values()):
        print(f'{option} {name}')
    print('')



def get_scraper():
    print_websites()
    chosen_option = get_option_choice(scrapers)
    return chosen_option

