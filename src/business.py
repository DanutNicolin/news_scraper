
from src.scraper import Digi24
from collections import defaultdict
from src.database import DataBaseManager
from matplotlib import pyplot as plt
import re


digi24 = Digi24()
db = DataBaseManager('database.db')

def get_all_titles(scraper):
    extracted_titles = []
    all_titles = scraper.scrape_titles()
    for title in all_titles:
        extracted_titles.append(title.strip())
    return extracted_titles


def get_titles_from_db(table_name: str):
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
     'ba', 'fie', 'cum', 'cu', 'cât', 'precum', 'așadar', 'prin', 'urmare', 'în', 'la']

    all_titles = get_titles_from_db(table_name)
    counts = defaultdict(int)
 
    for title in all_titles:
        for word in re.findall('\w+', title):
            if word in CONJUNCTIONS:
                continue
            else:
                counts[word] += 1
    return dict(counts)


def plot_data(data: dict):

    words = list(data.keys())
    count = list(data.values())

    plt.plot(words, count)

    plt.xlabel('Number of ocurencyes')
    plt.ylabel('Words')
    plt.title('Word frequency count')

    plt.show()


# def top_5_words(table_name: str):
#     all_titles = get_titles_from_db(table_name)



