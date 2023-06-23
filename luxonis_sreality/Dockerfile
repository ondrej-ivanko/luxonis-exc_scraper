FROM mcr.microsoft.com/playwright:v1.35.0-jammy

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

COPY . /scraper

WORKDIR /scraper

RUN apt update && \
    apt upgrade -y && \
    apt-get install -y --no-install-recommends git openssh-client gpg && \
    apt install -y software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt install -y python3 python3-distutils && \
    curl -sSL https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py && \
    rm get-pip.py && \
    pip install --upgrade pip && \
    pip install -r requirements.txt && \
    rm -rf /var/cache/apt/lists/*

RUN playwright install firefox
RUN playwright install-deps

EXPOSE 8000

CMD ["bash", "-c", "/scraper/docker-entrypoint.sh"] 
