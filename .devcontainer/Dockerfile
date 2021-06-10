FROM git-docker.mst.edu/it-docker/dkr-it-python/it-python:latest
RUN apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -yq make
ENV APP_USER=mstpylib             \
    LOCAL_ENV=local               \
    TZ=America/Chicago            \  
    PYTHONPATH="/local/mstpylib"
WORKDIR /local/mstpylib
COPY requirements.txt /local/mstpylib
RUN pip install -r requirements.txt
RUN pip install -U autopep8