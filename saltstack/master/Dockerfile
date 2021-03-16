FROM centos/systemd

ARG MINION_IDS
ARG MINIONS

EXPOSE 8000

RUN curl -o /bootstrap -Ls https://bootstrap.saltstack.com
RUN bash /bootstrap -MNPX -p salt-api -p pyOpenSSL -c /tmp

ADD master /etc/salt/master
ADD formulas /srv/formulas
ADD kubernetes.repo /etc/yum.repos.d/kubernetes.repo
#ADD master_minion.pem /etc/salt/pki/master.pem
#ADD master_minion.pub /etc/salt/pki/master.pub
#ADD master_minion.pem /etc/salt/pki/minion/minion.pem
#ADD master_minion.pub /etc/salt/pki/minion/minion.pub
#ADD master_minion.pub /etc/salt/pki/minion/minion_master.pub
##ADD minion1.pub /etc/salt/pki/master/minions/minion1
#ADD minion2.pub /etc/salt/pki/master/minions/minion2
RUN ln -sf /usr/lib/systemd/system/salt-api.service /etc/systemd/system/multi-user.target.wants/salt-api.service
RUN ln -sf /usr/lib/systemd/system/salt-master.service /etc/systemd/system/multi-user.target.wants/salt-master.service
RUN salt-run salt.cmd tls.create_self_signed_cert
#RUN for MINION_ID in $(echo "${MINION_IDS}" | tr ',' '\n'); do salt-key --gen-keys=${MINION_ID} && cp ${MINION_ID}.pub /etc/salt/pki/minion/${MINION_ID}; done

RUN useradd -m saltdev
RUN echo saltdev | passwd --stdin saltdev

RUN echo 'tmpfs /run tmpfs rw,nosuid,nodev,mode=755 0 0' >> /etc/fstab

RUN curl -o /bootstrap -Ls https://bootstrap.saltstack.com
RUN bash /bootstrap -PX -c /tmp

#ADD minion1 /etc/salt/minion
#ADD minion1.pem /etc/salt/pki/minion/minion.pem
#ADD minion1.pub /etc/salt/pki/minion/minion.pub
RUN sed -i -e 's/#master:.*/master: master/' /etc/salt/minion
RUN echo 'tmpfs /run tmpfs rw,nosuid,nodev,mode=755 0 0' >> /etc/fstab
RUN sed -i -e "s/id:.*/id: master/" /etc/salt/minion
