kubernetes:
  file.managed:
    - name: /etc/yum.repos.d/kubernetes.repo
  pkg.installed:
    - pkgs:
      - kubelet
      - kubeadm
      - kubectl
    - require:
      - file: /etc/yum.repos.d/kubernetes.repo

kubelet:
  service.running:
    - pkg: kubelet
    - enable: True