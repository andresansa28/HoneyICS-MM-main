FROM zeek/zeek:6.0
RUN  apt-get -y update && apt-get -y install python3.11 python3-pip cmake libssl-dev libpcap-dev tor
RUN  sed -i '/ControlPort 9051/s/^#//g' /etc/tor/torrc

WORKDIR /home/
COPY script script

WORKDIR /home/script/
RUN pip3 install -r ./requirements.txt --break-system-packages
RUN zkg install icsnpp-s7comm --force
RUN  /etc/init.d/tor restart

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5003"]

