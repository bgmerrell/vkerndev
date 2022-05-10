#!/usr/bin/env python

import argparse
import logging
import os
import subprocess
import sys
import time


class Mount(object):

    DEFAULT_DIR = 'mnt'

    def __init__(self, image_name, mnt_dir):
        self.image_name = image_name
        self.mnt_dir = mnt_dir

    def __enter__(self):
        if self.mnt_dir == self.DEFAULT_DIR:
            if not os.path.isdir(self.mnt_dir):
                os.mkdir(self.mnt_dir)
        elif not os.path.isdir(self.mnt_dir):
            raise RuntimeError(
                f'Non-default mount directory {self.mnt_dir} must be created '
                'manually')

        logging.debug(f'Mounting {self.image_name} -> {self.mnt_dir}')
        subprocess.run(
            ['sudo', 'mount', self.image_name, self.mnt_dir],
            check=True)
        time.sleep(1)

    def __exit__(self, type, value, traceback):
        if os.path.isdir(self.mnt_dir):
            logging.debug(f'Unmounting {self.mnt_dir}')
            subprocess.run(['sudo', 'umount', self.mnt_dir], check=True)
            time.sleep(1)


def parse_args():
    parser = argparse.ArgumentParser(
        description='Create qemu VM',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-n', '--name', dest='image_name',
        help='the filename for the raw VM image',
        default='arch_disk.vm')
    parser.add_argument(
        '-m', '--mount', dest='mnt_dir',
        help='the directory to mount the VM image to for provisioning ',
        default=Mount.DEFAULT_DIR)
    parser.add_argument(
        '-s', '--size', dest='image_size',
        help='the max storage space to allocate for the raw VM image with a '
             'suffix of K, M, or G (kilobytes, megabytes, gigabytes). Note '
             'that the image will only use as much space is needed to store '
             'its data.',
        default='8G')
    parser.add_argument(
        '-c', '--custom-setup', nargs='*', dest='custom_setup_paths',
        default=[],
        help='a custom setup script to run in addition to the bundled '
             'setup.sh script')
    parser.add_argument(
        '-k', '--ssh-key', dest='ssh_key_path',
        help='path to public SSH key to authorize on the VM',
        default=os.path.join(
            os.path.expanduser('~'), '.ssh/id_rsa.pub'))
    parser.add_argument(
        '-p', '--extra-packages', dest='extra_packages_path',
        help='path to a file of new-line separated Arch Linux packages to '
             'install in addition to the minimal packages that are installed '
             'by default.')
    parser.add_argument(
        '--debug', action='store_true', help='print debug messages')
    return parser.parse_args()


def get_all_packages(extra_packages):
    '''Return a list of all packages to be installed on the VM images.'''
    packages = ['pacman', 'vim', 'git', 'strace', 'gdb', 'dhcpcd', 'openssh',
                'clang', 'llvm', 'pahole']
    xforwarding_packages = [
        'xorg-xauth', 'xorg-xclock', 'xorg-fonts-type1', 'haveged']
    all_packages = packages + xforwarding_packages + extra_packages
    logging.debug(f'Installing packages: {", ".join(all_packages)}')
    return all_packages


def provision_image(mnt_dir, packages, ssh_key_path, custom_setup_paths):
    '''Provision the VM image with packages, files and configs.'''
    logging.debug('Provisioning VM...')
    if not mnt_dir:
        raise RuntimeError('Target mount dir not specified')

    # pacstrap
    cmd = ['sudo', 'pacstrap', '-c', 'mnt', 'base', 'base-devel'] + packages
    logging.debug(f'Running: {cmd}')
    subprocess.run(cmd, check=True)

    mounted_root = os.path.join(mnt_dir, 'root')
    # copy over public SSH key
    cmd = ['sudo', 'cp', ssh_key_path, mounted_root]
    logging.debug(f'Running: {cmd}')
    subprocess.run(cmd, check=True)

    # copy over bundled setup script
    cmd = ['sudo', 'cp', 'setup.sh', mounted_root]
    logging.debug(f'Running: {cmd}')
    subprocess.run(cmd, check=True)

    # run bundled setup script
    chrooted_cmd = 'cd /root && ./setup.sh && rm ./setup.sh'
    for custom_setup_path in custom_setup_paths:
        filename = os.path.basename(custom_setup_path)
        cmd = ['sudo', 'cp', custom_setup_path, mounted_root]
        logging.debug(f'Running: {cmd}')
        subprocess.run(cmd, check=True)
        chrooted_cmd += f' && ./{filename} && rm ./{filename}'
    cmd = (f'sudo chroot {mnt_dir} /bin/bash -c "{chrooted_cmd}"')
    logging.debug(f'Running: {cmd}')
    subprocess.run(cmd, shell=True, check=True)


def allocate_image(size, name):
    cmd = ['truncate', '-s', size, name]
    logging.debug(f'Running: {cmd}')
    subprocess.run(cmd, check=True)

    cmd = ['mkfs.ext4', name]
    logging.debug(f'Running: {cmd}')
    subprocess.run(cmd, check=True)


def main():
    logging.basicConfig()
    args = parse_args()
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
    extra_packages = []
    if args.extra_packages_path:
        with open(args.extra_packages_path, 'r') as f:
            extra_packages = f.read().splitlines()
        logging.debug(f'Additional packages: {", ".join(extra_packages)}')
    packages = get_all_packages(extra_packages)
    print(f"mnt_dir: {args.mnt_dir}")
    allocate_image(args.image_size, args.image_name)
    with Mount(args.image_name, args.mnt_dir):
        provision_image(
            args.mnt_dir,
            packages,
            args.ssh_key_path,
            args.custom_setup_paths)


if __name__ == '__main__':
    sys.exit(main())
