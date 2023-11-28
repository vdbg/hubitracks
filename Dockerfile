# Alpine for smaller size
FROM python:3.11-alpine

# Create a system account hubitracks.hubitracks
RUN addgroup -S hubitracks && adduser -S hubitracks -G hubitracks
# Non-alpine equivalent of above:
#RUN groupadd -r hubitracks && useradd -r -m -g hubitracks hubitracks

USER hubitracks

WORKDIR /app

# set environment variables
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing pyc files to disc
# PYTHONUNBUFFERED: Prevents Python from buffering stdout and stderr
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install location of upgraded pip
ENV PATH /home/hubitracks/.local/bin:$PATH

COPY requirements.txt     /app

RUN pip install --no-cache-dir --disable-pip-version-check --upgrade pip && \
    pip install --no-cache-dir -r ./requirements.txt

COPY *.py                 /app/
COPY template.config.toml /app/

ENTRYPOINT  ["python", "main.py"]
