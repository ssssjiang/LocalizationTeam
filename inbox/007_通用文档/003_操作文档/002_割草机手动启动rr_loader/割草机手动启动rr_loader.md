# 割草机手动启动rr_loader

rradb default shell killall -SIGUSR2 WatchDoge

rradb default shell ". /etc/profile; rrlogd /opt/rockrobo/rrlog/rrlog.conf"

另起终端：

rradb default shell "rr\_loader -c /opt/rockrobo/cleaner/conf/config.json"

