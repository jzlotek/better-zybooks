FROM python:3-alpine

LABEL version="1.0"
LABEL description="Docker image for running and compiling source code and scripts, redirecting output, and running test harnesses"
LABEL maintainer="jzlotek@gmail.com"

RUN apk update
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev

WORKDIR /flask/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8163

CMD ["python3", "./app.py"]
