#!/usr/bin/env python

import argparse
import logging
import os
import shlex
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description='Run qemu VM',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-k', '--kernel', dest='kernel_path',
        help='path to the kernel to use on the VM',
        default=os.path.join(
            os.path.expanduser('~'), 'code/linux/arch/x86/boot/bzImage'))
    parser.add_argument(
        '-s', '--shared-folder', dest='shared_folder',
        help='path to a directory that will be shared with the VM',
        default=os.path.join(os.path.expanduser('~'), 'dev/shared'))
    parser.add_argument(
        '-j', '--kernel-headers', dest='kernel_headers_path',
        help='path to the kernel headers to use for the VM',
        default=os.path.join(
            os.path.expanduser('~'), 'code/linux/usr/include'))
    parser.add_argument(
        '-m', '--memory', dest='vm_memory',
        help='amount of memory to use on the VM using a "M" or "G" suffix to '
             'signify megabytes or gigabytes respectively',
        default='2G')
    parser.add_argument(
        '-c', '--cpus', dest='vm_num_cpus',
        help='number of CPUs for the VM', type=int, default=2)
    parser.add_argument(
        '-p', '--ssh-port', dest='host_ssh_port',
        help='host port to forward to the SSH port on the VM', type=int,
        default=1313)
    parser.add_argument(
        '--vm', dest='vm_path',
        help='path to the vm image', default='arch_disk.vm')
    parser.add_argument(
        '--dry-run', action='store_true', help="Don't actually exec qemu")
    parser.add_argument(
        '--debug', action='store_true', help='print debug messages')
    return parser.parse_args()


def main():
    logging.basicConfig()
    args = parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    if not os.path.isdir(args.shared_folder):
        logging.critical(
            f"shared folder path doesn't exist: {args.shared_folder}")
    qemu_cmd_str = (
        'qemu-system-x86_64 '
        f'-boot order=a -drive file={args.vm_path},format=raw,if=virtio '
        f'-nographic -kernel {args.kernel_path} '
        '-append "root=/dev/vda rw console=ttyS0 loglevel=7 '
        'raid=noautodetect" '
        f'-fsdev local,id=fs1,path={args.shared_folder},security_model=none '
        '-device virtio-9p-pci,fsdev=fs1,mount_tag=shared_folder '
        f'-fsdev local,id=fs2,path={args.kernel_headers_path},'
        'security_model=none '
        '-device virtio-9p-pci,fsdev=fs2,mount_tag=linux_headers '
        f'--enable-kvm -m {args.vm_memory} -smp {args.vm_num_cpus} -cpu host '
        f'-net nic,model=e1000 -net user,hostfwd=tcp::{args.host_ssh_port}-:22'
    )
    qemu_cmd = shlex.split(qemu_cmd_str, posix=True)
    logging.debug(f'Running: {qemu_cmd}')
    sys.stdout.flush()
    sys.stderr.flush()
    if not args.dry_run:
        os.execvp('qemu-system-x86_64', qemu_cmd)


if __name__ == '__main__':
    sys.exit(main())
