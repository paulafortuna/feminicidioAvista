from Database import Database
from Variables import Variables
import requests
import json
import time
from datetime import date

from newspaper import Article


class Crawler:
    # variables
    crawler_id = 0
    db_keyword = Variables.keywords[0]
    db_newspaper = Variables.newspaper_list[0]
    db_offset = 0
    db_year = 1996

    maxItems = 200
    arquivo_start_year = 1996
    to_year = date.today().year
    dedupValue = 20

    sleep = 0.31
    N_attempts = 3

    def __init__(self, crawler_id):
        Crawler.crawler_id = crawler_id
        # if it exists read from database state from crawler or create a new register
        crawler_json = Database.starting_crawler(Database.db_crawler,
                                                 crawler_id,
                                                 Crawler.db_newspaper,
                                                 Crawler.db_keyword,
                                                 Crawler.db_offset,
                                                 Crawler.arquivo_start_year)
        Crawler.db_keyword = crawler_json['keyword']
        Crawler.db_newspaper = crawler_json['current_newspaper']
        Crawler.db_offset = crawler_json['offset']
        Crawler.db_year = crawler_json['year']

    @classmethod
    def process_news_url_to_json(cls, news_item, newspaper):
        print(news_item)
        #print(news_item['fileName'])
        #print(news_item['tstamp'])
        url = news_item['linkToNoFrame']
        try:
            news_article = Article(url, language="pt")
            news_article.download()
            news_article.parse()
            new_news_article = {'id': news_item['fileName'],
                                'arquivo_date': news_item['tstamp'],
                                'arquivo_hash': news_item['digest'],
                                'news_link': news_item['linkToNoFrame'],
                                'news_site_date': news_article.publish_date,
                                'news_site_title': news_article.title,
                                'news_site_authors': news_article.authors,
                                'news_site_text': news_article.text,
                                'search_newspaper': newspaper,
                                }
        except:
            new_news_article = {'id': news_item['fileName'],
                                'arquivo_date': news_item['tstamp'],
                                'arquivo_hash': news_item['digest'],
                                'news_link': news_item['linkToNoFrame'],
                                'news_site_date': "",
                                'news_site_title': "",
                                'news_site_authors': "",
                                'news_site_text': "",
                                'search_newspaper': newspaper,
                                }
        return new_news_article

    ################################
    # News crawler
    ################################
    @classmethod
    def crawling(cls):
        for keyword in Variables.keywords:
            for newspaper in Variables.newspaper_list:
                for year in range(Crawler.arquivo_start_year,Crawler.to_year):
                    if not Crawler.already_crawled(keyword,newspaper,year):
                        print(" ")
                        print(keyword)
                        print(newspaper)
                        print(year)
                        offset = Crawler.db_offset
                        while True:
                            try:
                                # first search and then analyse result
                                r = requests.get('http://arquivo.pt/textsearch?' +
                                                 'q=' + keyword + '&' +
                                                 'maxItems=' + str(Crawler.maxItems) + '&' +
                                                 'offset=' + str(offset) + '&' +
                                                 'siteSearch=' + Variables.newspaper_site[newspaper] + '&' +
                                                 'from=' + str(year) + '0101000000' + '&' +
                                                 'to=' + str(year + 1) + '0101000000' + '&' +
                                                 'dedupValue=' + str(Crawler.dedupValue) + '&' +
                                                 'prettyPrint=true')
                                # after each request we should wait 0.31 secs due to the limit of 195 requests per second
                                time.sleep(Crawler.sleep)
                                r_json_data = json.loads(r.text)
                                # check content length
                                if len(r_json_data['response_items']) > 0:
                                    # save current response elements
                                    print(len(r_json_data['response_items']))
                                    for news_item in r_json_data['response_items']:
                                        news_json = Crawler.process_news_url_to_json(news_item, newspaper)
                                        # check if news has at least a title
                                        # check if element already exists in the database
                                        if news_json['news_site_title'] != '' and not Database.news_exist(Database.db_news, news_json):
                                            Database.put_into_database(Database.db_news, news_json)
                                    # add previous response and continue until returns empty result
                                    previous_result_size = len(r_json_data['response_items'])
                                    offset = offset + previous_result_size
                                    Database.update_crawler(Database.db_crawler, Crawler.crawler_id, newspaper, keyword,
                                                            offset, year)
                                else:
                                    Database.update_crawler(Database.db_crawler, Crawler.crawler_id, newspaper, keyword,
                                                            offset, year)
                                    break
                            except:
                                print("error")
                                time.sleep(120)


    @classmethod
    def already_crawled(cls, current_keyword, current_newspaper, current_year):
        # keyword
        db_keyword_index = Variables.keywords.index(Crawler.db_keyword)
        current_keyword_index = Variables.keywords.index(current_keyword)
        # newspaper
        db_newspaper_index = Variables.newspaper_list.index(Crawler.db_newspaper)
        current_newspaper_index = Variables.newspaper_list.index(current_newspaper)
        if current_keyword_index < db_keyword_index:
            return True
        elif current_keyword_index > db_keyword_index:
            return False
        else:
            if current_newspaper_index < db_newspaper_index:
                return True
            elif current_newspaper_index > db_newspaper_index:
                return False
            else:
                if current_year < Crawler.db_year:
                    return True
                else:
                    return False
        return False

print("it is running")

c = Crawler(1)
c.crawling()

