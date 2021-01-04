FROM git-docker.mst.edu/it-docker/dkr-it-python/it-python:latest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq make
ENV APP_USER=mstpylib
ENV LOCAL_ENV=local
ENV TZ=America/Chicago
ENV PYTHONPATH="/local/mstpylib"
RUN /container-init.pl
WORKDIR /local/mstpylib
COPY requirements.txt /local/mstpylib
RUN pip install -r requirements.txt
RUN pip install -U autopep8