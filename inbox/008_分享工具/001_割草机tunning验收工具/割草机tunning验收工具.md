# 割草机tunning验收工具

# 环境依赖

1. 系统为ubuntu，安装docker

2. 获取并按照tunning\_check镜像

   1. 执行命令：sudo docker load -i tunning\_check.tar

# 输入规范

1. 要求将文件放在某个目录下(input\_path)，可以嵌套多层，代码会递归地处理所有文件

2. input\_path为other用户开启读、写、执行权限

   1. chmod -R 777 \<input\_path>

3. 文件名以.yuv结尾，并且命名规则如下

   1. 相机0图像：AT\_图像高x图像宽\_一个数字\_一个数字\_时间戳\_IR0\_0.yuv

   2. 相机1图像：AT\_图像高x图像宽\_一个数字\_一个数字\_时间戳\_IR1\_0.yuv

   3. 如：

      1. AT\_1088x1280\_214\_16\_2838022\_IR0\_0.yuv

      2. AT\_1088x1280\_214\_17\_2838092\_IR1\_0.yuv

   4. 代码会将每个文件夹进行递归遍历，所有文件夹按字典序排序，文件夹内图像按照时间戳排序分别处理

# 代码调用方式

1. April grid识别

```bash
chmod -R 777 <input_path> # 文件夹创建后只需执行一次
sudo docker run --rm -v <input_path>:/home/roborock/frame tunning_check --save true
```

* 黑色亚克力板角点识别

```bash
chmod -R 777 <input_path> # 文件夹创建后只需执行一次
sudo docker run --rm -v <input_path>:/home/roborock/frame tunning_check --do_fast true --save true
```

* 如上所示，代码使用docker拉起，必须将输入图片的目录映射到镜像内

  1. 其中input\_path替换为实际图片路径

* 可以加入额外参数：

  1. \--save true/false 来指定是否保存可视化图片

     1. 例如：sudo docker run --rm -v \<input\_path>:/home/roborock/frame tunning\_check --save true

  2. \--do\_fast true/false 来指定是否进行角点检测

     1. 例如：sudo docker run --rm -v \<input\_path>:/home/roborock/frame tunning\_check --save true --do\_fast true

  3. 如果目标靶为黑色方板，则需要开启--do\_fast来进行焦点检测

  4. april\_grid提取默认打开



附件：

