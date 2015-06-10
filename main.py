import codecs

__author__ = 'egoing'
import sys, os, zlib
from abc import ABCMeta, abstractmethod

#path = sys.argv[1]

class Data(metaclass=ABCMeta):
    filepath = None
    _info = None
    def __init__(self, filepath):
        self.filepath = filepath;
        self.parse()
    def __str__(self):
        return self.symbol()+self._info['type']+'\t\t'+self._info['data']
    @abstractmethod
    def parse(self):
        pass
    @abstractmethod
    def info(self):
        pass
    @abstractmethod
    def symbol(self):
        pass

class BlobData(Data):
    def parse(self):
        fileinfo = os.stat(self.filepath);
        compressed_content = open(self.filepath, 'rb').read()
        data = ''
        try:
            data = zlib.decompress(compressed_content).decode('utf-8')
        except:
            pass
        self._info = {
            'type' : 'BLOB',
            'name' : self.filepath,
            'data' : data,
            'mtime' : fileinfo.st_mtime
        }
    def info(self):
        return self._info
    def symbol(self):
        return "@"
    def __str__(self):
        import re
        p = re.compile('^(^.+?)\s(\d+)\x00(.+)')
        m = p.match(self._info['data'])
        subtype = '\t'
        try:
            subtype = m.group(1)
        except AttributeError:
            pass
        return self.symbol()+self._info['type']+':'+subtype+'\t'+self._info['name']

class RefData(Data):
    def parse(self):
        fileinfo = os.stat(self.filepath);
        content = open(self.filepath, 'rb').read()
        self._info = {
            'type' : 'REFE',
            'name' : self.filepath,
            'data' : content.decode('utf-8'),
            'mtime' : fileinfo.st_mtime
        }
    def info(self):
        return self._info
    def symbol(self):
        return "#"

dlist = []

path = '.'
p_objects = path+'/.git/objects'
for p in os.listdir(p_objects):
    if p in ['info', 'pack']:
        continue
    for p2 in os.listdir(p_objects+'/'+p):
        dlist.append(BlobData(p_objects+'/'+p+'/'+p2))

p_refs = path+'/.git/refs'
for p in os.listdir(p_refs):
    for p2 in os.listdir(p_refs+'/'+p):
        dlist.append(RefData(p_refs+'/'+p+'/'+p2))

dlist.append(RefData('.git/HEAD'))


def call_sort(x):
    info = x.info()
    return info['mtime']
dlist.sort(key=call_sort, reverse=True)

for o in dlist:
    print(o)