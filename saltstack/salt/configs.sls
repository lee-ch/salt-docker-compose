k8s_conf_file:
  file.managed:
    - name: /etc/sysctl.d/k8s.conf
    - source: salt://k8s.conf
    - user: root
    - group: root
    - mode: 644

enforcing:
  cmd.run:
    - name: setenforce 0
  file.managed:
    - name: /etc/selinux/config
    - source: salt://selinux.conf
    - user: root
    - group: root
    - mode: 644

swap_d:
  cmd.run:
    - name: sed -i '/swap/d' /etc/fstab

swap_off:
  cmd.run:
    - name: swapoff -a

yum_utils:
  cmd.run:
    - name: yum install -y yum-utils