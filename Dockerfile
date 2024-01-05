FROM python:3.11

WORKDIR /usr/src/recettes

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG_MODE 0
RUN apt update
RUN apt install -y postgresql 
RUN pip install --upgrade pip
COPY ./requirements.dev.txt .
RUN pip install -r requirements.dev.txt

# RUN python mannage.py compilemessages

COPY . .
