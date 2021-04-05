![main_title](https://github.com/paulafortuna/images/blob/main/main_title.png)

![main_icons](https://github.com/paulafortuna/images/blob/main/icons_2.jpg)

### Manifesto


### Repository
This repository presents the structure of the "Feminicídio À Vista" project. It centralizes the back-end of this project, and it links to the front-end repository and the annotated dataset. The following scheme summarizes the project and readme structure.

![project_structure](https://github.com/paulafortuna/images/blob/main/feminicidio(4).jpg)

### 1) Femicide News Crawler in Arquivo.pt (Python Back-end Container)
Arquivo.pt offers an API where it is possible to crawl all Portuguese web since 1994. We aimed at collecting all available news referring to femicide cases in Portuguese Newspapers. The news were introduced in the MongoDB database. The set of steps that are followed in the Crawling container are described in the app.py file and can be summarized in this figure:

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

### 2) Femicide News Storage (MongoDB  Container)
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
