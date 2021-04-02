FROM python:3.8-buster

ADD . /
RUN pip install -r requirements.txt
ENV PYTHONUNBUFFERED 1

CMD ["python", "-u", "./app.py"]

