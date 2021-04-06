![main_title](https://github.com/paulafortuna/images/blob/main/main_title.png)

![main_icons](https://github.com/paulafortuna/images/blob/main/icons_2.jpg)

### Manifesto


### Repository
This repository presents the structure of the "Feminicídio À Vista" project. It centralizes the back-end, and it links to the [front-end](https://github.com/paulafortuna/feminicidioAvista_dash) repository and the annotated [dataset](https://github.com/paulafortuna/feminicidioAvista_dataset). The following scheme summarizes the project and readme structure.

![project_structure](https://github.com/paulafortuna/images/blob/main/feminicidio(4).jpg)

### 1) Femicide News Crawler in Arquivo.pt (Python Back-end Container)
The first directory inside this project is *crawling*. It corresponds to a Docker container that will connect to the Arquivo.pt API and later to the database container. The Arquivo.pt offers an API where it is possible to crawl all Portuguese web since 1994. I aimed at collecting all available news referring to femicide cases in Portuguese Newspapers. The news were introduced in the MongoDB database. The set of followed steps in the Crawling container are described in the 
[app.py](https://github.com/paulafortuna/feminicidioAvista/blob/main/crawling/app.py) file and can be summarized in this figure:


![scheme1](https://github.com/paulafortuna/images/blob/main/schema1.jpg)



#### 1.1 Crawling
The goal here is to find news about femicide cases. I started by enumerating all relevant newspapers: Público, Expresso, Diário de Notícias, Correio da Manhã, Sol, Visão e Jornal de Notícias. Because Arquivo.pt API allows a keyword search method, enumerating keywords seemed a good approach. For this, a thorough keyword list was built. For instance, keywords such as "assassina mulher" (murders woman) were included (for the entire list check the [Variables](https://github.com/paulafortuna/feminicidioAvista/blob/main/crawling/Variables.py) class or the annotated [dataset](https://github.com/paulafortuna/feminicidioAvista_dataset). Regarding the Arquivo.pt API the request was done with the following parameters:


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

The news crawling took around 3 days.

#### 1.2 Pos-processing
The pos processing consisted of cleaning the database and storing a subset of news. The pos processing took care of: erase news without title or text, erase news where the text has less than 4 words and drop news with repeated title.

#### 1.3 Keyword confirmation
It was not 100% transparent the matching between Keywords and pages happening in Arquivo.pt. For instance, I verified that some news pages would match but because in the footnote there would be referrence to the keywords. It was then important to conduct a new filtering of news to assure that news contain keywords in the title or body. I've considered a keyword match if the there are matching of all keywords subwords independently of its position.

### 2) Femicide News Storage (MongoDB  Container)
The database in this project contains a collection for each of the steps happening in the previous section. I've opted for this strategy so that I keep always a copy of the data and new experiments for each step can be done later. The corresponding database structure is:

![scheme1](https://github.com/paulafortuna/images/blob/main/schema2.jpg)

### 3) News Annotation and Metrics (Python Back-end Container)

The code for this container is present in the /classification directory. The followed steps can be described in:
![scheme3](https://github.com/paulafortuna/images/blob/main/scheme_3.jpg)

#### 3.1 Femicide news manual annotation
First, the annotation of news as referring to a femicide case was conducted manually. I started by opening the file in ~/python/data directory, transferring it to any spreadsheet editor and manually tagging news. Around 700 news were annotated and marked as femicide, and this procedure took 3h to be applied. Here it is the resulting [file](https://github.com/paulafortuna/feminicidioAvista/blob/main/classification/data/classified_news.tsv). 

#### 3.2 Geo NER Extraction
With the annotated data I aimed then at automatically extract the geolocation of the news. For this, I extracted from the news title and text all entities of type "LOC" (local). I used SpaCy with the Portuguese model  [pt_core_news_sm](https://spacy.io/models/pt) as can be found in the [jupyter notebook](https://github.com/paulafortuna/feminicidioAvista/blob/main/classification/statistics_plot_computation.ipynb). 

#### 3.3 Coordinates and District Extraction
With the entities extracted from the previous step I've used the [geopy library](https://geopy.readthedocs.io/en/stable/) and Nominatim API which offers an interface to the OpenStreetMap, for each entity I've extracted latitude and longitude, and for each news I've averaged the different local entities positions so this maps to an unique point that centralizes where the crime have happened. Of course this is an approximation and it implies some error, but overall the results seem quite satisfying, when displayed in the [map](https://feminicidioavista.herokuapp.com/). In our web app we have displayed only Continental Portugal crimes, and have excluded either other countries or Azores and Madeira, which should be addressed in future venues of this project.

#### 3.4 Metrics
Regarding metrics we extracted femicide news frequencies over year and district. We also presented different tables where the different news titles can be read. This helps to understand the collected news and to have an idea on how the media is presenting femicide. This should bring insight to future steps of this project.

![news_ano_distrito](https://github.com/paulafortuna/images/blob/main/ano_distrito.svg)

Other result of this module was the computed plots and tables that are then visualized in the web app. The code for producing plots can also be found in this [jupyter notebook](https://github.com/paulafortuna/feminicidioAvista/blob/main/classification/statistics_plot_computation.ipynb). The resulting json files are in this [directory](https://github.com/paulafortuna/feminicidioAvista/tree/main/classification/data_to_visualize).

#### *** Automatic Classification
I've investigated the usability of this dataset for machine learning supervised classification tasks. I've used BERT multilingual, which can be applied to Portuguese. The classification results with this dataset seem that in the future an automatic classifier can be used to crawl all the available news in order to find new crime instances. However, in the extracted metrics and web app section I've opted to present only manually annotated data, so that the presented results are absent of automatic classification error. I run the BERT classifier code in colab, so that I've access to TPU processing speed. Here it is the link for this [project](https://colab.research.google.com/drive/1PwI75NtL-OIJ46tbrcDcyOVWwdvAbYUD?usp=sharing).  

### 4) Femicide News Annotated Dataset
The resulting dataset can be found in this [repository](https://github.com/paulafortuna/feminicidioAvista_dataset). 

### 5) Dash Front-end (Feminicídio À Vista Web App)
The front end of this web application was developed with [dash](https://dash.plotly.com/) and can be found in this [repository](https://github.com/paulafortuna/feminicidioAvista_dash). I've opted to do it in an isolated repository so that I can continuosly integrate and deploy the github code to heroku. Hence there's an advantage to keep the project reduced to its minimum. The processed data and plots that will serve as input for the web app can be found in this [directory](https://github.com/paulafortuna/feminicidioAvista/tree/main/classification/data_to_visualize) and should be copied [here](https://github.com/paulafortuna/feminicidioAvista_dash/tree/main/data_to_visualize). I've opted to pre-compute data and plots for a matter of efficiency and code modularity. The resulting website can be found [here](https://feminicidioavista.herokuapp.com/). Unfortunately, when deployed in Heroku takes some time to load (~10 seconds).

### Extra: Configuration with docker-compose
This configuration was run in a machine using ubuntu. Hence it is possible that other OS face some additional issues. In any case the code was organized in such a way that minor changes are needed in case you want to run it without Docker.

1) Install [Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04) and [Docker-compose](https://docs.docker.com/compose/install/).
2) run docker-compose

```bash
cd feminicidioAvista
docker-compose build
docker-compose up -d
```

### Future development

- Include Madeira and Azores data.
- Include international data.
- Include other news sources.
- Report on news about "feminicide" phenomenon.
- Conduct deeper qualitative analysis in the feminicide cases news.
- Conduct deeper quantitative and classification analysis in the feminicide cases news.
- Improve web app, by replacing dash that proved to be slow and with limited design.

### Contact

In case you have any contact, suggestion or will to collaborate in this project, please contact me through my [LinkedIn](
https://pt.linkedin.com/in/paula-fortuna-a6b75a7a).

