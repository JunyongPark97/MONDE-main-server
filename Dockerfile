FROM python3.7


RUN mkdir /code

# install our code
ADD . /code/

ADD Pipfile /code
ADD Pipfile.lock /code

# RUN pip install on app Pipfile
RUN pip install pipenv
RUN pipenv install

# sort out permissions
RUN chown -R www-data:www-data /code

# setup nginx config
RUN ln -s /code/nginx-app.conf /etc/nginx/sites-enabled/
RUN ln -s /code/supervisor-app.conf /etc/supervisor/conf.d/

WORKDIR /code

EXPOSE 80 22
CMD ["supervisord", "-n"]

