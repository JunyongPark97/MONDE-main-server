FROM python:3.7

MAINTAINER MONDEIQUE

# use mirror
# RUN cd /etc/apt && \
#  sed -i 's/deb.debian.org/ftp.daum.net/g' sources.list

# install some packages for python/django/nginx/supervisor
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y \
	git \
	python3 \
	python3-dev \
	python3-setuptools \
	python3-pip \
	nginx \
	supervisor && \
	pip3 install -U pip setuptools && \
   rm -rf /var/lib/apt/lists/*


RUN apt-get update
RUN apt-get install -y build-essential git

# install mysql_config
#RUN apt-get install -y default-libmysqlclient-dev

# install uwsgi
RUN pip3 install uwsgi
RUN pip3 install pipenv

RUN mkdir /code

# install our code
ADD . /code/

# sort out permissions
RUN chown -R www-data:www-data /code

# setup nginx config
RUN echo "daemon off;" >> /etc/nginx/nginx.conf
COPY nginx-app.conf /etc/nginx/sites-enabled/default
RUN ln -s /code/supervisor-app.conf /etc/supervisor/conf.d/

WORKDIR /code

RUN pipenv install
RUN pipenv install mysqlclient --skip-lock

# setting virtualenv
RUN export replacement=`pipenv --venv` && sed -i -e 's@pyhome@'"$replacement"'@' /code/uwsgi.ini


EXPOSE 80 22
CMD ["supervisord", "-n"]

