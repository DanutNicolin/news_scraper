
from collections import defaultdict
from typing import Optional
from src.scraper import Digi24
from src.database import DataBaseManager
from matplotlib import pyplot as plt
from operator import itemgetter
from src.utils import clear_screen
import re


digi24 = Digi24()
db = DataBaseManager('database.db')
curent_date = str(digi24.curent_date())


def option_choice_is_valid(choice: str, options: dict):
    if choice.upper() in options.keys():
        return True
    else:
        return False


def get_option_choice(options: dict):
    choice = input("Choose an option: ")
    while not option_choice_is_valid(choice, options):
        print("Invalid choice!")
        choice = input("Choose an option: ")
    return options[choice.upper()]


def get_date():
    options = {'A': '- Curent date', 'B': '- Input date', 'C': '- All the dates'}
    for option in options.items():
        print(option[0], option[1])
    print('')
        
    choice = get_option_choice(options)
    clear_screen()
    
    if choice == '- All the dates':
        return None
    if choice == '- Curent date':
        return curent_date
    if choice == '- Input date':
        date = str(input('Input date (dd.mm.yyyy): '))
        return date




def get_all_titles(scraper):
    extracted_titles = []
    all_titles = scraper.scrape_titles()
    for title in all_titles:
        extracted_titles.append(title.strip())
    return extracted_titles


def get_date_from_db(table_name: str):
    db_data = db.retrieve_data(table_name)

    dates = []
    for date in db_data:
        dates.append(date[1])
    return dates



def get_titles_from_db(table_name: str, date: Optional[str]=None):
    db_data = db.retrieve_data(table_name, date)

    titles = []
    for data in db_data:
        titles.append(data[2].strip())
    return titles


def create_table(table_name: str):
    db.create_table(table_name)

def check_if_title_in_db(scraper_titles: list, db_titles: list):
    unsaved_titles = []

    for s_title in scraper_titles:
        if s_title in db_titles:
            print('Titles already in db')
        else:
            unsaved_titles.append(s_title)
    return unsaved_titles

        
def add_title_in_db(scraper, title: str):
    db.add_data(str(scraper), title)


def parse_titles(titles: list):
    CONJUNCTIONS = ['și', 'nici', 'de', 'sau', 'ori', 'dacă', 'fiindcă', 'iar', 'dar', 'însă', 'ci', 'deci', 'că', 'să', 'ca', 'căci', 'deși', 'încât', 'deoarece',
     'ba', 'fie', 'cum', 'cu', 'cât', 'precum', 'așadar', 'prin', 'urmare', 'în', 'la', 'au', 'o', 'a', 'un', 'din', 'pentru', 'ce', 'cum', 'pe', 'sub', 'care', 'fost', 's',
     'înainte', 'după','ar', 'la', 'din', 'te', 'mai', 'vai', 'se', 'al', 'fi', 'nu', 'da', 'va', 'vă', 'îl', 'este', 'si', 'e', 'sunt', 'despre', 'i', 'asupra', 'putea', 'vor']

    # all_titles = get_titles_from_db(table_name, date)
    counts = defaultdict(int)
 
    for title in titles:
        for word in re.findall('\w+', title.lower()):
            if word in CONJUNCTIONS:
                continue
            else:
                counts[word] += 1
    # counts = sorted(counts.items(), key=lambda x:x[1])
    return dict(counts)


def get_top_words(words: dict, n: int):
    top_n_words = dict(sorted(words.items(), key = itemgetter(1), reverse = True)[:n])
    return top_n_words


def plot_data(data: dict, date: str, db_date: list):
    db_date = [db_date[0], db_date[-1]]

    if date == None:
        date = f' between {db_date[0]} - {db_date[1]}'

    words = list(data.keys())
    count = list(data.values())

    plt.bar(words, count)

    plt.xlabel('Words')
    plt.ylabel('Number of ocurencyes')
    plt.title(f'Word frequency {date}')

    plt.show()
