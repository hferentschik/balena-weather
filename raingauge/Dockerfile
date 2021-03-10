FROM balenalib/raspberrypi4-64-python:3-buster-build

RUN apt-get update \
 && apt-get install -yq vim openssh-server \
 && apt-get clean \
 && rm -rf /var/lib/apt/lists/*

RUN mkdir /var/run/sshd \
 && echo 'root:balena' | chpasswd \
 && sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config \
 && sed -i 's/UsePAM yes/UsePAM no/' /etc/ssh/sshd_config

WORKDIR /app
COPY . ./

RUN pip3 install -r requirements.txt

CMD ["./start.sh"]
