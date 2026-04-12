# 外参对slam算法影响测试

# 测试结论：

在外参roll、pitch及yaw在3°以内，对建图结果影响很小，可忽略



| 外参                   | roll: 0°pitch : 0°yaw: 0°                                                                                                                                                                                                                                 | roll: 3°pitch : 3°yaw: 3°                                                           | roll: 6°pitch : 6°yaw: 6°                                                           |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 建图效果（对齐后）：           | ![Image Token: LWDkbHP0XovnjPxYW4pctHRQnjh](images/LWDkbHP0XovnjPxYW4pctHRQnjh.png)![Image Token: ZpPPbDO1Eo9mygxjlFWc07Qnnmf](images/ZpPPbDO1Eo9mygxjlFWc07Qnnmf.png)                                                                                    |                                                                                     |                                                                                     |
| 建图轨迹：                | ![Image Token: VZySb1JNPopjmlx15jxchUfxnVh](images/VZySb1JNPopjmlx15jxchUfxnVh.png)                                                                                                                                                                       | ![Image Token: FWbcbcJVRonrsqxl0i0cuVugnrb](images/FWbcbcJVRonrsqxl0i0cuVugnrb.png) | ![Image Token: Arkgb56Zio08Z0xZ5G4crsYHnWg](images/Arkgb56Zio08Z0xZ5G4crsYHnWg.png) |
| &#xA;不同维度下轨迹对齐后的对比图： | ![Image Token: GNysbpB7aoQNTzxfAJJcetAfnHd](images/GNysbpB7aoQNTzxfAJJcetAfnHd.png)![Image Token: XqdWboo8goSVADx1Q5nc0SFVn7e](images/XqdWboo8goSVADx1Q5nc0SFVn7e.png)![Image Token: JNVbbFr0QoV3UOxtfndcVyV5np1](images/JNVbbFr0QoV3UOxtfndcVyV5np1.png) |                                                                                     |                                                                                     |

