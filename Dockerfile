FROM python:3.5

RUN easy_install -U pip
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
