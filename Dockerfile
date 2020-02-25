FROM alpine:latest

LABEL version="1.0"
LABEL description="Docker image for running and compiling source code and scripts, redirecting output, and running test harnesses"
LABEL maintainer="jzlotek@gmail.com"

RUN apk add --no-cache python3


