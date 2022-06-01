#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

"""
Scan and find the duplicated files.
"""

scan_dir = './'
res = {}


def walk2dir(t_dir):
	if os.path.exists(t_dir) and os.path.isdir(t_dir):
		w = os.walk(t_dir)

		for path, dirlist, filelist in w:
			for f in filelist:
				fname = os.path.join(path, f)
				# print('debug: FILE:' + fname)
				check_file(fname)


def check_file(file):
	# print(os.stat(file))
	global res
	sizef = os.path.getsize(file)
	if sizef > 1048576:  # If file size larger than 1MB
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
			del(res[s])
			record = {s: yyy}
			# print('record', record)
			res.update(record)

def loop_files():
	for v in res.values():
		if len(v) > 1:
			print(v)


if __name__ == '__main__':

	print("************************************************************")
	if len(sys.argv) > 1:
		scan_dir = sys.argv[1]

	print('>>> Debug: scan dir = ' + scan_dir + '\n')
	walk2dir(scan_dir)

	# print("\n>>> Result:", res)

	print("\n>>> Loop for Result:")
	loop_files()
