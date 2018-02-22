[comment]: <> (![](https://udemy-images.udemy.com/course/750x422/752950_b773.jpg))
  * git查看当前修改内容

    
    
    git diff FILENAME
    

  * git 回退版本

    
    
    # 回退上一个版本
     git reset --hard HEAD^
    # 跳到某个版本（可以现在和未来的）
     git reset --hard 3628164
    

  * 查看历史命令

    
    
    git reflog
    

  * 删除分支

    
    
    git branch -d new

- 与远程分支进行比较

    git fetch origin
    git diff master origin/master

- git diff命令加减号说明
diff 第一个参数是src版本，第二个参数dest版本，src中拥有使用-号标注，dest使用+号标注，src没有时，默认src为当前前版本，dest为当前工作空间版本
    


[comment]: <tags> (git)
[comment]: <description> (git 命令大全)
[comment]: <title> (git 命令)
[comment]: <author> (夏洛之枫)