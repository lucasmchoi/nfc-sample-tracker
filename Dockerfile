FROM debian:bookworm

RUN apt-get update && apt-get install -y --no-install-recommends dirmngr gnupg git curl

RUN mkdir /root/.gnupg/ && gpg --no-default-keyring --keyring /usr/share/keyrings/raspberrypi-archive-keyring.gpg --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E

RUN echo "deb [signed-by=/usr/share/keyrings/raspberrypi-archive-keyring.gpg] http://archive.raspberrypi.com/debian/ bookworm main" > /etc/apt/sources.list.d/raspi.list


RUN apt-get update && apt-get -y upgrade && apt-get install -y --no-install-recommends python3 python3-pip python3-venv python3-picamera2 python3-dev build-essential libcap-dev

RUN apt-get clean && apt-get autoremove && rm -rf /var/cache/apt/archives/* && rm -rf /var/lib/apt/lists/*


WORKDIR /nfc-sample-tracker

COPY . .

COPY ./docker/entrypoint.sh /

COPY ./docker/healthchecks.sh /

RUN python3 -m venv --system-site-packages /.venv

RUN /.venv/bin/pip install --no-cache-dir -r requirements.txt

RUN chmod +x /entrypoint.sh

RUN chmod +x /healthchecks.sh

HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 CMD [ "/healthchecks.sh" ]

ENTRYPOINT ["/entrypoint.sh"]
