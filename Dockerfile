FROM python:3.11.6

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && pip install -r requirements.txt

COPY services /app/services
COPY flask_app.py /app

EXPOSE 8000 5000

#RUN echo "postgresql_password = 1234" > services/settings.py
#RUN echo "secret_key='lmvsdlavlge'" >> services/settings.py
#RUN echo "host_name='host.docker.internal'" >> services/settings.py

CMD [ "flask", "--app", "flask_app", "run" ]