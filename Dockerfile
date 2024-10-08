FROM python:3.11-slim

RUN apt update && \
    apt install -y g++ gcc make libevent-dev libffi-dev libxml2-dev libxslt-dev zlib1g-dev ffmpeg tzdata && \
    ln -sf /usr/share/zoneinfo/Asia/Taipei /etc/localtime && \
    echo "Asia/Taipei" > /etc/timezone && \
    dpkg-reconfigure -f noninteractive tzdata && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python3", "-u", "aniGamerPlus.py" ]
