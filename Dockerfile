FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2


WORKDIR /app
COPY ingest_data_green.py ingest_data_green.py 
COPY ingest_data_yellow.py ingest_data_yellow.py 
COPY entrypoint.sh entrypoint.sh

RUN chmod +x ./entrypoint.sh


# first is name of origin file, second is name of destination file


# executes the below command on startup
ENTRYPOINT [ "./entrypoint.sh" ]

