FROM nikolaik/python-nodejs:python3.10-nodejs19

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    ffmpeg \
    libavcodec-dev libavformat-dev libavdevice-dev libavutil-dev \
    libswscale-dev libavresample-dev libavfilter-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/
WORKDIR /app/

RUN pip3 install --upgrade pip
RUN pip3 install --no-cache-dir -U -r requirements.txt

CMD bash start
