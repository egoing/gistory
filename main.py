import codecs

__author__ = 'egoing'
import sys, os, zlib
from abc import ABCMeta, abstractmethod

LIST_SIZE = 30

#path = sys.argv[1]

class Data(metaclass=ABCMeta):
    filepath = None
    _info = None
    def __init__(self, filepath):
        self.filepath = filepath;
        self.parse()
    def __str__(self):
        return self.symbol()+self._info['type']+','+self._info['data']
    @abstractmethod
    def parse(self):
        pass
    @abstractmethod
    def info(self):
        pass
    @abstractmethod
    def symbol(self):
        pass

class ObjectData(Data):
    def parse(self):
        fileinfo = os.stat(self.filepath);
        _fileinfo = os.path.split(self.filepath)
        object = _fileinfo[0][-2:] + _fileinfo[1]
        import subprocess
        p = subprocess.Popen("git cat-file -p "+object, shell=True, stdout=subprocess.PIPE)
        data = p.communicate()[0].decode('utf-8').strip()
        p = subprocess.Popen("git cat-file -t "+object, shell=True, stdout=subprocess.PIPE)
        t = p.communicate()[0].decode('utf-8').strip()
        self._info = {
            'type' : t,
            'name' : object,
            'data' : data,
            'mtime' : fileinfo.st_mtime
        }
    def info(self):
        return self._info
    def symbol(self):
        return "@"
    def __str__(self):
        content = self._info['data']
        if self._info['type'] == 'blob':
            content = content[:100]
        str = '________________________________________________\n'
        str += self.symbol()+self._info['type']+'\t'+self._info['name']+'\n'+content+'\n'
        # str += '________________________________________________\n'
        return str

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
    def __str__(self):
        str = '________________________________________________\n'
        str += self.symbol()+self._info['type']+'\t'+self._info['name']+'\n'+self._info['data']+'\n'
        # str += '________________________________________________\n'
        return str

dlist = []
path = '.'
p_objects = path+'/.git/objects'
i = 0
for p in os.listdir(p_objects):
    if i > 30:
        break
    if p in ['info', 'pack']:
        continue
    for p2 in os.listdir(p_objects+'/'+p):
        dlist.append(ObjectData(p_objects+'/'+p+'/'+p2))
    i += 1

p_refs = path+'/.git/refs'
for p in os.listdir(p_refs):
    for p2 in os.listdir(p_refs+'/'+p):
        dlist.append(RefData(p_refs+'/'+p+'/'+p2))

dlist.append(RefData('.git/HEAD'))


def call_sort(x):
    info = x.info()
    return info['mtime']
dlist.sort(key=call_sort, reverse=True)

i = 0
while i < min(len(dlist), LIST_SIZE):
    print(dlist[i])
    i += 1

print('\u001b[1;31mColor Text\u001b[0m')
print('\u001b[1;31mColor Text\u001b[0m')

