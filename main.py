__author__ = 'egoing'
import sys, os, zlib

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))


#path = sys.argv[1]
path = '.'
p_objects = path+'/.git/objects'
for p in sorted_ls(p_objects):
    if p in ['info', 'pack']:
        continue
    for p2 in os.listdir(p_objects+'/'+p):
        fname = p_objects+'/'+p+'/'+p2
        with open(fname, 'rb') as f:
            data = f.read()
        print(p+p2+"\t"+str(os.stat(fname).st_mtime)+"\t"+str(zlib.decompress(data)))


