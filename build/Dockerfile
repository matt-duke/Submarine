FROM python:3.7.4-slim-buster

RUN apt-get update -y && \
    apt-get install -y --no-install-recommends arduino-core arduino-mk \
    && rm -rf /var/lib/apt/lists/*

RUN pip install pyinstaller

COPY ./firmware /sub-gen/firmware/
COPY ./processor /sub-gen/processor/
COPY ./build /sub-gen/build/

RUN pip install -r /sub-gen/build/requirements.txt

VOLUME [ "/sub-gen/work", "/sub-gen/deploy"]

ENTRYPOINT [ "python3", "/sub-gen/build" ]
