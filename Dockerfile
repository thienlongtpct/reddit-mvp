FROM python:3.8-slim-buster

# Installs python, removes cache file to make things smaller
RUN apt update -y && \
    yum install -y python3 python3-dev python3-pip gcc postgresql python-devel postgresql-devel && \
    rm -Rf /var/cache/yum

# Be sure to copy over the function itself!
# Goes last to take advantage of Docker caching.
COPY . .
RUN pip install -r requirements.txt
RUN python3 manage.py migrate

# Points to the handler function of your lambda function
CMD ["python3", "manage.py", "runserver"]
