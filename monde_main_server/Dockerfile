FROM python3.7


RUN mkdir /code

WORKDIR /code

ADD Pipfile /code
ADD Pipfile.lock /code

RUN pip install pipenv
RUN pipenv install
RUN pipenv install gunicorn

ADD . /code

CMD gunicorn
