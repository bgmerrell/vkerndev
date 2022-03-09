# Goal

The goal of these scripts it to provide a fast, easy, and lightweight
development environment for development and testing related to the Linux
kernel.

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

Here's a [quick video overview](https://www.youtube.com/watch?v=PhyRykOOgZM).

This repo also contains a Linux kernel config file; it may or may not meet your
needs.

# Prerequisites

This is not an exhaustive list. Some other basic packages are also required.

## Arch
* qemu
* pacstrap

## Fedora
* archlinux-keyring
* arch-install-scripts

# Usage

This should be all you need to do:

* Run `make_vm.py`, this creates your raw Arch Linux VM image (`arch_disk.vm`,
  by default). This script also installs base userspace packages and minimal
  other packages into the image. The image is also configured (to start some
  services and login automatically, for example).
* Build a kernel (you can use the included Linux config from this repo) and
  make the kernel headers. Using kernel modules isn't supported yet (but should
  be the next feature).
* Run `run_vm.sh` to run your VM
* Wham, you should be running a VM with your specified Linux kernel and
  headers. Use `shutdown(8)` when you're done. Changes on the guest will
  persist so consider making a pristine copy of your guest image.
* You can SSH to your VM using `ssh -X root@localhost -p 1313` (1313 is the
  default host port that is forwarded to the VM).
* Going forward you just need to run `run_vm.sh` to run your VM again.

# Advanced make_vm.py usage

The `--custom-setup` and `--extra-packages` options can be used to customize
your VM.

For example, if your VM requires proxy configuration to access the Internet,
you may want to use something like the included example script
`custom_setup.sh.example` to configure the proxy using `--custon-setup`.

If you want to install more packages to your VM, you can create a file with
your list of packages (newline separated), and pass that file to
`--extra-packages`.

See `--help` for other options.

# TODO

* How to best support and automate using kernel modules? Maybe something like
  virtme?
* Consider using qcow2 (overlay?) and utilizing snapshots

# CREDITS

Thanks to André Almeida for the [underlying idea](https://www.youtube.com/watch?v=HVPTpGLTJVw).
