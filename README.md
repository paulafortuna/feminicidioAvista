![main_title](https://github.com/paulafortuna/images/blob/main/main_title.png)

![main_icons](https://github.com/paulafortuna/images/blob/main/icons_2.jpg)

### Manifesto


### Repository
This repository presents the structure of the "Feminicídio À Vista" project. It centralizes the back-end of this project, and it links to the front-end repository and the annotated dataset. The following scheme summarizes the project and readme structure.

![project_structure](https://github.com/paulafortuna/images/blob/main/feminicidio(4).jpg)

### 1) Femicide News Crawler in Arquivo.pt (Python Back-end Container)
It corresponds to the Arquivo.pt offers an API where it is possible to crawl all Portuguese web since 1994. We aimed at collecting all available news referring to femicide cases in Portuguese Newspapers. The news were introduced in the MongoDB database. The set of steps that are followed in the Crawling container are described in the app.py file and can be summarized in this figure:

![scheme1](https://github.com/paulafortuna/images/blob/main/schema1.jpg)



#### 1.1 Crawling
We started by enumerating all relevant newspapers: Público, Expresso, Diário de Notícias, Correio da Manhã, Sol, Visão e Jornal de Notícias. Arquivo.pt API allows different search methods. In this case enumerating keywords seemed a good approach. For this, a thorough keyword list was built. For instance, keyword such as "assassina mulher" (murders woman), for the entire list check Variables.py or the annotated dataset repository. Regarding the Arquivo.pt API the request was done with the following parameters:

```python
q = keyword
maxItems = 200
offset = 0 #and then updated after each call
siteSearch = newspaper_site
from = 1994
to = 2021
dedupValue = 20
sleep = 0.31
```

The crawling of the news took around 3 days.

#### 1.2 Pos-processing
The pos processing consisted of cleaning the database and storing a subset of news. The pos processing took care of: erase news without title or text, erase news where the text has less than 4 words and drop news with repeated title.

#### 1.3 Keyword confirmation
As it was not 100% transparent the matching between Keywords and pages from the archive it was important to conduct a new filtering of news so that we assure that news contain keywords at least in the title or body. For the match, I also consider that it occurres even if the words in the keyword are not contiguous.

### 2) Femicide News Storage (MongoDB  Container)
The database in this project contains a collection for each of the steps happening in the previous section. I've opted for this strategy so that new experiments with the data can be done in each step. The corresponding structure is:

![scheme1](https://github.com/paulafortuna/images/blob/main/schema2.jpg)

### 3) News Annotation and Metrics (Python Back-end Container)
### 4) Femicide News Annotated Dataset
### 5) Dash Front-end (Feminicídio À Vista Web App)

### Extra: Configuration with docker-compose




1) basic instructions to build the individual containers:
https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04

2) import the build containers to other machines:

Next steps:

import python crawler in the docker and connect with the mongodb

### Future development
