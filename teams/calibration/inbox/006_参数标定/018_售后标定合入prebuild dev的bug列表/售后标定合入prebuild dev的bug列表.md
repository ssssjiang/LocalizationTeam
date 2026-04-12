# 售后标定合入prebuild dev的bug列表

| **合入日期**   | **合入分支**        | **pick分支**                       | ButchartcalibandcheckCOMMIT ID           | **bug**                                                                                                                                   |
| ---------- | --------------- | -------------------------------- | ---------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------- |
| 2026/4/2   | prebuid/develop | 2026/4/2 pick                    | fe9e9552a3f17dc2f626b28fc69fa68b8699b7b4 | 限制BA窗口以及删除无用变量来减少耗时和内存。&#xA;Bug#492211 - Butchart-售后标定模块-耗时 & 内存占用过多http://192.168.111.52/index.php?m=bug\&f=view\&t=html&=\&bugID=492211 |
| 2026/3/21  | prebuid/develop | 2026/3/25 pick                   | 49cfbbd1d74cc3339a8a75b5bef3250668252fbc | 修改toi的輸出順序爲按行                                                                                                                             |
| 2026/3/18  | prebuid/develop | 2026/3/19 pick                   | 931b0be2d3d6b2c0e7cb2df4cad8b41ab4509238 | 对于LDS机器和其他配置不同轨迹，并且筛掉售后标定用于lidar标定的数据来缩短计算时间。                                                                                             |
| 2026/3/9   | prebuid/develop | 2026/3/19 pick                   | caccd72db49d4db23b8c70cbfe21b622266f1e75 | 修复BA优化失败导致报635的问题                                                                                                                         |
| 2026/3/2   | prebuid/develop | 2026/3/19 pick                   | e7a7b225d2bf6ec6624af19f8350b94c8cef014f | 加入行差检测、售后行差标定、售后标定的第二次slam改为同时获取左右目的观测进行BA，得到优化后的Tcrcl。                                                                                   |
| 2026/2/5   | prebuid/develop | 2026/2/9 pick进HF1.0分支，3/6发线上版本带上 | 88e05955c70c61327881c1a03d7cd8a98a3e804f | 关掉侧目标定;toc的z固定为结构值。&#xA;http://192.168.111.52/index.php?m=bug\&f=view\&t=html\&id=437327                                                  |
| 2026/12/17 | prebuid/develop | 2026/12/19 pick                  | 72af7857cbdfcafe585f7dd65b8bc6d88b1e2f35 | 开了侧目标定容易标定失败;底部板子太厚导致toi的z容易标定失败。                                                                                                         |

