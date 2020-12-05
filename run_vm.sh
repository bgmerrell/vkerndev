#!/bin/bash

# optional shared folder for arbitrary sharing
shared_folder=/home/bgmerrell/dev/shared

# build kernel image and headers on your host and use them on your guest
kernel_image=/home/bgmerrell/code/linux/arch/x86/boot/bzImage
kernel_headers=/home/bgmerrell/code/linux/usr/include

qemu-system-x86_64 \
	-boot order=a -drive file=arch_disk.vm,format=raw,if=virtio \
	-nographic -kernel $kernel_image \
	-append "root=/dev/vda rw console=ttyS0 loglevel=7 raid=noautodetect" \
	-fsdev local,id=fs1,path=$shared_folder,security_model=none \
	-device virtio-9p-pci,fsdev=fs1,mount_tag=shared_folder \
	-fsdev local,id=fs2,path=$kernel_headers,security_model=none \
	-device virtio-9p-pci,fsdev=fs2,mount_tag=linux_headers \
	--enable-kvm -m 4G -smp 2 -cpu host \
	-net nic,model=e1000 -net user,hostfwd=tcp::1313-:22
