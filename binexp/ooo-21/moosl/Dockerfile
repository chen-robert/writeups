FROM ubuntu:21.04

RUN apt-get update && apt-get install -y openssh-server
RUN apt-get install -y musl
RUN apt-get install -y software-properties-common
RUN add-apt-repository universe
RUN apt-get update 
RUN apt-get install -y python2
RUN apt-get install -y curl
RUN curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
RUN python2 get-pip.py
RUN pip2 install pwntools
RUN apt-get install -y libc6-dbg
RUN apt-get install -y gdb
RUN apt-get install -y git
RUN git clone https://github.com/pwndbg/pwndbg
RUN mkdir /var/run/sshd
RUN echo 'root:123456789' | chpasswd
RUN echo "PermitRootLogin yes" >> /etc/ssh/sshd_config
RUN apt-get install -y vim
RUN chmod +x /pwndbg/setup.sh
WORKDIR /pwndbg
RUN ./setup.sh
WORKDIR /
# CHANGE
COPY mooosl /root/mooosl
RUN chmod +x /root/mooosl
# SSH login fix. Otherwise user is kicked off after login
RUN sed 's@session\s*required\s*pam_loginuid.so@session optional pam_loginuid.so@g' -i /etc/pam.d/sshd

ENV NOTVISIBLE "in users profile"
RUN echo "export VISIBLE=now" >> /etc/profile

EXPOSE 22
CMD ["/usr/sbin/sshd", "-D"]

EXPOSE 22
