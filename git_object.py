from abc import ABCMeta, abstractmethod
import sys, os

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
            'data' : data,
            'path' : self.filepath
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
        print(self.filepath)
        content = open(self.filepath, 'rb').read()
        self._info = {
            'type' : 'REFE',
            'name' : self.filepath,
            'data' : content.decode('utf-8'),
            'path' : self.filepath
        }

class IndexData(Data):
    def parse(self):
        import subprocess
        p = subprocess.Popen("git ls-files --stage", shell=True, stdout=subprocess.PIPE)
        data = p.communicate()[0].decode('utf-8').strip()
        self._info = {
            'type' : 'index',
            'name' : 'index',
            'data' : data,
            'path' : self.filepath
        }

class PackData(Data):
    def parse(self):
        import subprocess
        p = subprocess.Popen("git verify-pack -v "+self.filepath, shell=True, stdout=subprocess.PIPE)
        data = p.communicate()[0].decode('utf-8').strip()
        self._info = {
            'type' : 'pack',
            'name' : self.filepath,
            'data' : data,
            'path' : self.filepath
        }

class Factory:
    @staticmethod
    def getElement(path):
        if '.git/hooks' in path:
            return RefData(path)
        if '.git/objects/pack' in path:
            return PackData(path)
        elif '.git/objects' in path:
            return ObjectData(path)
        elif '.git/index' in path:
            return IndexData(path)