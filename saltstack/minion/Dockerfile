FROM centos/systemd

RUN curl -o /bootstrap -Ls https://bootstrap.saltstack.com
RUN bash /bootstrap -PX -c /tmp

#ADD minion1 /etc/salt/minion
#ADD minion1.pem /etc/salt/pki/minion/minion.pem
#ADD minion1.pub /etc/salt/pki/minion/minion.pub
RUN sed -i -e 's/#master:.*/master: 172.28.1.1/' /etc/salt/minion
RUN echo 'tmpfs /run tmpfs rw,nosuid,nodev,mode=755 0 0' >> /etc/fstab
RUN sed -i -e "s/id:.*/id: ${MINION_ID}/" /etc/salt/minion
