FROM 304872096477.dkr.ecr.us-west-2.amazonaws.com/kasasa/python:3.7

WORKDIR /app

COPY ./requirements.txt .
RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt \
    && touch ./worker_pid

COPY ./app .

ENTRYPOINT ["./entrypoint.sh"]
