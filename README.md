# Goal

The goal of these scripts it to provide a fast, easy, and lightweight
development environment for kernel, bpf, and XDP development.

# Highlights

These scripts do the following

* Build a raw, minimal Arch Linux VM image (~1.8G) with no kernel, bootloader,
  or initrd
* Install some additional packages for development and X11 forwarding over SSH
* Automatically enable dhcp, ssh, and automatic login
* Run and boot the VM using qemu. The Linux kernel and headers are mounted from
  specified locations (in run_vm.sh) on the host machine. This allows users to
  develop and/or build kernels on their host machine and quickly run them in a
  minimal VM.

This repo also contains a Linux kernel config file.

The scripts in this repo are pretty basic; you may want to customize them to
better suit your needs.

# Prerequisites

* qemu
* pacstrap (part of the arch-install-scripts in Arch, but I believe this
  utility can be installed on other distros).
* Some other basic packages, which should be obvious from the scripts or
  runtime failures.

# Usage

This should be all you need to do:

* Run `deploy_vm.sh`, this creates your raw Arch Linux VM image
  (`arch_disk.vm`)
* Build a kernel (you can use the included Linux config from this repo) and
  make the kernel headers. Using kernel modules isn't supported yet (but should
  be the next feature).
* Update the variables in `run_vm.sh` to be suitable for your system
* Run `run_vm.sh` to run your VM
* Wham, you should be running a VM with your specified Linux kernel and
  headers. Use shutdown(8) when you're done. Changes on the gues will persist
  so consider making a pristine copy of your guest image.
* Going forward you just need to run `run_vm.sh` to run your VM again.

# Demo

[Demo](http://bean.freeshell.org/files/demo.gif) (gif)

# TODO

* Better document usage on host distros other than Arch
* How to best support and automate using kernel modules? Maybe something like
  virtme?
* Consider using qcow2 (overlay?) and utilizing snapshots

# CREDITS

Thanks to André Almeida for the [underlying idea](https://www.youtube.com/watch?v=HVPTpGLTJVw).
