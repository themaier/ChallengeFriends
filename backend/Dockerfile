FROM python:3.10

WORKDIR /backend
RUN pip install --upgrade pip
COPY ./requirements.txt /backend/requirements.txt
RUN pip install -r requirements.txt

COPY . /backend