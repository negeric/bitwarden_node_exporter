FROM tiangolo/uwsgi-nginx-flask:python3.8

WORKDIR /app
# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY ./app /app
