FROM python:3.9-slim-buster

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

ENV CORE_DB_NAME orb_core
ENV CORE_DB_USER orbsight
ENV CORE_DB_PASSWORD orbsight

ENV TIYARO_API_KEY api_key

# install few required tools
RUN apt-get update && apt-get upgrade -y && apt-get install -y curl git pkg-config cmake libncurses5 build-essential
RUN apt-get clean autoclean && apt-get autoremove -y
RUN rm -rf /var/lib/{apt,dpkg,cache,log}/

COPY requirements.txt setup.py /home/user/
COPY analyzer /home/user/analyzer

# install as a package
RUN pip install --upgrade pip
RUN pip install --no-cache-dir gunicorn uvloop
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -e .

USER user
EXPOSE 8080

# cmd for running the API
CMD ["sh", "-c", "gunicorn analyzer.api.api:app -b 0.0.0.0:${SERVER_PORT} -k ${WORKER_TYPE} --workers ${NUM_OF_WORKERS} --timeout ${WORKER_TIMEOUT}"]
