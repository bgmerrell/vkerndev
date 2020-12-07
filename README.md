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
  default for most desktop systems I would imagine).
* Some other basic packages, which should be obvious from the scripts or
  runtime failures.

# Usage

This should be all you need to do:

* Run `deploy_vm.sh`, this creates your raw Arch Linux image (`arch_disk.vm`)
* Build a kernel (you can use the included Linux config from this repo) and
  make the kernel headers
* Update the variables in `run_vm.sh` to be suitable for your system
* Run `run_vm.sh`
* Wham, you should be running a VM with your specified Linux kernel and headers

# Demo

[Demo](https://lh3.googleusercontent.com/3FTVWFIq0khWT8johsk8qR4XBoWLvaRcGR5byY-GwEfdXjt7M48QSHW6PsOX9R4RFzESXWvagxzNEKfI1OXQR7NoBpEyBs2eVJHOVRPhWbl4dBlVO3-WNoC_AgzG3b96wsUMbSHWHMmch18Z9X4wBFChN33zS0BMkXj33Y85qaDQ8hXQL3Bc6laVmePXW_1ywaxF64-cQYwMjqiTH3BgmdFcjKJveFdlB59q7i0qX582KJchNEHxenBXwTKmUykw_uVHWRpmJJBdiSVh7YqdgcAndoiiNs_EuwebZAf_AJQPETbjVLFcBdHX0nbgqFTzPQnDGAOgAv2LFyE2ULTScbM56rwJhUnroFtVkHk816ngBuCmmHJhkP6aIhqPQqM5HESXbnwwtHVmuGZlTGVnep4w-lf-qx2awHCSwoKiEv59-2yKfoEpeEIZedOCK5KqLXSNR5syDHE7-wkk0AclJHGRRiuwWX62ngi6eFuklaLC8os79aWALt_EKUKNuYFIXktj9tAcbXAXcONss4yfW77Bi7rWzHf1IEaVTZfPlIvZjBey969povZYPGt-MKN4VgESK81Xmf5ecA0mOxvPClzimfPER2aTkhBrB9oG7k4WthBSbuMp8WxmszYXI8umHblXravHDPwo4CNPYCG4KXo0tSLHrJBD3cx8-I3t797SidhZK3pWggYRarRJ=w1277-h1140-no?authuser=0) (gif)

# TODO

* Better document usage on host distros other than Arch
* Kernel modules haven't been used or tested for this environment. How do we
  best support them? Maybe something like virtme? Need to document behavior.
