__author__ = 'egoing'
import sys, os
#path = sys.argv[1]
path = '.'
for dirname, dirnames, filenames in os.walk(path):
    print(dirname)