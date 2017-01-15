#!/usr/bin/env python3
import argparse
import os
import sys

from gistory import bottle
from gistory.bottle import route, run, template, post, get, request
from gistory.git_object import *

packagePath = os.path.dirname(bottle.__file__)

parser = argparse.ArgumentParser()
parser.add_argument("path", help="Path of .git directory.", nargs='?')
parser.add_argument("-p", "--port", help="Web server port", type=int)
args = parser.parse_args()
path = args.path if args.path else './'


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
    elif isinstance(time, datetime):
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


@route('/')
def hello():
    _files = []
    for file in GitElement.getFileRecursivly(path + '.git'):
        _files.append([file[0], pretty_date(int(file[1]))])
    return template(os.path.join(packagePath,'views','main'), elements=_files)


from gistory.bottle import static_file


@route('/static/<filename>')
def server_static(filename):
    return static_file(filename, root=os.path.join(packagePath,'views','static'))


@route('/ajax/element', method='POST')
def ajax_element():
    path = request.forms.get('path')
    info = GitDataObjectFactory.getElement(path).info()
    return info


@route('/ajax/object', method='POST')
def ajax_object():
    obj = request.forms.get('object')
    info = ObjectDataById(obj, path).info()
    return info


def main():
    _port = args.port if args.port else 8805
    run(host='localhost', port=_port, debug=True)


if __name__ == "__main__":
    main()
