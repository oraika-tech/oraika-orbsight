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

ENV DB_NAME obsights
ENV DB_HOST localhost:5432
ENV DB_USER obsights
ENV DB_PASSWORD obsights

ENV twitter_consumer_key twitter_consumer_key
ENV twitter_consumer_secret twitter_consumer_secret
ENV twitter_bearer_token twitter_bearer_token

ENV AWS_REGION eu-west-1
ENV AWS_SQS_ANALYSER_QUEUE AWS_SQS_ANALYSER_QUEUE
ENV AWS_ACCESS_KEY_ID AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY AWS_SECRET_ACCESS_KEY

# install few required tools
RUN apt-get update && apt-get upgrade -y && apt-get install -y curl git pkg-config cmake libncurses5 build-essential
RUN apt-get clean autoclean && apt-get autoremove -y
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/

COPY requirements.txt setup.py /home/user/
COPY observer /home/user/observer

# install as a package
RUN pip install --upgrade pip
RUN pip install --no-cache-dir gunicorn uvloop
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

USER user
EXPOSE 8080

# cmd for running the API
CMD ["sh", "-c", "gunicorn observer.presentation.observer_job_controller:app -b 0.0.0.0:${SERVER_PORT} -k ${WORKER_TYPE} --workers ${NUM_OF_WORKERS} --timeout ${WORKER_TIMEOUT}"]
