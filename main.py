import codecs

__author__ = 'egoing'
import sys, os, zlib
from abc import ABCMeta, abstractmethod

LIST_SIZE = 30

#path = sys.argv[1]
path = '.git'

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
    def info(self):
        return self._info
    def __str__(self):
        str = ('-'*100)+'\n'
        str += self._info['type']+'\t'+self._info['name']+'\n'+self._info['data']+'\n\n'
        return str

class ObjectData(Data):
    def parse(self):
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
            'data' : data
        }
    def __str__(self):
        content = self._info['data']
        if self._info['type'] == 'blob':
            content = content[:100]
        str = '________________________________________________\n'
        str += self._info['type']+'\t'+self._info['name']+'\n'+content+"\n\n"
        # str += '________________________________________________\n'
        return str

class RefData(Data):
    def parse(self):
        content = open(self.filepath, 'rb').read()
        self._info = {
            'type' : 'REFE',
            'name' : self.filepath,
            'data' : content.decode('utf-8')
        }

class IndexData(Data):
    def parse(self):
        import subprocess
        p = subprocess.Popen("git ls-files --stage", shell=True, stdout=subprocess.PIPE)
        data = p.communicate()[0].decode('utf-8').strip()
        self._info = {
            'type' : 'index',
            'name' : 'index',
            'data' : data
        }


class PackData(Data):
    def parse(self):
        import subprocess
        p = subprocess.Popen("git verify-pack -v "+self.filepath, shell=True, stdout=subprocess.PIPE)
        data = p.communicate()[0].decode('utf-8').strip()
        self._info = {
            'type' : 'pack',
            'name' : self.filepath,
            'data' : data
        }

fileList = []
for (_path, _dir, _files) in os.walk(path):
    _path = _path.replace('\\', '/')
    for _file in _files:
        fpath = os.path.join(_path+'/'+_file)
        _type = None
        if '.git/hooks' in fpath:
            break;
        if '.git/objects/pack' in fpath:
            if '.pack' in fpath:
                continue;
            _type = 'pack'
        elif '.git/objects' in fpath:
            _type = 'object'
        elif '.git/index' in fpath:
            _type = 'index'
        fileList.append([fpath, os.stat(fpath).st_mtime, _type])
import operator
fileList.sort(key=operator.itemgetter(1), reverse=True)
for _file in fileList:
    if _file[2] in ['commit', 'blob', 'tree']:
        print(ObjectData(_file[0]))
    elif _file[2] == 'index':
        print(IndexData(_file[0]))
    elif _file[2] == 'pack':
        print(PackData(_file[0]))
    else:
        print(RefData(_file[0]))