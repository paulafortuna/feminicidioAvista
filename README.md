![main_title](https://github.com/paulafortuna/images/blob/main/main_title.png)

![main_icons](https://github.com/paulafortuna/images/blob/main/icons_2.jpg)

([English Available](https://github.com/paulafortuna/feminicidioAvista/blob/main/readme_en))


### Manifesto

O objectivo da plataforma Feminicídio à Vista é dar visibilidade ao problema do feminicídio e não deixar que as mulheres assassinadas sejam esquecidas. Para isso, o Arquivo.pt permitiu recuperar estas histórias e anotar um conjunto de dados sobre feminicídios que se disponibilizam à comunidade. Estes dados podem ser utilizados não só por outros investigadores, mas também para construir modelos com tecnologias de inteligência artificial para anotar novas notícias e propriedades das notícias referentes a feminicídios.

Feminicídio é um termo relativamente recente, que designa o extermínio de mulheres.Estes crimes não podem ser vistos como desligados das questões de género e da intencionalidade de controlar a existência e comportamento femininos. Em alguns países, o termo feminicídio passou a estar contemplado na lei. Contudo, esse não é o caso de Portugal. Em Portugal, existe um vazio legal [1] e falta de estudos a respeito do feminicídio [2].

O projecto Feminicidio à Vista complementa outros esforços de investigação [3] ao disponibilizar à comunidade não só um conjunto de dados mas também uma plataforma open source. Nesta é possível de uma relembrar as vítimas e de uma forma dinâmica ver a relação entre as notícias individuais e estatísticas no tempo e espaço. Se, por um lado, os dados apresentados fazem referência a casos individuais de feminicídio, por outro lado, o feminicídio é um problema que requer uma resposta da sociedade. Para isso é necessário agir e os primeiros passos são reconhecer o feminicídio legalmente, recolher dados e analizá-los para se poder intervir.

*Este projeto não é*: um conjunto de estatísticas oficial sobre o feminicídio em Portugal. Neste projeto foram recolhidas notícias no Arquivo.pt como fonte de informação. Este método pode por si só conter erros e deixar de fora alguns casos. Este projecto é apenas um esforço inicial de recolha de dados, que aponta a necessidade de documentar estes crimes oficialmente e de forma mais estruturada.

*Sources*

[1] [A transversalidade dos crimes de femicídio/feminicídio no Brasil e em Portugal](https://hdl.handle.net/10216/123178)

[2] [Femminicidio in Europa un confronto tra paesi](https://www.europeandatajournalism.eu/ita/Notizie/Data-news/Femminicidio-in-Europa-un-confronto-tra-paesi)

[3] [Observatorio de mulheres assassinadas](http://www.umarfeminismos.org/index.php/observatorio-de-mulheres-assassinadas)


### Repositório
Este repositório apresenta a estrutura do projeto "Feminicídio À Vista". Centraliza o código para o back-end, referencia o repositório do [front-end](https://github.com/paulafortuna/feminicidioAvista_dash) e do [conjunto de dados](https://github.com/paulafortuna/feminicidioAvista_dataset) anotado. No esquema seguinte pode ver-se o sumário do projeto e estrutura deste README.

![project_structure](https://github.com/paulafortuna/images/blob/main/feminicidio(4).jpg)

### 1) Crawler de notícias referentes a feminicídios no Arquivo.pt (Contentor em Python - Back-end)
O primeiro diretório neste projecto tem o nome *crawling*. Corresponde a um contentor de Docker que vai ligar à API do Arquivo.pt e ao contentor da base de dados. O Arquivo.pt oferece uma API onde é possível fazer crawling a toda a web portuguesa desde 1994. Neste caso o o objetivo é encontrar todas as notícias referentes a casos de feminicídio em jornais portugueses. Estas notícias são então introduzidas numa base de dados em MongoDB. Os passos seguidos neste contentor podem ser melhor compreendidos ao analizar o ficheiro 
[app.py](https://github.com/paulafortuna/feminicidioAvista/blob/main/crawling/app.py) e podem ser sumarizados nesta figura:


![scheme1](https://github.com/paulafortuna/images/blob/main/schema1.jpg)



#### 1.1 Crawling
O objetivo era encontrar notícias sobre casos de feminicídio. O primeiro passo foi enumerar jornais relevantes para este fim. Neste caso escolheu-se: Público, Expresso, Diário de Notícias, Correio da Manhã, Sol, Visão e Jornal de Notícias. Uma vez que a API do Arquivo.pt permite pesquisar com palavras (keywords), enumerou-se um conjunto de keywords para restringir as notícias encontradas. Por exemplo, keywords como "assassina mulher" foram incluidas (para aceder à lista completa verificar ou a classe [Variables](https://github.com/paulafortuna/feminicidioAvista/blob/main/crawling/Variables.py) ou o [conjunto de dados anotado](https://github.com/paulafortuna/feminicidioAvista_dataset). As chamadas à API do Arquivo.pt foram feitas com os seguintes parâmetros:


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

O crawling de notícias demorou certa de 3 dias.

#### 1.2 Pós processamento
O pós processamento consistiu em limpar a base de dados e guardar apenas um subconjunto das páginas recolhidas. Esta fase consistiu em: remover notícias sem título ou texto, remover notícias se o título tivesse menos de 4 palavras e eliminar notícias com título repetido.

#### 1.3 Confirmação das Keywords
Uma vez que a seleção de páginas com keywords através da API do Arquivo.pt não é 100% transparente. Por exemplo, verificou-se que algumas páginas eram selecionadas porque no rodapé estaria uma referência às palavras pesquisadas, mas sem esta fazer parte do conteúdo da notícia.Foi então importante realizar uma nova filtragem, para assegurar que ou o título ou o corpo da notícia continham alguma das palavras-chave. Considerou-se que a notícia contém a keyword quando todas as subpalavras estão na notícia independentemente da posição. 

### 2) Base de dados para as notícias referentes a feminicídios (Contentor em MongoDB)
A base de dados neste projeto contém uma coleção para cada um dos passos a decorrer na secção anterior. Esta estratégia permite manter cópias dos dados nas várias fases da pipeline, o que pode ser útil caso se queiram implementar novas estratégias em cada um dos passos seguidos. A estrutura da base de dados é então:

![scheme1](https://github.com/paulafortuna/images/blob/main/schema2.jpg)

### 3) Anotação de notícias e métricas (Contentor em Python - Back-end)

The code for this container is present in the *classification* directory. The followed steps can be described in:
![scheme3](https://github.com/paulafortuna/images/blob/main/scheme_3.jpg)

#### 3.1 Femicide news manual annotation
First, the annotation of news as referring to a femicide case was conducted manually. I started by opening the file in ~/python/data directory, transferring it to any spreadsheet editor and manually tagging news. Around 700 news were annotated and marked as femicide. Here is the resulting [file](https://github.com/paulafortuna/feminicidioAvista/blob/main/classification/data/classified_news.tsv). 

#### 3.2 Geo NER Extraction
With the annotated data I aimed then to automatically extract the geolocation of the news. For this, I extracted from the news title and text all entities of type "LOC" (local). I used SpaCy with the Portuguese model  [pt_core_news_sm](https://spacy.io/models/pt) as can be found in the [jupyter notebook](https://github.com/paulafortuna/feminicidioAvista/blob/main/classification/statistics_plot_computation.ipynb). 

#### 3.3 Coordinates and District Extraction
With the entities extracted from the previous step, I've used the [geopy library](https://geopy.readthedocs.io/en/stable/) and Nominatim API which offers an interface to the OpenStreetMap. For each entity I've extracted latitude and longitude, and for each news I've averaged the different local entities positions so this maps to a unique point that centralizes where the crime has happened. This is an approximation and it implies some error, but overall the results seem quite satisfying when displayed in the [map](https://feminicidioavista.herokuapp.com/). In our web app, we have displayed only Continental Portugal crimes, and have excluded either other countries or Azores and Madeira, which should be addressed in future venues of this project.

#### 3.4 Metrics
Regarding metrics, I extracted femicide news frequencies over year and district. I also presented different tables where the different news titles can be read. This helps to understand the collected news and to have an idea on how the media is presenting femicide. This should bring insight to future steps of this project.

![news_ano_distrito](https://github.com/paulafortuna/images/blob/main/ano_distrito.svg)

Another result of this module was the computed plots and tables that are then visualized in the web app. The code for producing plots can also be found in this [jupyter notebook](https://github.com/paulafortuna/feminicidioAvista/blob/main/classification/statistics_plot_computation.ipynb). The resulting json files are in this [directory](https://github.com/paulafortuna/feminicidioAvista/tree/main/classification/data_to_visualize).

#### *** Automatic Classification
I've investigated the usability of this dataset for machine learning supervised classification tasks. I've used BERT multilingual, which can be applied to Portuguese. The classification results with this dataset seem that in the future an automatic classifier can be used to crawl all the available news in order to find new crime instances. However, in the extracted metrics and web app section I've opted to present only manually annotated data, so that the presented results are absent of automatic classification error. I run the BERT classifier code in colab, so that I've access to TPU processing speed. Here it is the link for this [project](https://colab.research.google.com/drive/1PwI75NtL-OIJ46tbrcDcyOVWwdvAbYUD?usp=sharing).  

### 4) Femicide News Annotated Dataset
The resulting dataset can be found in this [repository](https://github.com/paulafortuna/feminicidioAvista_dataset). 

### 5) Dash Front-end (Feminicídio À Vista Web App)
The front end of this web application was developed with [dash](https://dash.plotly.com/) and can be found in this [repository](https://github.com/paulafortuna/feminicidioAvista_dash). I've opted to do it in an isolated repository so that I can continuously integrate and deploy the GitHub code to Heroku. Hence there's an advantage to keep the project reduced to its minimum. The processed data and plots that will serve as input for the web app can be found in this [directory](https://github.com/paulafortuna/feminicidioAvista/tree/main/classification/data_to_visualize) and should be copied [here](https://github.com/paulafortuna/feminicidioAvista_dash/tree/main/data_to_visualize). I've opted to pre-compute data and plots for a matter of efficiency and code modularity. Unfortunately, when deployed in Heroku, the [Feminicídio À Vista website](https://feminicidioavista.herokuapp.com/) takes some time to load (~10 seconds).

### Extra: Configuration with docker-compose
This configuration was run in a machine using ubuntu. Hence, other OS may face some additional issues. In any case, the code was organized in such a way that minor changes are needed in case you want to run it without Docker.

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

