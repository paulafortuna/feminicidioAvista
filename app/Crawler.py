from Database import Database
from Variables import Variables
import requests
import json
import time
from datetime import date

from newspaper import Article


class Crawler:
    """
    This class allows to run a crawler that will to collect all the news referring to
    keywords. It will do it since 1996 until present date. In case the crawler stops it
    is possible to restore its progress and continue crawling as it saves its state in
    the database.

    Parameters
    ----------
    crawler_id : int
        The crawler_id is used for giving a database id to the crawler.
    """

    # default crawler parameters:
    # the id of the crawler
    crawler_id = 0
    # the keyword that is currently being searched
    db_keyword = Variables.keywords[0]
    # the newspaper that is currently being searched
    db_newspaper = Variables.newspaper_list[0]
    # offset is a variable used in arquivo.pt
    db_offset = 0
    # maxItems is a variable used in arquivo.pt
    maxItems = 200
    # starting crawler year
    db_year = Variables.arquivo_start_year
    # final year the crawler should consider
    to_year = date.today().year
    # dedupValue is a variable used in arquivo.pt to reduce duplicated results
    dedupValue = 20
    # recomended time between API calls
    sleep = 0.31

    def __init__(self, crawler_id):
        """
        Crawler initializer.

        Arguments
        ----------
        crawler_id : int
            The crawler_id is used for giving a database id to the crawler.
        """
        Crawler.crawler_id = crawler_id
        # if it exists read from database state from crawler or create a new register
        crawler_json = Database.starting_crawler(Database.db_crawler,
                                                 crawler_id,
                                                 Crawler.db_newspaper,
                                                 Crawler.db_keyword,
                                                 Crawler.db_offset,
                                                 Variables.arquivo_start_year)
        Crawler.db_keyword = crawler_json['keyword']
        Crawler.db_newspaper = crawler_json['current_newspaper']
        Crawler.db_offset = crawler_json['offset']
        Crawler.db_year = crawler_json['year']

    @classmethod
    def process_news_url_to_json(cls, news_item, newspaper):
        """
        Convert arquivo.pt news instance to json.

        Arguments
        ----------
        news_item : str
            The news instance retrieved from arquivo.pt
        newspaper : str
            The crawled newspaper to add to the news json.
        """
        print(news_item)
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

    @classmethod
    def crawling(cls):
        """
        Central code of the crawler to arquivo.pt.
        For each of the keywords, for each of the newspaper, for each of the years Crawl.
        Before, check if crawler already conducted crawling for a query so that it does not repeat it.
        """
        for keyword in Variables.keywords:
            for newspaper in Variables.newspaper_list:
                for year in range(Variables.arquivo_start_year,Crawler.to_year+1):
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
                                # after each request we should wait 0.31 secs due to the limit of 195 requests
                                # per second
                                time.sleep(Crawler.sleep)
                                r_json_data = json.loads(r.text)
                                # check content length to see if we got response
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
        """
        Method that checks if the instantiated crawler already conducted a query,
        so that it does not repeat it.

        Arguments
        ----------
        current_keyword : keyword currently being crawled.
        current_newspaper : newspaper currently being crawled.
        current_year : year currently being crawled.

        Return
        ----------
        boolean : returns if query was already conducted by this crawler in arquivo.pt
        """
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

