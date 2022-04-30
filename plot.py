import matplotlib.pyplot as plt
import numpy as np

from src.commands import GetWordCount
from src.business import parsing_titles, get_top_words

data = GetWordCount().execute('Digi24')


def plot_data(data, n):
    n = int(input('Number of words to plot: '))
    scrapers = ['Adevarul',
               'Digi24',
               'Mediafax',
               'Stirile ProTv',
               'Libertatea']

    top_words = get_top_words(data, n)
    top_words_keys = [top_words.keys()]

    labels = [top_words]

    cols = {}

    fig, ax = plt.subplots()

    x = np.arange(len(labels))  # the label locations
    width = 0.35  # the width of the bars

    for scraper in scrapers:
        col = ax.bar(x - width/2, scraper, width, label=str(scraper))
        cols.setdefault(scraper, col)

  




    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Word frequency')
    ax.set_title('Word frequency graph')
    ax.set_xticks(x, labels)
    ax.legend()

    for index,col in enumerate(cols.items()):
        print(type(col[1]))
        ax.bar_label(col[1], padding=3)


    fig.tight_layout()

    plt.show()

plot_data(data, 5)