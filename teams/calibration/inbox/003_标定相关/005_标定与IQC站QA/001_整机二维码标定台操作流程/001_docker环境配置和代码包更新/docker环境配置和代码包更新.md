# docker环境配置和代码包更新

## docker环境配置

1. wsl -d wsl\_server（进入linux机器）

2. cd /opt/roborock/ ,并且把docker压缩文件放在此路径下

3. 将zip在wsl\_server里解压成tar包

unzip tartanlib\_\*.zip

* 整包docker替换

&#x20;       先删除有标签的旧镜像：docker rmi -f tartanlib:\*  (先用docker image ls看下旧的版本叫什么名字)

&#x20;       删除所有悬空镜像（没有标签的镜像）docker image prune

&#x20;       docker load -i tartanlib\_\*.tar

&#x20;       docker image ls -a（看docker是否更新）



## 代码包更新

1. 将install\_linux.tar.gz放置于linux下/opt/roborock手动操作

2. wsl -d wsl\_server

3. cd /opt/roborock/

4. rm -rf install\_linux（删除原始文件夹）

5. tar -xvf install\_linux\_\*.tar.gz（解压）

