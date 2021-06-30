FROM python:3.8-slim-buster
ARG DATABASE_URL
RUN pip install gunicorn==20.1.0 flask==2.0.1 flask-sqlalchemy==2.5.1 flask-cors==3.0.10 psycopg2-binary==2.9.1
COPY ./ /
CMD gunicorn app:app