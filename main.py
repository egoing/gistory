__author__ = 'egoing'
from git_object import *
import sys, os
#path = sys.argv[1]
path = '.git'
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
fileList.sort(key=operator.itemgetter(1))
for _file in fileList:
    if _file[2] in ['object']:
        print(ObjectData(_file[0]))
    elif _file[2] == 'index':
        print(IndexData(_file[0]))
    elif _file[2] == 'pack':
        print(PackData(_file[0]))
    else:
        print(TextData(_file[0]))