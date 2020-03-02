#!/usr/bin/python

import sys

f = open(sys.argv[1], 'w')

content = sys.stdin.read()

f.write('{"content": "')
f.write(content.strip().replace('"', '\\"'))
f.write('"}')

f.close()
