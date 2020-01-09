#!/usr/bin/env python3

import itertools
import subprocess

# list of packages I maintain that have not yet been upstreamed for some reason
# or another
klardotsh_packages = {
    'wl-clipboard-x11',
    'capitaine-cursors',
    'swaylock-effects',
    'chamber',
}

arch_mappings = {
    'x86_64': 'x86_64',
    'x86_64-musl': 'x86_64-musl',
    'aarch64': 'x86_64',
    'aarch64-musl': 'x86_64-musl',
}

def prepare_masterdirs(mappings):
    masterdirs_required = set(d for d in mappings.values())

    for md in masterdirs_required:
        subprocess.run(
            f'./xbps-src -m "masterdir-{ md }" binary-bootstrap "{ md }"',
            shell=True,
            check=True,
        )

def maybe_arch_string(arch, masterdir):
    if arch == masterdir:
        return ''

    return f'-a "{ arch }"'

def build_package_for_arch(package, arch, masterdir):
    subprocess.run(
        f'./xbps-src -m "masterdir-{ masterdir }" { maybe_arch_string(arch, masterdir) } pkg "{ package }"',
        shell=True,
        check=True,
    )

if __name__ == '__main__':
    prepare_masterdirs(arch_mappings)

    for package, (arch, masterdir) in itertools.product(klardotsh_packages, arch_mappings.items()):
        build_package_for_arch(package, arch, masterdir)
