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

O código deste contentor pode ser encontrado no diretório *classification*. Os passos seguidos podem ser descritos através de:
![scheme3](https://github.com/paulafortuna/images/blob/main/scheme_3.jpg)

#### 3.1 Anotação manual de notcícias de feminicídio
Em primeiro, conduziu-se uma anotação manual de notícias referentes a feminicídios. Para isso deve encontrar-se o ficheiro gerado no passo anterior e depositado ~/python/data directory, e transferir-se para algum editor de texto ou spreadsheet e manualmente decidir se uma notícia corresponde a um caso de feminicídio. 1356 notícias foram anotadas e cerca de 700 marcadas como feminicidio. Aqui pode ser encontrado o [ficheiro](https://github.com/paulafortuna/feminicidioAvista/blob/main/classification/data/classified_news.tsv) resultante da anotação. 

#### 3.2 Extração de Geo NER 
Com os dados anotados o objetivo era agora atribuir às notícias uma posição no espaço. Para isso, extraiu-se automaticamente do título e texto da notícia entidades correspondentes a locais, o que corresponde a entidades do tipo "LOC" (local). Foi usado SpaCy com um modelo para português, [pt_core_news_sm](https://spacy.io/models/pt) e o código pode ser encontrado no [jupyter notebook](https://github.com/paulafortuna/feminicidioAvista/blob/main/classification/statistics_plot_computation.ipynb). 

#### 3.3 Extração de coordenadas e distritos
Com as entidades extraidas no passado anterior, foi usada a biblioteca [geopy](https://geopy.readthedocs.io/en/stable/) e a API Nominatim, que oferece uma interface para o OpenStreetMap. Para cada entidade extraiu-se latitude e longitude, e para cada notícia fez-se a média das coordenadas das diferentes localizações. Desta forma consegue-se obter uma posição única para cada notícia e crime. Este método não corresponde à localização exacta do crime, mas permite ter uma visualização dos crimes no espaço. Os resultados obtidos com este método parecem satisfatórios quando visualizados no [mapa](https://feminicidioavista.herokuapp.com/). É de notar que nesta aplicação, visualizãmos apenas Portugal Continental e excluimos nesta fase outras países, assim como Açores e Madeira. Pretendemos incluir estes dados no futuro.

#### 3.4 Métricas
Relativamente a outras métricas, foram extraídas frequências de crimes por ano e distrito. Também se podem encontrar na aplicação tabelas onde os títulos das notícias podem ser lidos. Este tipo de visualização ajuda a compreender as notícias recolhidas e permite ter uma ideia de como os media estão a representar o feminicídio. Este tipo de análise permite dar-nos insight para os próximos passos deste projeto.

![news_ano_distrito](https://github.com/paulafortuna/images/blob/main/ano_distrito.svg)

Os resultados deste módulo são então convertidos em gráficos e tabelas, guardados em ficheiros [json](https://github.com/paulafortuna/feminicidioAvista/tree/main/classification/data_to_visualize). O código que permite obter estes ficheiro está também neste [jupyter notebook](https://github.com/paulafortuna/feminicidioAvista/blob/main/classification/statistics_plot_computation.ipynb).

#### *** Classificação automática
Foram conduzidas experiências que permitiram testar a usabilidade deste dataset com modelos de machine learning para tarefas de classificação. Neste caso testou-se BERT multilíngua, que pode ser aplicado em português. Os resultados de classificação provaram muito boa performance indicando que no futuro modelos de classificalão podem ser utilizados para mais rapidamente identificar notícias de feminocídio com base nos títulos das notícias. É de notar que na aplicação web optou-se por apresentar apenas os dados anotados manualmente, para que a inforamção apresentada esteja isenta dos erro da classificação automática. O código BERT foi corrido em Google Colab, para aceder ao poder de processamento de TPU's. Neste link pode ser encontrado este [projeto](https://colab.research.google.com/drive/1PwI75NtL-OIJ46tbrcDcyOVWwdvAbYUD?usp=sharing).  

### 4) Conjunto de dados com notícias de feminicídios
O dataset resultante pode ser encontrado neste [repositório](https://github.com/paulafortuna/feminicidioAvista_dataset). 

### 5) Dash Front-end (Feminicídio À Vista Web App)
O Front-End desta aplicação foi desenvolvido com [dash](https://dash.plotly.com/) e pode ser encontrado neste [repositório](https://github.com/paulafortuna/feminicidioAvista_dash). 
Criou-se um repositório isolado para que se pudesse fazer CI/CD (integração e deplyment contínuos) com GitHub e Heroku. Portanto, neste caso existe uma vantagem em criar um projecto isolado com o mínimo código possível. Os dados e gráficos que vão ser usados nesta aplicação podem ser encontrados neste [directório](https://github.com/paulafortuna/feminicidioAvista/tree/main/classification/data_to_visualize) e devem ser copiados para [aqui](https://github.com/paulafortuna/feminicidioAvista_dash/tree/main/data_to_visualize). Optou-se por pré-compilar dados e hráficos para que a visualização fosse mais eficiente e também para que o código apresente uma estrutura mais modular de separalão de back e fron-end. Infelizmente, quando deployed no Heroku, o site [Feminicídio À Vista](https://feminicidioavista.herokuapp.com/) pode demorar algum tempo a fazer load (~10 segundos), o que provavelmente estará relacionado com a utilização desta tecnologia pois localmente não se verifica tal problema.

### Extra: Confuguração do docker-compose
Estas instruções foram corridas numa mãquina com Ubunto. Portanto, é possível que outros sistemas operativos encontrem necessitem de outras instruções. De qualquer forma, tentou-se organizar o código de forma clara e que seja fácil de correr mesmo sem usar Docker.

1) Install [Docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-20-04) and [Docker-compose](https://docs.docker.com/compose/install/).
2) run docker-compose:

```bash
cd feminicidioAvista
docker-compose build
docker-compose up -d
```

### Futuro do projeto

- Encontrar parceiros.
- Incluir dados sobre Madeira e Açores.
- Incluir dados internacionais.
- Incluir outras fontes de notícias.
- Mostrar também outro tipo de notícias referentes ao fenómeno do feminicídio.
- Aprofundar análises quantitativas e qualitativas nas notícias sobre casos de feminicídio.
- Melhorar a aplicação web e substituir dash, uma vez que demonstrou ser lento e com um design limitado.

### Contact

Em caso de sugestões, ou interesse em colaborar, por faor, contactar através do meu [LinkedIn](
https://pt.linkedin.com/in/paula-fortuna-a6b75a7a).

