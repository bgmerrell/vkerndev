#!/usr/bin/env python

import argparse
import logging
import os
import shlex
import sys


def parse_args():
    parser = argparse.ArgumentParser(description='Run qemu VM')
    parser.add_argument(
        '--kernel', dest='kernel_path',
        help='path to the kernel to use on the VM',
        default=os.path.join(
            os.path.expanduser('~'), 'code/linux/arch/x86/boot/bzImage'))
    parser.add_argument(
        '--shared-folder', dest='shared_folder',
        help='path to a directory that will be shared with the VM',
        default=os.path.join(os.path.expanduser('~'), 'dev/shared'))
    parser.add_argument(
        '--kernel-headers', dest='kernel_headers_path',
        help='path to the kernel headers to use for the VM ',
        default=os.path.join(
            os.path.expanduser('~'), 'code/linux/usr/include'))
    parser.add_argument(
        '--vm', dest='vm_path',
        help='path to the vm image', default='arch_disk.vm')
    parser.add_argument(
        '--debug', action=argparse.BooleanOptionalAction,
        help='print debug messages')
    return parser.parse_args()


def main():
    logging.basicConfig()
    args = parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    qemu_cmd_str = \
        'qemu-system-x86_64 ' \
        f'-boot order=a -drive file={args.vm_path},format=raw,if=virtio ' \
        f'-nographic -kernel {args.kernel_path} ' \
        '-append "root=/dev/vda rw console=ttyS0 loglevel=7 '\
            'raid=noautodetect" ' \
        f'-fsdev local,id=fs1,path={args.shared_folder},security_model=none ' \
        '-device virtio-9p-pci,fsdev=fs1,mount_tag=shared_folder ' \
        f'-fsdev local,id=fs2,path={args.kernel_headers_path},' \
            'security_model=none ' \
        '-device virtio-9p-pci,fsdev=fs2,mount_tag=linux_headers ' \
        '--enable-kvm -m 4G -smp 2 -cpu host ' \
        '-net nic,model=e1000 -net user,hostfwd=tcp::1313-:22'
    qemu_cmd = shlex.split(qemu_cmd_str, posix=True)
    logging.debug(f'Running: {qemu_cmd}')
    sys.stdout.flush()
    sys.stderr.flush()
    os.execvp('qemu-system-x86_64', qemu_cmd)


if __name__ == '__main__':
    sys.exit(main())
