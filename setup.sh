#!/bin/bash

# enable and start service
services="sshd dhcpcd"
systemctl enable $services
#systemctl start $services

# place ssh public key
mkdir .ssh
mv id_rsa.pub .ssh/authorized_keys


# set up auto login
mkdir "/etc/systemd/system/serial-getty@.service.d"
echo "[Service]" > "/etc/systemd/system/serial-getty@.service.d/override.conf"
echo "ExecStart=" >> "/etc/systemd/system/serial-getty@.service.d/override.conf"
echo 'ExecStart=-/usr/bin/agetty --autologin root --noclear %I $TERM' >> "/etc/systemd/system/serial-getty@.service.d/override.conf"

# setup bash
echo "alias ls='ls --color=auto'" >> /root/.bashrc
echo "export PS1='🦄 \[\e[32m\]\u@\h: \[\e[33m\]\w\[\e[0m\]\n\\$ '" >> /root/.bashrc
echo "[[ -f ~/.bashrc ]] && . ~/.bashrc" >> /root/.bash_profile

# enable X11 forwarding
echo "X11Forwarding yes" >> /etc/ssh/sshd_config

# create a user
useradd -m user -G wheel
mkdir /home/user/.ssh
cp /root/.ssh/authorized_keys /home/user/.ssh/authorized_keys
echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# Remove installed linux headers package. We mount the host headers below
pacman -Rnsdd --noconfirm linux-api-headers

# fill the fstab
echo "shared_folder /home/user/host 9p trans=virtio 0 0" >> /etc/fstab
echo "linux_headers /usr/local/include 9p trans=virtio 0 0" >> /etc/fstab
