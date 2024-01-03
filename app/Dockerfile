FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apt update
RUN apt install -y postgresql 
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

RUN pip uninstall PIL
RUN pip install django-versatileimagefield

# RUN python mannage.py compilemessages

COPY . .

CMD ["python","manage.py","migrate","&&","python","manage.py","collectstatic","--noinput","&&","gunicorn","elisasrecipe.wsgi"]
