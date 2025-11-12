FROM ubuntu:latest

RUN apt-get update && apt-get install -y bind9 bind9-utils && rm -rf /var/lib/apt/lists/*

COPY named.conf /etc/bind/
COPY zones/ /etc/bind/zones/

EXPOSE 53/udp 53/tcp

CMD ["/usr/sbin/named", "-g"]
