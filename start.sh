#!/bin/bash

# enable and start service
services="sshd dhcpcd"
systemctl enable $services
systemctl start $services

# place ssh public key
mkdir .ssh
mv id_rsa.pub .ssh/authorized_keys


# set up auto login
mkdir "/etc/systemd/system/serial-getty@.service.d"
echo "[Service]" > "/etc/systemd/system/serial-getty@.service.d/override.conf"
echo "ExecStart=" >> "/etc/systemd/system/serial-getty@.service.d/override.conf"
echo 'ExecStart=-/usr/bin/agetty --autologin root --noclear %I $TERM' >> "/etc/systemd/system/serial-getty@.service.d/override.conf"

# enable X11 forwarding
echo "X11Forwarding yes" >> /etc/ssh/sshd_config

# create a user
useradd -m user -G wheel
mkdir /home/user/.ssh
cp /root/.ssh/authorized_keys /home/user/.ssh/authorized_keys
echo "%wheel ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# fill the fstab
echo "shared_folder /home/user/host 9p trans=virtio 0 0" >> /etc/fstab

reboot
