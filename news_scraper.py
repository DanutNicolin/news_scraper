
from src.presentation import (
 Option,
 print_menu, 
 get_scraper, 
 )
from src.business import (
get_option_choice
)

from src.commands import PrintAllTitles, PrintKeywords, Exit, WriteToDataBase, PlotData
from src.utils import clear_terminal



def loop():
    with clear_terminal():      
        options = {
            'A': Option('- Print todays news', PrintAllTitles(), prep_call=get_scraper),
            'B': Option('- Search by key word', PrintKeywords(), prep_call=get_scraper),
            'C': Option('- Add all titles to database', WriteToDataBase(), prep_call=get_scraper),
            'D': Option('- Plot words count', PlotData(), prep_call=get_scraper),
            'X': Option('- Exit', Exit())
        }   
        print_menu(options)
        chosen_option = get_option_choice(options)

    chosen_option.choose()
    _ = input("Press ENTER to return to menu.")


if __name__ == '__main__':
    print('Welcome to NewsScraper')

    while True:
        loop()