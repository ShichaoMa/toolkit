### ubuntu下python安装包setup.py中由于读取了带有中文件的文件导致的编码题
```python
Collecting pyaop (from apistellar>=1.0.30)
  Using cached https://files.pythonhosted.org/packages/b5/6d/4a39bf5f225c9925b26122c663860118999b262c4db293c74f435bfb0da0/pyaop-0.0.6.tar.gz
    Complete output from command python setup.py egg_info:
    Traceback (most recent call last):
      File "<string>", line 1, in <module>
      File "/tmp/pip-install-33yvlkcn/pyaop/setup.py", line 34, in <module>
        VERSION = get_version("pyaop")
      File "/tmp/pip-install-33yvlkcn/pyaop/setup.py", line 14, in get_version
        init_py = open(os.path.join(package, '__init__.py')).read()
      File "/root/.pyenv/versions/3.6.5/lib/python3.6/encodings/ascii.py", line 26, in decode
        return codecs.ascii_decode(input, self.errors)[0]
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xe4 in position 297: ordinal not in range(128)
```
#### 问题原因
这个问题很明显是由于`init_py = open(os.path.join(package, '__init__.py')).read()`
这一行读了一个有中文注释的__init__.py文件，而系统本身默认是ascii的，所以导致报错。
#### 解决方案

```
export LC_ALL=zh_CN.UTF-8
```
有些系统没有安中文。可能会出现以下报错：
```
bash: warning: setlocale: LC_ALL: cannot change locale (zh_CN.UTF-8)
```
解决方案是安装新的语言包或者
```
export LC_ALL=en_US.UTF-8
```
