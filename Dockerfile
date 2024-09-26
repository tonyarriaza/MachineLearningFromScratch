
FROM python:3.10-slim


RUN pip install --upgrade pip


RUN apt-get update && apt-get install -y tzdata pandoc


ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


WORKDIR /app


COPY . /app


ENV PYTHONPATH="/app/:${PYTHONPATH}"

RUN pip install --no-cache-dir --verbose -r requirements.txt
