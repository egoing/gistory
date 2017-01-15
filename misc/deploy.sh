# ~/.pypirc 파일을 아래와 같이 셋팅한다
#    [distutils]
#    index-servers=
#        pypi
#        pypitest
#
#    [pypi]
#    repository = https://pypi.python.org/pypi
#    username =
#    password =
#
#    [pypitest]
#    repository = https://testpypi.python.org/pypi
#    username =
#    password =

python3 setup.py sdist upload -r pypi