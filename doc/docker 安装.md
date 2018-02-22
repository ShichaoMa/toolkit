# 1. Set up the repository
```
sudo apt-get -y install \
  apt-transport-https \
  ca-certificates \
  curl
 
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) \
       stable"

sudo apt-get update
```
# 2. Get Docker CE
```
sudo apt-get -y install docker-ce
```
# 
[comment]: <tags> (docker)
[comment]: <description> (docker 安装方法)
[comment]: <title> (docker 安装)
[comment]: <author> (夏洛之枫)