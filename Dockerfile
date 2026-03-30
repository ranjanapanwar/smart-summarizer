FROM python:3.11-slim

RUN apt-get update && apt-get install -y supervisor

RUN apt-get install -y net-tools

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 7860

CMD ["/usr/bin/supervisord", "-n"]





