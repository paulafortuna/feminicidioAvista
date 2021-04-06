from Crawler import Crawler
from CrawlerPosProcessing import CrawlerPosProcessing
from NewsKeywordFiltering import NewsKeywordFiltering
from CasesAnnotation import CasesAnnotation

# start crawler class that connects to the arquivo.pt api
c = Crawler(1)
c.crawling()

# after crawling conducts a post processing step removing some redundant or poor quality news
c = CrawlerPosProcessing()
c.pos_process_news()

# assures that the news title or body contains the keywords
c = NewsKeywordFiltering()
c.initialize_search_keywords_annotation()
c.keywords_annotation()

# retrieves a file with the news to manually annotate
c = CasesAnnotation()
c.cases_annotation()

print("0")









