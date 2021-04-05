from Database import Database
from Variables import Variables
from Utils import Utils


class NewsKeywordFiltering:
    """
    This class encapsulates functions to filter news based on the keywords.
    This is a necessary step because arquivo.pt retrieves pages based on a match with entire page text.
    So a match could happen because there was advertisement for other news.
    """

    @classmethod
    def initialize_search_keywords_annotation(cls):
        """
        In this class there's a separation between collection initialization and annotation.
        Here is done the first - initialization.
        """
        # get all pos processed news
        df = Database.get_all_posprocessed_crawled_news(Database.db_pos_processed_news)
        # mark all news as not annotated
        for column_name in Variables.keyword_categories:
            df[column_name] = False
        df['search_keywords'] = False
        # insert news again in new collection in mongo db
        Database.save_initialized_keywords_news(Database.db_keywords_news, df)


    @classmethod
    def keywords_annotation(cls):
        """
        In this class there's a separation between collection initialization and annotation.
        Here is done the second - annotation. A news is annotated if it contains a keyword in its title or text.
        """
        # get all news in annotated collection
        df = Database.get_all_non_keyword_annotated_news(Database.db_keywords_news)
        # for all news with keyword in title or text, mark as True
        for iter, row in df.iterrows():
            for category in Variables.keyword_categories:
                keywords = Variables.get_keywords_from_category(category)
                set_keywords = Utils.convert_text_to_set(' '.join(keywords))
                set_news_title = Utils.convert_text_to_set(row['news_site_title'])
                if len(set.intersection(set_keywords, set_news_title)) > 0:
                    df.at[iter, category] = True
                    continue
                set_news_text = Utils.convert_text_to_set(row['news_site_text'])
                if len(set.intersection(set_keywords, set_news_text)) > 0:
                    df.at[iter, category] = True

            df.at[iter, 'search_keywords'] = True

        # save result back in database
        Database.update_keyword_annotated_news(Database.db_keywords_news, df)


