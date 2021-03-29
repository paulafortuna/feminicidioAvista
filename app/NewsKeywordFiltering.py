from Database import Database
from Variables import Variables
from Utils import Utils


class NewsKeywordFiltering:

    @classmethod
    def initialize_search_keywords_annotation(cls):
        df = Database.get_all_posprocessed_crawled_news(Database.db_pos_processed_news)
        for column_name in Variables.keyword_categories:
            df[column_name] = False
        df['search_keywords'] = False
        # insert in mongo db
        Database.save_initialized_keywords_news(Database.db_keywords_news, df)


    @classmethod
    def keywords_annotation(cls):

        df = Database.get_all_non_keyword_annotated_news(Database.db_keywords_news)

        # convert this to set intersection
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

        Database.update_keyword_annotated_news(Database.db_keywords_news, df)

        mask = df[Variables.keyword_categories[0]]
        for category in Variables.keyword_categories:
            mask = mask | df[category]

        filtered_df = df[mask]

        print(filtered_df)


c = NewsKeywordFiltering()
#c.initialize_search_keywords_annotation()
c.keywords_annotation()

