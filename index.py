from bottle import route, run, template, post, get, request
from git_object import *

def pretty_date(time=False):
    """
    Get a datetime object or a int() Epoch timestamp and return a
    pretty string like 'an hour ago', 'Yesterday', '3 months ago',
    'just now', etc
    """
    from datetime import datetime
    now = datetime.now()
    if type(time) is int:
        diff = now - datetime.fromtimestamp(time)
    elif isinstance(time,datetime):
        diff = now - time
    elif not time:
        diff = now - now
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(int(second_diff / 60)) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(int(second_diff / 3600)) + " hours ago"
    if day_diff == 1:
        return "Yesterday"
    if day_diff < 7:
        return str(int(day_diff)) + " days ago"
    if day_diff < 31:
        return str(int(day_diff / 7)) + " weeks ago"
    if day_diff < 365:
        return str(int(day_diff / 30)) + " months ago"
    return str(int(day_diff / 365)) + " years ago"

@route('/hello')
@route('/hello/<name>')
def hello():
    _files = []
    for file in GitElement.getFileRecursivly('.git'):
        _files.append([file[0], pretty_date(int(file[1]))])
    return template('main', elements=_files)

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