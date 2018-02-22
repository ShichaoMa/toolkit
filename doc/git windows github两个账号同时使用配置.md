[comment]: <> (![](http://upload-images.jianshu.io/upload_images/3079674-a724f50b31ce43ab.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240))
首先在window上安装git时，取消勾选gui及enable git credential manager，随后安装完毕

### 现在有2账号A和B

#### 先使用A账号克隆代码

    
    
    $ git clone https://github.com/cnaafhvk/deer.git
    # 出现异常信息，不用管，输入帐号
       ֵ▒▒▒▒Ϊ null▒▒
    ▒▒▒▒▒▒: username
    error: unable to read askpass response from 'D:\Softwares\Git\mingw64\libexec\git-core\git-askpass.exe'
    Username for 'https://github.com':
    
    

#### 这时会弹出登录窗，输入账号密码登录，代码克隆成功，进入项目

    
    
    cd deer
    vi .git/config
    ### 把下面的代码粘到最后
    [credential]
        helper = store --file=.git/cred.txt
    

#### 拉代码

    
    
    git pull
    # 出现异常信息，不用管，输入帐号
       ֵ▒▒▒▒Ϊ null▒▒
    ▒▒▒▒▒▒: username
    error: unable to read askpass response from 'D:\Softwares\Git\mingw64\libexec\git-core\git-askpass.exe'
    Username for 'https://github.com':
    

#### 这时不会再弹出登录窗了，因为windows用户凭据中已经保存了密码，同时，在本地保存了密码

    
    
    $ cat .git/cred.txt
    https://cnaafhvk:04a7a2e73aec8c4051a16656991b752c336cd349@github.com
    

### 然后打开windows用户凭据，删除刚才保存的凭据

### 之后使用B账号重复上面的操作

### 最后再把凭证删除

###
如果还有其它账号，重复上面的步骤，如果其中一个账号还有其它项目，只需要配置credential后把同一帐号下面的.git/cred.txt进行复制即可。

参考资料

[如何切换多个GitHub账号](http://www.jianshu.com/p/0ad3d88c51f4)


[comment]: <tags> (git,windows)
[comment]: <description> (windows上在多个账号之间切换git)
[comment]: <title> (git windows github两个账号同时使用配置)
[comment]: <author> (夏洛之枫)