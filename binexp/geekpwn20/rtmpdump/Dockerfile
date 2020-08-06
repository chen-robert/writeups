FROM centos:7

RUN yum -y install cronie openssl-devel zlib gcc make
RUN curl http://rtmpdump.mplayerhq.hu/download/rtmpdump-2.3.tgz > rtmpdump.tgz && \
    tar xvzf rtmpdump.tgz && cd rtmpdump-2.3/ && \
    make && make install

CMD crond && rtmpsrv -z
