FROM python:3

RUN mkdir -p /opt/src/application/store
WORKDIR /opt/src/application/store

COPY application/store/migrate.py ./migrate.py
COPY application/store/configuration.py ./configuration.py
COPY application/store/models.py ./models.py
COPY application/store/requirements.txt ./requirements.txt
COPY application/store/customerApplication.py ./customerApplication.py
COPY application/store/decorator.py ./decorator.py

RUN pip install -r ./requirements.txt

ENTRYPOINT ["python", "./customerApplication.py"]