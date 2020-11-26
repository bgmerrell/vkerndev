#!/bin/bash

qemu-system-x86_64 \
	-boot order=a -drive file=arch_disk.vm,format=raw,if=virtio \
	-nographic -kernel \
 	/home/bgmerrell/code/linux/arch/x86/boot/bzImage \
	-append "root=/dev/vda rw console=ttyS0 loglevel=7 raid=noautodetect" \
	-fsdev local,id=fs1,path=/home/bgmerrell/dev/shared,security_model=none \
	-device virtio-9p-pci,fsdev=fs1,mount_tag=shared_folder \
	--enable-kvm -m 4G -smp 2 -cpu host \
	-net nic,model=virtio -net user,hostfwd=tcp::1313-:22
