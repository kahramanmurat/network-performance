FROM python:3.9

RUN  apt-get update && apt-get install -y \
    wget

RUN pip install pandas sqlalchemy psycopg2
RUN pip install Faker


WORKDIR /app

COPY pipeline.py pipeline.py

ENTRYPOINT [ "python","pipeline.py" ]