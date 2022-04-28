
from matplotlib.pyplot import plot
from src.business import (
    get_all_titles,
    get_titles_from_db,
    db,
    create_table,
    check_if_title_in_db,
    add_title_in_db,
    parsing_titles,
    plot_data
    )
from src.utils import clear_screen
import sys





class Command:
    def execute(self):
        raise NotImplementedError()





class GetAllTitles:
    def execute(self, scraper):
        clear_screen()
        extracted_titles = get_all_titles(scraper)
        return extracted_titles


class PrintAllTitles: 
    def execute(self, scraper):
        clear_screen()
        extracted_titles = GetAllTitles().execute(scraper)
        for title in extracted_titles:
            print(title)




        
class SearchKeyword:
    def execute(self, scraper, keyword: str):
        all_titles = GetAllTitles().execute(scraper)
        filtered_titles = []

        for title in all_titles:
            if keyword in title:
                filtered_titles.append(title)
        return filtered_titles


class PrintKeywords:
    def execute(self, scraper, keyword:str):
        filtered_titles = SearchKeyword().execute(scraper, keyword)
        clear_screen()
        if len(filtered_titles)>0:
            for title in filtered_titles:
                print(title)
        else:
            print(f'No title found with {keyword} keyword')





class Exit:
    def execute(self):
        sys.exit()





class GetDbTitles:
    def execute(self, table_name:str):
        titles = get_titles_from_db(table_name)
        return titles
        

class WriteToDataBase:
  def execute(self, scraper):
        create_table(str(scraper))

        scraper_titles = GetAllTitles().execute(scraper)
        db_titles = GetDbTitles().execute(str(scraper))

        titles_not_in_db = check_if_title_in_db(scraper_titles, db_titles)

        loop_criteria = True if len(titles_not_in_db)>=1 else False

        if loop_criteria is True:
            for title in titles_not_in_db:
                add_title_in_db(scraper, title)
                print('Title added in database')




class GetWordCount:
    def execute(self, table_name):
        counted_words = parsing_titles(str(table_name))
        return counted_words

class PlotData:
    def execute(self, table_name):
        data = GetWordCount().execute(table_name)
        plot_data(data)
