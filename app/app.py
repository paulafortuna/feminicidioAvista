from Crawler import Crawler
from CrawlerPosProcessing import CrawlerPosProcessing
from NewsKeywordFiltering import NewsKeywordFiltering
from CasesAnnotation import CasesAnnotation


#c = Crawler(1)
#c.crawling()

#c = CrawlerPosProcessing()
#c.pos_process_news()

#c = NewsKeywordFiltering()
#c.initialize_search_keywords_annotation()
#c.keywords_annotation()

print("it is running")

c = CasesAnnotation()
c.cases_annotation()

print("progressed")
while True:
    1











