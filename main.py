__author__ = 'egoing'
import sys, os, zlib
#path = sys.argv[1]
path = '.'
p_objects = path+'/.git/objects'
for p in os.listdir(p_objects):
    if p in ['info', 'pack']:
        continue
    for p2 in os.listdir(p_objects+'/'+p):
        fname = p_objects+'/'+p+'/'+p2
        with open(fname, 'rb') as f:
            data = f.read()
        print(zlib.decompress(data))

