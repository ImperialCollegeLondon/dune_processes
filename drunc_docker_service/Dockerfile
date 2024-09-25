FROM ghcr.io/dune-daq/frozen-release-alma9:fddaq-v5.1.0-a9

RUN yum install -y openssh-server && yum clean all

# required for dunedaq setup
SHELL ["/bin/bash", "-c"]

WORKDIR /basedir

# for frozen release
RUN source /cvmfs/dunedaq.opensciencegrid.org/setup_dunedaq.sh && \
        setup_dbt latest_v5 && \
        dbt-create fddaq-v5.1.0-a9 fddaq-v5.1.0-a9 && \
        cd fddaq-v5.1.0-a9 && \
        source env.sh && \
        dbt-build && \
        dbt-workarea-env && \
        pip install git+https://github.com/DUNE-DAQ/drunc.git@v0.10.2
WORKDIR /basedir/fddaq-v5.1.0-a9/

COPY process-manager-no-kafka.json data/

RUN mkdir -p /root/.ssh && \
    ssh-keygen -b 2048 -t rsa -f /root/.ssh/id_rsa -q -N "" && \
    cp /root/.ssh/id_rsa.pub /root/.ssh/authorized_keys

RUN echo "PermitRootLogin without-password" >> /etc/ssh/sshd_config && \
    echo "StrictHostKeyChecking no" >> /etc/ssh/ssh_config && \
    echo "UserKnownHostsFile /dev/null" >> /etc/ssh/ssh_config && \
    ssh-keygen -A

RUN mkdir -p /usr/src/app
ENTRYPOINT []

ADD wibeth_output_all_zeros.bin /cvmfs/dunedaq.opensciencegrid.org/assets/files/d/d/1/wibeth_output_all_zeros.bin
