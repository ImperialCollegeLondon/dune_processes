FROM python:3.11-slim-bookworm

RUN apt-get update \
  && apt-get -y install --no-install-recommends git ssh openssh-server \
  && rm -fr /var/lib/apt/lists/*

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

COPY process-manager-no-kafka.json /

EXPOSE 22
RUN mkdir -p /root/.ssh && \
    ssh-keygen -b 2048 -t rsa -f /root/.ssh/id_rsa -q -N "" && \
    cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

RUN echo "PermitRootLogin without-password" >> /etc/ssh/sshd_config && \
    echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config && \
    echo "UserKnownHostsFile /dev/null" >> /etc/ssh/ssh_config

RUN mkdir -p /usr/src/app
