FROM python:3.11

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DEBUG_MODE 0
RUN apt update
RUN apt install -y postgresql 
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# RUN pip install django
# RUN pip install psycopg2
# # RUN pip install b2sdk
# RUN pip install django-easy-audit
# RUN pip install django-quill-editor
# RUN pip install django-storages
# RUN pip install gunicorn
# RUN pip install django-htmx
# RUN pip install boto3
# RUN pip install 'django-tailwind[reload]'

# RUN pip uninstall PIL
# RUN pip install django-versatileimagefield



# RUN python mannage.py compilemessages

COPY . .

# CMD ["gunicorn","elisasrecipe.wsgi"]
