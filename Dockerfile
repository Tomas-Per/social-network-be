FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements/dev.txt /code/
ADD requirements/base.txt /code/
RUN pip install --upgrade pip
RUN pip install -r dev.txt
ADD . /code/