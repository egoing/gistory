__author__ = 'egoing'
import sys, os, zlib

def sorted_ls(path):
    mtime = lambda f: os.stat(os.path.join(path, f)).st_mtime
    return list(sorted(os.listdir(path), key=mtime))


#path = sys.argv[1]

dlist = []

path = '.'
p_objects = path+'/.git/objects'
for p in os.listdir(p_objects):
    if p in ['info', 'pack']:
        continue
    for p2 in os.listdir(p_objects+'/'+p):
        fname = p_objects+'/'+p+'/'+p2
        with open(fname, 'rb') as f:
            data = f.read()
        dlist.append({
            'type' : 'object',
            'name' : p+p2,
            'data' : str(zlib.decompress(data)),
            'mtime' : os.stat(fname).st_mtime
        })

dlist.append({
    'type': 'HEAD',
    'name' : 'HEAD',
    'data' : open('.git/HEAD').readline(),
    'mtime' : os.stat('.git/HEAD').st_mtime
})

p_refs = path+'/.git/refs'
for p in os.listdir(p_refs):
    for p2 in os.listdir(p_refs+'/'+p):
        fname = p_refs+'/'+p+'/'+p2
        with open(fname, 'rb') as f:
            data = f.read()
        dlist.append({
            'type' : p,
            'name' : p2,
            'data' : open(fname).readline(),
            'mtime' : os.stat(fname).st_mtime
        })

dlist.sort(key=lambda x : x['mtime'], reverse=True)
for p in dlist:
    print(p['type'] +'\t'+ p['data'])
