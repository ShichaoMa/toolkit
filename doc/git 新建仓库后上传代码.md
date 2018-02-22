[comment]: <> (![](https://julienrenaux.fr/wp-content/uploads/2013/10/git-770x605.png))
### 初始化仓库

    
    
    git init
    

### 添加文件

    
    
    git add -A # 添加所有文件，可以使用.gitignore排除不必添加的文件
    

### 从远程仓库拉取数据

    
    
     git pull https://github.com/derekluo/jay-cluster-captcha-jomashop.git master
    

### 手动或自动合并冲突，并添加提交

    
    
    git add 
    git commit
    

### 添加远程仓库

    
    
    git remote add origin https://github.com/derekluo/jay-cluster-captcha-jomashop.git

    
### 推送远程仓库， 为推送当前分支并建立与远程上游的跟踪

    
    
    git push --set-upstream origin master
    

注：origin指的是远程仓库的一个别名， master是一个分支

    
    
    git branch -v # 查看本地分支
    * master b03b633 commit
    
    git remote -v # 查看远程仓库
    origin  https://github.com/derekluo/jay-cluster-captcha-jomashop.git (fetch)
    origin  https://github.com/derekluo/jay-cluster-captcha-jomashop.git (push)
    
    

若之前操作有误，出现如下错误：

    
    
    fatal: refusing to merge unrelated histories
    

则在运行

    
    
    git pull https://github.com/derekluo/flume-cosmo-intercepror.git master --allow-unrelated-histories
    

参考资料[Git 的origin和master分析
](http://blog.csdn.net/abo8888882006/article/details/12375091)


[comment]: <tags> (git)
[comment]: <description> (git新建仓库后上传代码的方法)
[comment]: <title> (git 新建仓库后上传代码)
[comment]: <author> (夏洛之枫)