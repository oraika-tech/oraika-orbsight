FROM python:3.9-slim-buster

RUN useradd --create-home user
WORKDIR /home/user

# env variable
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_NO_CACHE_DIR 1

ENV DB_HOST localhost:5432
ENV CORE_DB_NAME orb_core
ENV CORE_DB_USER orbsight
ENV CORE_DB_PASSWORD orbsight

ENV twitter_consumer_key twitter_consumer_key
ENV twitter_consumer_secret twitter_consumer_secret
ENV twitter_bearer_token twitter_bearer_token

ENV AWS_REGION eu-west-1
ENV AWS_SQS_ANALYSER_QUEUE AWS_SQS_ANALYSER_QUEUE
ENV AWS_ACCESS_KEY_ID AWS_ACCESS_KEY_ID
ENV AWS_SECRET_ACCESS_KEY AWS_SECRET_ACCESS_KEY
ENV AWS_SQS_OBSERVER_QUEUE AWS_SQS_OBSERVER_QUEUE

# install few required tools
RUN apt-get update && apt-get upgrade -y && apt-get install -y curl git pkg-config cmake libncurses5 build-essential
RUN apt-get clean autoclean && apt-get autoremove -y
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/

COPY pyproject.toml requirements.txt /home/user/
COPY observer /home/user/observer

# install as a package
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .

USER user

CMD ["sh", "-c", "python observer/presentation/observer_job_controller.py"]
