
from collections import defaultdict
from typing import Optional
from src.scraper import Digi24
from src.database import DataBaseManager
from matplotlib import pyplot as plt
from operator import itemgetter
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




def get_all_titles(scraper):
    extracted_titles = []
    all_titles = scraper.scrape_titles()
    for title in all_titles:
        extracted_titles.append(title.strip())
    return extracted_titles


def get_titles_from_db(table_name: str, date: Optional[str]=None):
    if date:
        db_data = db.retrieve_data(table_name, date)
    else:
        db_data = db.retrieve_data(table_name)

    titles = []
    for title in db_data:
        titles.append(title[2].strip())
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


def parsing_titles(table_name: str):
    CONJUNCTIONS = ['și', 'nici', 'de', 'sau', 'ori', 'dacă', 'fiindcă', 'iar', 'dar', 'însă', 'ci', 'deci', 'că', 'să', 'ca', 'căci', 'deși', 'încât', 'deoarece',
     'ba', 'fie', 'cum', 'cu', 'cât', 'precum', 'așadar', 'prin', 'urmare', 'în', 'la', 'au', 'o', 'a', 'un', 'din', 'pentru', 'ce', 'cum', 'pe', 'sub', 'care', 'fost', 's',
     'înainte', 'după','ar', 'la', 'din', 'te', 'mai', 'vai', 'se', 'al', 'fi', 'nu', 'da', 'va', 'vă', 'îl', 'este', 'si', 'e', 'sunt', 'despre']

    all_titles = get_titles_from_db(table_name)
    counts = defaultdict(int)
 
    for title in all_titles:
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


def plot_data(data: dict):
    words = list(data.keys())
    count = list(data.values())

    plt.bar(words, count)

    plt.xlabel('Words')
    plt.ylabel('Number of ocurencyes')
    plt.title(f'Word frequency count {curent_date}')

    plt.show()
