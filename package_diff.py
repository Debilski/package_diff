#!/usr/bin/env python

# collect all installed packages and show the difference

import sys
from subprocess import Popen, PIPE
from collections import Counter, defaultdict

def get_installed_packages(host, user=None, pw=None):
    h = "%s@%s" % (user, host) if user else host
    cmd = ['ssh', h, "dpkg -l"]
    exe = Popen(cmd, stdout=PIPE, stderr=PIPE)
    p = {}
    pkgs = exe.stdout.readlines()[4:]
    for pkg in pkgs:
        pkg_split = pkg.split()
        try:
            p[pkg_split[1]] = (pkg_split[2], pkg_split[0])
        except:
            pass
    return p

if __name__ == "__main__":
    hosts = sys.argv[1:]

    global_count = Counter()
    global_count_v = Counter()
    occurence = defaultdict(list)
    occurence_v = defaultdict(list)

    for host in hosts:
        packages = get_installed_packages(host)
        for (pkg, version_state) in packages.iteritems():
            version, state = version_state
            if state != "ii":
                host_ = "{}({})".format(host, state)
            else:
                host_ = host
            global_count[pkg] += 1
            global_count_v[pkg + "-" + version] += 1
            occurence[pkg].append(host_)
            occurence_v[pkg + "-" + version].append(host_)

    for (pkg, count) in sorted(global_count.items(), key=lambda item: - item[1]):
        print "{:>3d} {:<16s} [ {} ]".format(count, pkg[:16], " ".join(occurence[pkg]))

    for (pkg, count) in sorted(global_count_v.items(), key=lambda item: - item[1]):
        print "{:>3d} {:<26s} [ {} ]".format(count, pkg[:26], " ".join(occurence_v[pkg]))

