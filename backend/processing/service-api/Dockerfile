FROM python:3.8-slim-buster

RUN useradd --create-home user
WORKDIR /home/user

# env variable
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1

ENV NUM_OF_WORKERS 1
ENV WORKER_TIMEOUT 180
ENV SERVER_PORT 8080
ENV WORKER_TYPE uvicorn.workers.UvicornWorker

ENV DB_HOST localhost:5432

ENV BUSINESS_DB_NAME business_db
ENV BUSINESS_DB_USER username
ENV BUSINESS_DB_PASSWORD password

ENV USER_DB_NAME user_db
ENV USER_DB_USER username
ENV USER_DB_PASSWORD password

ENV DATA_DB_NAME data_db
ENV DATA_DB_USER username
ENV DATA_DB_PASSWORD password

ENV CORS_ORIGINS ["*"]
ENV ALLOWED_HOSTS ["*"]

ENV SECRET_KEY "secrety_key"

# install few required tools
RUN apt-get update && apt-get upgrade -y && apt-get install -y curl git pkg-config cmake libncurses5 build-essential
RUN apt-get clean autoclean && apt-get autoremove -y
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/

COPY requirements.txt setup.py /home/user/
COPY service /home/user/service

# install as a package
RUN pip install --upgrade pip
RUN pip install --no-cache-dir gunicorn uvloop
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .


USER user
EXPOSE 8080

# cmd for running the API
CMD ["sh", "-c", "gunicorn service.main:app -b 0.0.0.0:${SERVER_PORT} -k ${WORKER_TYPE} --workers ${NUM_OF_WORKERS} --timeout ${WORKER_TIMEOUT}"]
