from bottle import route, run, template, post, get, request
from git_object import *

@route('/hello')
@route('/hello/<name>')
def hello():
    ge = GitElement('.git')
    return template('main', elements=ge.getAll())

from bottle import static_file
@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root='./views/static')

@route('/ajax/element', method='POST')
def ajax_element():
    path = request.forms.get('path')
    info = GitDataObjectFactory.getElement(path).info()
    return info

@route('/ajax/object', method='POST')
def ajax_object():
    path = request.forms.get('object')
    info = ObjectDataById(path).info()
    return info



run(host='localhost', port=8080, debug=True)