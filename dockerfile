FROM centos:latest
RUN sed -i 's/mirrorlist/#mirrorlist/g' /etc/yum.repos.d/CentOS-*
RUN sed -i 's|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g' /etc/yum.repos.d/CentOS-*
RUN yum install -y wget make && cd /usr/src && \
    wget https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tar.xz && \
    tar -xvf Python-3.9.7.tar.xz && \
    cd Python-3.9.7 && \
    yum install gcc -y && \
    yum install openssl-devel -y && \
    ./configure --prefix=/opt/python3 && \
    make altinstall && \
    ln -s /opt/python3/bin/python3.9 /usr/bin/python3.9
RUN python3.9 -m pip install python-telegram-bot --pre
RUN python3.9 -m pip install mysql-connector-python
RUN python3.9 -m pip install numpy
# CMD python3.9 /home/bot.py
