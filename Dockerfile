FROM python:3.6

LABEL MAINTAINER="Rajat Mhetre <mhetrerajat@gmail.com>"

WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT ["sh", "-x", "entrypoint.sh"]