[comment]: <> (![](https://timgsa.baidu.com/timg?image&quality=80&size=b9999_10000&sec=1507352875&di=6c7b70744b8441002f20401bf3c653ed&imgtype=jpg&er=1&src=http%3A%2F%2Fs6.51cto.com%2Fwyfs02%2FM02%2F23%2FC4%2FwKioL1NDWp2wpN3_AAA1lJYopPE427.gif))
- 打包
```
python setup.py sdist
```
- 新建文件`vi ~/.pypirc`
```
[distutils]
index-servers =
    pypi

[pypi]
repository: https://upload.pypi.org/legacy/
username: xxxx
password: xxxx
~                                                                                                                        
```
- 上传
```
python setup.py sdist upload
```
[comment]: <tags> (pip)
[comment]: <description> (pip的pypi上传包的方法)
[comment]: <title> (pypi使用方法)
[comment]: <author> (夏洛之枫)