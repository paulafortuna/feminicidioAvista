from Database import Database
import pandas as pd
from Utils import Utils


class CrawlerPosProcessing:
    """
    This class encapsulates a function for cleaning the database and storing a subset of news.

    """

    @classmethod
    def pos_process_news(cls):
        """
        This class encapsulates a function for cleaning the database and storing a subset of news.
        The pos processing takes care of: erase news without title or text, erase news where the text has less than 4
        wors. Sort news by date and then drop news that have title repeated
        """
        # get from db
        df = Database.get_all_crawled_news(Database.db_news)

        # erase news without title or text
        df = df.loc[df['news_site_title'] != '']
        df = df.loc[df['news_site_text'] != '']

        # erase number words title
        df['title_len'] = df.apply(lambda row: Utils.count_words(row['news_site_title']), axis=1)
        df = df.loc[df['title_len'] > 3]

        # sort by date so that we keep the last news
        df['arquivo_date'] = pd.to_datetime(df.arquivo_date)
        df = df.sort_values(by=['arquivo_date'], ascending=False)
        df = df.set_index(['arquivo_date'])
        df['arquivo_date'] = df.index

        # drop news that have title repeated
        df_title_text = df[['news_site_title']]
        df_title_text = df_title_text.drop_duplicates()
        df = df.loc[df.index.isin(df_title_text.index)]

        # insert in mongo db
        Database.save_posprocessed_crawled_news(Database.db_pos_processed_news,df)


