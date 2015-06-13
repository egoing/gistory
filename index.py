from bottle import route, run, template, post, get, request
from git_object import *

def _git_viewer():
    import sys, os, operator
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
    fileList.sort(key=operator.itemgetter(1))
    return fileList

@route('/hello')
@route('/hello/<name>')
def hello():
    elements = []
    for _file in _git_viewer():
        e = Factory.getElement(_file[0])
        if e != None:
            elements.append(e)
    return template('main', elements=elements)

from bottle import static_file
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./views/static')

@route('/ajax/element', method='POST')
def ajax_element():
    path = request.forms.get('path')
    info = Factory.getElement(path).info()
    info['data'] = info['data'].replace('\n','<br>\n')
    return info


run(host='localhost', port=8080, debug=True)