FROM python:3

RUN mkdir -p /opt/src/application/auth
WORKDIR /opt/src/application/auth

COPY application/auth/application.py ./application.py
COPY application/auth/configuration.py ./configuration.py
COPY application/auth/models.py ./models.py
COPY application/auth/requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="opt/src/application/auth"

ENTRYPOINT ["python", "./application.py"]