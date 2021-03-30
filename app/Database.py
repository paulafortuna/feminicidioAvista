from pymongo import MongoClient
import pandas as pd
import json
import datetime
from pandas import DataFrame


class Database:
    """
    This class encapsulates all the connections and queries to the mongodb where the collected news are stored.
    """
    # open connection
    client = MongoClient(host='db', port=27017)

    # get db and collections
    db = client['arquivo_feminicidio']
    db_crawler = db['crawler']
    db_news = db['news']
    db_pos_processed_news = db['pos_processed_news']
    db_keywords_news = db['keywords_news']
    db_annotated_news = db['annotated_news']

    @classmethod
    def put_into_database(cls, db_news, news):
        '''
        Directly inserts news in the database.

        Arguments
        ----------
        db_news : The database news table where to insert.
        news : The news object to insert.
        '''
        # transfer dataframe to database
        db_news.insert(news)

    @classmethod
    def save_crawler(cls, db_crawler, id, newspaper, keyword, offset, year):
        """
        Puts all crawler data in a dictionary and inserts it in the database.

        Arguments
        ----------
        db_crawler : The database crawler table where to update.
        id : The id of the crawler to update.
        newspaper : The newspaper of the crawler to update.
        keyword : The keyword of the crawler to update.
        offset : The offset of the crawler to update.
        year : The year of the crawler to update.
        """
        register_crawler = {'id': id,
                            'current_newspaper': newspaper,
                            'keyword': keyword,
                            'offset': offset,
                            'year': year
                            }
        db_crawler.insert(register_crawler)

    @classmethod
    def update_crawler(cls, db_crawler, id, newspaper, keyword, offset, year):
        """
        Updates all crawler data in a dictionary and inserts it in the database.

        Arguments
        ----------
        db_crawler : The database crawler table where to insert.
        id : The id of the crawler to insert.
        newspaper : The newspaper of the crawler to insert.
        keyword : The keyword of the crawler to insert.
        offset : The offset of the crawler to insert.
        year : The year of the crawler to insert.
        """
        register_crawler = {'id': id,
                            'current_newspaper': newspaper,
                            'keyword': keyword,
                            'offset': offset,
                            'year': year
                            }
        db_crawler.update_one({"id": id},
                              {"$set": register_crawler})

    @classmethod
    def starting_crawler(cls, db_crawler, id, newspaper, keyword, offset, year):
        '''
        Method that starts a crawler in the database.
        If crawler with id already exists in the database, reads properties.
        If does not exist creates new.

        Arguments
        ----------
        db_crawler : The database crawler table where to insert.
        id : The id of the crawler to insert.
        newspaper : The newspaper of the crawler to insert.
        keyword : The keyword of the crawler to insert.
        offset : The offset of the crawler to insert.
        year : The year of the crawler to insert.

        Return
        ----------
        crawler_json : is a dictionary with crawler properties
        '''
        # if a register for the crawler does not exist in the database create one
        crawler_json = db_crawler.find_one({"id": id})
        if crawler_json is None:
            Database.save_crawler(db_crawler, id, newspaper, keyword, offset, year)
            crawler_json = db_crawler.find_one({"id": id})
        return crawler_json

    @classmethod
    def news_exist(cls, db_news, news_json):
        """
        Check if news exist in db.

        Arguments
        ----------
        db_news : The database news table where to check.
        news : The news object to check.
        """
        crawler_json = db_news.find_one({"arquivo_hash": news_json['arquivo_hash']})
        if crawler_json is None:
            return False
        return True

    @classmethod
    def get_all_crawled_news(cls, db_news):
        """
        Get all the news in the database.

        Arguments
        ----------
        db_news : The database news table where to check.

        Return
        ----------
        df : A pandas dataframe with all the news in the database.
        """
        df = pd.DataFrame(list(db_news.find()))
        return df

    @classmethod
    def save_posprocessed_crawled_news(cls, db_pos_processed_news, df):

        # erase dates that are problematic for mongo db
        df['arquivo_date'] = df['arquivo_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['news_site_date'] = df['news_site_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df.reset_index(drop=True, inplace=True)

        # rename id mongo column
        df = df.rename(columns={'_id': 'news_table_id'})

        # insert in database
        db_pos_processed_news.insert_many(df.to_dict('records'))

    @classmethod
    def save_initialized_keywords_news(cls, db_keywords_news, df):

        # rename id mongo column
        df = df.rename(columns={'_id': 'pos_processed_news'})

        # insert in database
        db_keywords_news.insert_many(df.to_dict('records'))

    @classmethod
    def save_keywords_news(cls, db_pos_processed_news, df):

        # erase dates that are problematic for mongo db
        df['arquivo_date'] = df['arquivo_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df['news_site_date'] = df['news_site_date'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df.reset_index(drop=True, inplace=True)

        # rename id mongo column
        df = df.rename(columns={'_id': 'news_table_id'})

        # insert in database
        db_pos_processed_news.insert_many(df.to_dict('records'))

    @classmethod
    def get_all_posprocessed_crawled_news(cls, db_pos_processed_news):
        df = pd.DataFrame(list(db_pos_processed_news.find()))
        return df

    @classmethod
    def get_all_non_keyword_annotated_news(cls, db_keywords_news):
        result = db_keywords_news.find({
            "search_keywords": {"$eq": False}
        })
        return pd.DataFrame(list(result))

    @classmethod
    def update_keyword_annotated_news(cls, db_keywords_news, df):

        bulk_operation = db_keywords_news.initialize_unordered_bulk_op()

        # Address filed to be added to all documents
        for iter, row in df.iterrows():
            bulk_operation.find({'_id': row['_id']}).update({'$set': {'feminicidio': row['feminicidio'],
                                                                      'violencia_domestica': row['violencia_domestica'],
                                                                      'violencia_sexual': row['violencia_sexual'],
                                                                      'assedio_sexual': row['assedio_sexual'],
                                                                      'mulheres_assassinadas': row['mulheres_assassinadas'],
                                                                      'search_keywords': row['search_keywords']
                                                                      }})
        bulk_operation.execute()

    @classmethod
    def get_all_keyword_murdered_women_news(cls, db_keywords_news):
        result = db_keywords_news.find({
            "mulheres_assassinadas": {"$eq": True}
        })
        return pd.DataFrame(list(result))
