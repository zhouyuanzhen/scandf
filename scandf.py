#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import zlib
import hashlib

"""
Scan and find the duplicated files.
"""

scan_dir = '.'
res = {}


def walk2dir(t_dir):
    if os.path.exists(t_dir) and os.path.isdir(t_dir):
        w = os.walk(t_dir)

        for path, dirlist, filelist in w:
            for f in filelist:
                fname = os.path.join(path, f)
                check_file(fname)


def check_file(file):
    # print(os.stat(file))
    global res
    sizef = os.path.getsize(file)
    if sizef > 10485760:  # If file size larger than 10MB
        s = str(sizef)
        if not res.get(s):  # If not find the same size files
            xxx = [file]
            add = {s: xxx}
            res.update(add)
            # print('res: ', res)
            return
        if res.get(s):  # If find the same size files
            # print('>>> Found same size file: ------- ' + file)
            yyy = res.get(s)
            # print(yyy)
            yyy.append(file)
            del (res[s])
            record = {s: yyy}
            # print('record', record)
            res.update(record)


def loop_files():
    for k in res.keys():
        if len(res[k]) > 1:
            verify_same_files(res[k])


def calc_crc(filepath):
    fd = open(filepath, 'rb')
    content = fd.readlines()
    fd.close()

    prev = 0
    for line in content:
        prev = zlib.crc32(line, prev)
    return "%X" % (prev & 0xFFFFFFFF)


def calc_sha1(filepath):
    fd = open(filepath, 'rb')
    content = fd.readlines()
    fd.close()

    h = ''
    for line in content:
        h = hashlib.sha1(line).hexdigest()
    return h


def verify_same_files(filelist):
    # print('--> verify_same_files:')
    r = {}
    for file in filelist:
        flag = False
        hash = calc_sha1(file)
        if r.get(hash):
            newfilelist = r.get(hash)
            newfilelist.append(file)
            record = {hash:newfilelist}
            r.update(record)
            flag = True
            # continue
        if not flag:
            newfilelist = []
            newfilelist.append(file)
            record = {hash: newfilelist}
            r.update(record)
    for k in r.keys():
        if r.get(k):
            print(k, r[k])


if __name__ == '__main__':

    print("************************************************************")
    if len(sys.argv) > 1:
        scan_dir = sys.argv[1]

    print('>>> To scan directory: ' + scan_dir + '\n')
    walk2dir(scan_dir)

    print(">>> Loop for Result:")
    loop_files()
