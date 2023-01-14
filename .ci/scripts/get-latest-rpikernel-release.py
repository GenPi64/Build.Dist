#!/usr/bin/env python3
import re
import subprocess


def get_version():
    cmd = '/usr/bin/git', 'ls-remote', '--tags', 'https://github.com/raspberrypi/linux.git'
    try:
        versions = subprocess.check_output(cmd).decode().strip().splitlines()
        stripped_version = []
        for version in versions:
            v = version.split()[1].replace("refs/tags/", "")
            stripped_version.append(v)
    except subprocess.CalledProcessError:
        print("Unable to get tags from Github")
        exit(1)
    pattern = re.compile(r'^1\.\d{8}$')
    matching_versions = [version for version in stripped_version if pattern.match(version)]
    matching_versions = sorted(matching_versions, reverse=True)
    if len(matching_versions) > 0:
        return matching_versions[0]
    else:
        return None


def check_kernel_release():
    cmd = 'curl', '-s', f'https://raw.githubusercontent.com/raspberrypi/linux/{get_version()}/Makefile'
    makefile_head = subprocess.check_output(cmd).decode().strip().splitlines()
    makefile_version = {}
    for line in makefile_head:
        if line.startswith("VERSION"):
            match = re.search(r'VERSION = (\d+)', line)
            makefile_version["VERSION"] = match.group(1)
        elif line.startswith("PATCHLEVEL"):
            match = re.search(r'PATCHLEVEL = (\d+)', line)
            makefile_version["PATCHLEVEL"] = match.group(1)
        elif line.startswith("SUBLEVEL"):
            match = re.search(r'SUBLEVEL = (\d+)', line)
            makefile_version["SUBLEVEL"] = match.group(1)
    return f'{makefile_version["VERSION"]}.{makefile_version["PATCHLEVEL"]}.{makefile_version["SUBLEVEL"]}'



if __name__ == '__main__':
    print(check_kernel_release())
