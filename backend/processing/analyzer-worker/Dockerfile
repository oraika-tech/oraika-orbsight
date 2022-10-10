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

ENV TIYARO_API_KEY api_key

ENV AWS_SQS_ANALYSER_QUEUE AWS_SQS_ANALYSER_QUEUE

# install few required tools
RUN apt-get update && apt-get upgrade -y && apt-get install -y curl git pkg-config cmake libncurses5 build-essential
RUN apt-get clean autoclean && apt-get autoremove -y
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/

COPY pyproject.toml requirements.txt /home/user/
COPY analyzer /home/user/analyzer

# install as a package
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install .
RUN python -m nltk.downloader punkt && python -m nltk.downloader stopwords

USER user

CMD ["sh", "-c", "python analyzer/worker/worker.py"]
