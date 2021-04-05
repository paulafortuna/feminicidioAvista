FROM python:3.8-buster

ADD . /
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1

# add this line when you want to run the classification after crawling
#CMD ["ipython", "-u", "./statistics_plot_computation.py"]
