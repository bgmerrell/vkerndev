#!/bin/bash
disk_space=${1:-'8G'}
disk_name=${2:-'arch_disk.vm'}

extra_packs='vim git strace gdb dhcpcd openssh'
xforwarding_packs='xorg-xauth xorg-xclock xorg-fonts-type1 haveged'

all_packs="$extra_packs $xforwarding_packs"

# allocate and format disk file
truncate -s $disk_space $disk_name
mkfs.ext4 $disk_name

# mount disk
mkdir mnt
sudo mount $disk_name mnt
sleep 3

# install basic system
sudo pacstrap -c mnt base base-devel $all_packs

# configure ssh
sudo cp ~/.ssh/id_rsa.pub mnt/root/

# copy bootstrap script
sudo cp start.sh mnt/root/

# umount disk
sudo umount mnt
