FROM disconnect3d/nsjail

RUN apt-get update && apt-get install -y \
    gcc g++

RUN mkdir /task
WORKDIR /task
ADD . /task
