FROM python:3

RUN mkdir -p /opt/src/application/auth
WORKDIR /opt/src/application/auth

COPY application/auth/migrate.py ./migrate.py
COPY application/auth/configuration.py ./configuration.py
COPY application/auth/models.py ./models.py
COPY application/auth/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./migrate.py"]