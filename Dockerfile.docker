# Use the official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y tzdata pandoc

ENV TZ=America/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --verbose -r requirements.txt

COPY . /app

ENV PYTHONPATH="/app/:${PYTHONPATH}"

EXPOSE $PORT

CMD gunicorn app:app --bind 0.0.0.0:$PORT
