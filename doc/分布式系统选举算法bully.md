[comment]: <> (![](http://www.lanceyan.com/wp-content/uploads/2013/12/mongorep3.png))
[分布式系统理论基础 - 选举、多数派和租约](http://www.cnblogs.com/bangerlee/p/5767845.html)

## raft算法举例说明

- 现有小红小明小刚3个人，要选出一个leader
  - 初次启动，没有leader，所以发起选举
    - term = 1，小红，小明，小刚作为follower等待leader发来的heartbeat
    - 由于所有follower的的定时器时长是不同的，必定有部分follower依次变成candidate,为什么说依次，因为假设小红先变成了candidate，在向小明和小刚发送vote for me 时，网络比较慢，与此同时小刚的定时器也到时间了变成了candidate，所以就存在2个candidate。
    - 按假设进行，此时，小红和小刚term=2,小明保持term = 1，小刚和小红分别收到了对方的vote for me，均不予理会，小明先收到了小红的vote for me，小明term同步到了2,并投票给小红，小红现在有两票（自己的+小明的），小刚等待定时器超时后（假设这期间没有收到小红的heartbeat），重新发起了选举term变成3，而这个时候小红收到了小刚的vote for me 发现自己的term=2小于小刚的term=3，则恢复成了跟随者的状态，[如果一个候选人或者领导者发现自己的任期号过期了，那么他会立即恢复成跟随者状态]，并向小刚投票，则小刚成为了新的leader


参考[寻找一种易于理解的一致性算法（扩展版）](https://github.com/maemual/raft-zh_cn/blob/master/raft-zh_cn.md)

[comment]: <tags> (分布式,bully,算法)
[comment]: <description> (分布式系统选举算法)
[comment]: <title> (分布式系统选举算法bully)
[comment]: <author> (夏洛之枫)