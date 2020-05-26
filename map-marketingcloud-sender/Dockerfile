FROM python:3.7

WORKDIR /app

COPY ./requirements.txt ./

RUN pip3 install --upgrade pip \
    && pip3 install -r requirements.txt

COPY ./app .

CMD python app.py