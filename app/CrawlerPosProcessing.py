from Database import Database
import re
import pandas as pd
import spacy
from Utils import Utils
from Variables import Variables
import requests
import json
import time
from datetime import date

from newspaper import Article


class CrawlerPosProcessing:

    @classmethod
    def pos_process_news(cls):

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

    @classmethod
    def pos_process_news_old(cls):

        df = Database.get_all_crawled_news(Database.db_news)

        # erase news without title or text
        df = df.loc[df['news_site_title'] != '']
        df = df.loc[df['news_site_text'] != '']

        # erase number words title
        df['title_len'] = df.apply(lambda row: CrawlerPosProcessing.count_words(row['news_site_title']), axis=1)
        df = df.loc[df['title_len'] > 3]

        # drop news that have title and text repeated
        df_title_text = df[['news_site_title','news_site_text']]
        df_title_text = df_title_text.drop_duplicates()
        df = df.loc[df.index.isin(df_title_text.index)]

        # compute a percentage of similitude between two texts we above thresold 0.98 we consider same news
        # for all the news see if the news already exists in the database
        # by comparing with news from same newspaper, in the past 1 year
        df['arquivo_date'] = pd.to_datetime(df.arquivo_date)
        df = df.sort_values(by=['arquivo_date'],ascending=False)
        df = df.set_index(['arquivo_date'])
        df['arquivo_date'] = df.index
        df['state'] = 'no_copy'

        nlp = spacy.load('pt_core_news_sm')
        for i in range(0,df.shape[0]-1):
            print(i)
            news_date = df.iloc[i]['arquivo_date']
            candidate_news = df.loc[news_date:news_date - pd.Timedelta(days=365)]
            for j in range(1, candidate_news.shape[0]-1):
                if candidate_news.iloc[j]['state'] == 'no_copy':
                    doc_1 = nlp(df.iloc[i]['news_site_text'])
                    doc_2 = nlp(candidate_news.iloc[j]['news_site_text'])
                    similarity = doc_1.similarity(doc_2)
                    print(similarity)
                    if similarity > 0.99:
                        df.loc[df['_id'] == candidate_news.iloc[j]['_id'], 'state'] = df.iloc[i]['_id']

        df_title = df[['news_site_title']]
        df_title = df_title.drop_duplicates()
        df = df.loc[~df.index.isin(df_title.index)]

        df = df.sort_values(by=['news_site_title']).head(10)

        for iterator1,row1 in df.iterrows():
            for iterator2, row2 in df.iterrows():
                print(row1['news_site_title'])
                print(row2['news_site_title'])
                doc_1 = nlp(row1['news_site_text'])
                doc_2 = nlp(row2['news_site_text'])
                print(doc_1.similarity(doc_2))


        #print(df)


c = CrawlerPosProcessing()
c.pos_process_news()
