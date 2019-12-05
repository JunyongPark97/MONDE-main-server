FROM python:3.7

MAINTAINER MONDEIQUE

# use mirror
RUN cd /etc/apt && \
  sed -i 's/deb.debian.org/ftp.daum.net/g' sources.list

# install nginx
RUN \
  apt-get update && \
  apt-get install -y nginx && \
  rm -rf /var/lib/apt/lists/* && \
  echo "\ndaemon off;" >> /etc/nginx/nginx.conf && \
  rm /etc/nginx/sites-enabled/default && \
  chown -R www-data:www-data /var/lib/nginx

# install some packages for python/django/nginx/supervisor
RUN apt-get update
RUN apt-get install -y build-essential git
# RUN apt-get install -y python python-dev python-setuptools

# install mysql_config
RUN apt-get install -y default-libmysqlclient-dev

# install supervisor
RUN apt-get install -y supervisor

# install uwsgi
RUN apt-get install -y python3-pip
RUN pip3 install uwsgi
# install uwsgi-plugin-python3
# RUN apt-get install uwsgi

RUN mkdir /code

# install our code

ADD Pipfile /code
ADD Pipfile.lock /code

# RUN pip install on app Pipfile
RUN pip3 install pipenv

WORKDIR /code

RUN pipenv install
RUN pipenv install mysqlclient --skip-lock

ADD . /code/

# sort out permissions
RUN chown -R www-data:www-data /code

# setup nginx config
RUN ln -s /code/nginx.conf /etc/nginx/sites-enabled/
RUN ln -s /code/supervisor-app.conf /etc/supervisor/conf.d/


# setting virtualenv
RUN export replacement=`pipenv --venv` && sed -i -e 's@pyhome@'"$replacement"'@' /code/uwsgi.ini

RUN cat /code/uwsgi.ini

EXPOSE 80 22
CMD ["supervisord", "-n"]

