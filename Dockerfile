FROM python:3.6

LABEL MAINTAINER="Rajat Mhetre <mhetrerajat@gmail.com>"

WORKDIR /app

COPY . /app
RUN pip install pipenv --dev
RUN pipenv install

EXPOSE 5000

ENTRYPOINT ["sh", "-x", "entrypoint.sh"]
