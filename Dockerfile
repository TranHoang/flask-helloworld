FROM python:3.5-alpine

# Install build tools for psycopg2 and flask-bcrypt
RUN apk add --no-cache bash \ 
    && apk --no-cache add build-base libffi-dev postgresql-dev

# Copy source code
COPY . /app
WORKDIR /app

# Install all dependencies
RUN pip install -r requirements.txt

# Setup python application path
ENV PYTHONPATH $PYTHONPATH:/app/src
