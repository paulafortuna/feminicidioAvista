from Database import Database
from Variables import Variables
from Utils import Utils


class CasesAnnotation:

    @classmethod
    def cases_annotation(cls):

        df = Database.get_all_keyword_murdered_women_news(Database.db_keywords_news)
        df['title_countains_keyword'] = False

        # check if title contains keywords (both words in this case)
        for iter, row in df.iterrows():
            if iter == 16:
                print('hello')
            text = row['news_site_title']
            keywords = Variables.get_keywords_from_category('mulheres_assassinadas')
            set_news_title = Utils.convert_text_to_set(row['news_site_title'])
            for keyword in keywords:
                contains_keyword = True
                for word in Utils.convert_text_to_words_lower(keyword):
                    if word not in set_news_title:
                        contains_keyword = False
                        break
                if contains_keyword:
                    df.at[iter, 'title_countains_keyword'] = True

        df.to_csv('test.tsv',sep='\t')


c = CasesAnnotation()
c.cases_annotation()
