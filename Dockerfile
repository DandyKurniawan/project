# Builder Stage
FROM python:3-slim-bullseye AS builder

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y libpq-dev gcc

# Create the Virtual Env
RUN python -m venv /opt/venv

# Activate the virtual env
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Operational Stage
FROM python:3-slim-bullseye

RUN apt-get update -y && apt-get upgrade -y && apt-get install -y libpq-dev && rm -rf /var/lib/apt/lists/*

# Create a directory for your app
WORKDIR /PYTHONPROJECT

# Copy the virtual env from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Set the PATH and expose the port
ENV PATH="/opt/venv/bin:$PATH"
ENV CLOUD_APPS=CLOUD_RUN
EXPOSE 8080

# Copy your application code
COPY . .

# Installation For Gunicorn
RUN /opt/venv/bin/pip install gunicorn

# Run With Gunicorn
CMD . /opt/venv/bin/activate && exec gunicorn --bind 0.0.0.0:8080 --workers 1 --threads 8 --timeout 0 main:app