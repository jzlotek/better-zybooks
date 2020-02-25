FROM python:3-alpine

LABEL version="1.0"
LABEL description="Docker image for running and compiling source code and scripts, redirecting output, and running test harnesses"
LABEL maintainer="jzlotek@gmail.com"

WORKDIR /usr/src/app

RUN apk update && apk add --no-cache postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
CMD ["python3", "./app.py"]
