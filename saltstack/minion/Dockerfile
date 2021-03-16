FROM centos/systemd

RUN curl -o /bootstrap -Ls https://bootstrap.saltstack.com
RUN bash /bootstrap -PX -c /tmp

ADD kubernetes.repo /etc/yum.repos.d/kubernetes.repo
RUN sed -i -e 's/#master:.*/master: master/' /etc/salt/minion
RUN echo 'tmpfs /run tmpfs rw,nosuid,nodev,mode=755 0 0' >> /etc/fstab
RUN sed -i -e "s/id:.*/id: ${MINION_ID}/" /etc/salt/minion
