# 개발을 위해서 실행하는 방법
분석을 하려는 .git 디렉토리로 이동한 후에 아래 명령을 실행합니디.
python __main__.py

# 배포방법
setup.py의 version 값을 변경합니다.
배포 파일을 생성합니다.  
`python setup.py sdist bdist_wheel`
테스트 서버에 배포합니다. 
`twine upload --repository-url https://test.pypi.org/legacy/ dist/*`
개발서버에 배포합니다.
`twine upload --repository-url https://pypi.org/legacy/ dist/*`