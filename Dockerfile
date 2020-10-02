FROM ubuntu:18.04
# install ubuntu dependencies
RUN apt-get update && apt-get install \
  -y --no-install-recommends python3 python3-virtualenv netcat python3-dev \
    build-essential cmake default-libmysqlclient-dev htop curl \
    libglib2.0-0 libsm6 libxrender1 libxext6 python-psutil openssh-server net-tools && \
    apt-get clean

RUN echo "root:Docker!" | chpasswd 
COPY sshd_config /etc/ssh/

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m virtualenv --python=/usr/bin/python3 $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

COPY requirements.txt .
# install requirements
RUN pip install \
   -r requirements.txt

# set working directory
WORKDIR /usr/src/app

# create uploads directory
RUN mkdir /usr/src/app/uploads

# add entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Install dependencies:
# add app
RUN mkdir /usr/src/app/lib
RUN mkdir /usr/src/app/etc

COPY lib /usr/src/app/lib
COPY *.py /usr/src/app/
COPY etc /usr/src/app/etc

EXPOSE 5000 2222

RUN mkdir /var/run/sshd

# run server
CMD ["/usr/src/app/entrypoint.sh"]
