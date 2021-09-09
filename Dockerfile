FROM python:3.8-slim-buster
ADD . /mvisia
WORKDIR /mvisia
RUN pip install -r requirements.txt
CMD ./entrypoint.sh