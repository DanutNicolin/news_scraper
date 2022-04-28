
from src.scraper import Digi24
from src.commands import Command
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


def get_scraper():
    print_websites()
    chosen_option = get_option_choice(scrapers)
    return chosen_option

    
def get_keyword():
    keyword = input('Input keyword: ')
    return keyword


def get_scraper_and_keyword():
    scraper = get_scraper()
    keyword = get_keyword()
    data = (scraper, keyword)
    return data


def print_menu(menu: dict):
    print('')
    for (option, name) in zip(menu.keys(), menu.values()):
        print(f'{option} {name}')
    print('')



def option_choice_is_valid(choice: str, options: dict):
    if choice.upper() in options.keys():
        return True
    else:
        return False


def get_option_choice(options: dict) -> Option:
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice!")
        choice = input("Choose an option: ")
    return options[choice.upper()]