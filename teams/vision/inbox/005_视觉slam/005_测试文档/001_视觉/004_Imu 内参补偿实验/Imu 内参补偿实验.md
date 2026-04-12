# Imu 内参补偿实验

# MK2-12

| sequence                 | okvis2 private/songs/dev | imu intrinsic补偿 |
| ------------------------ | ------------------------ | --------------- |
| MK2-12\_lake2\_0.4m      | 0.164514                 | 0.154565        |
| MK2-12\_lake2\_0.5m      | 0.194985                 | 0.201556        |
| MK2-12\_normal\_z\_0.8m2 | 0.154039                 | 0.123865        |
|                          |                          |                 |
| MK2-12\_normal\_z\_0.4m  | 0.197084                 | 0.187263        |
| MK2-12\_normal\_z\_0.5m  | 0.276453                 | 0.177592        |
| MK2-12\_normal\_z\_0.8m  | 0.191282                 | 0.173605        |



> Imu 参数

```yaml
# imu parameters
imu_parameters:
    use: True
    a_max: 176.0
    g_max: 7.8
    sigma_g_c: 0.002
    sigma_a_c: 0.02
    sigma_bg: 0.01
    sigma_ba: 0.1
    sigma_gw_c: 2e-05
    sigma_aw_c: 0.002
    g: 9.81007
    
    # 初始bias
    g0: [ 0.001, 0.001, 0.002 ]
    a0: [ 0.1, -0.04, -0.12 ]
    # g0: [ 0.0, 0.0, 0.0 ]
    # a0: [ 0.0, 0.0, 0.0 ]
   
    # transform Body-Sensor (IMU)
    T_BS:
        [1.0000, 0.0000, 0.0000, 0.0000,
         0.0000, 1.0000, 0.0000, 0.0000,
         0.0000, 0.0000, 1.0000, 0.0000,
         0.0000, 0.0000, 0.0000, 1.0000]

    # factory intrinsic Calibration
    bg: [0.0011677597649395466, 0.0030051274225115776, -0.0017693043919280171]
    sg: [1.001610279083252, 0.99961006641387939, 0.9975619912147522]
    rg: [1,
         0.0065002413466572762,
         -0.0018954087281599641,
         -0.011348632164299488,
         1,
         0.010757584124803543,
         0.00066448800498619676,
         -0.0087396362796425819,
         1]

    ba: [0.066002614796161652, -0.031401805579662323, -0.08587453514337546]
    sa: [0.995108962059021, 0.99641090631484985, 0.99685221910476685]
    ra: [1,
         0.0017330222763121128,
         0.0014053317718207836,
         0,
         1,
         0.0061812316998839378,
         -0,
         0,
         1]
```



> estimated bias

plot okvis2-vio-calib-final\_trajectory.csv bias

|                          | 无内参补偿                                                                               | imu intrinsic补偿                                                                     |   |
| ------------------------ | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | - |
| MK2-12\_lake2\_0.4m      | ![Image Token: Oxx0bU8nsoCurSx30n7cxsKintt](images/Oxx0bU8nsoCurSx30n7cxsKintt.png) | ![Image Token: OEbnbd0pNonG3sxXHmrcc4xJnLb](images/OEbnbd0pNonG3sxXHmrcc4xJnLb.png) |   |
| MK2-12\_lake2\_0.5m      | ![Image Token: Y5t8bV3mmovhhMx9Tooc0FU2nwf](images/Y5t8bV3mmovhhMx9Tooc0FU2nwf.png) | ![Image Token: MDLVbBzasowGdNxIH7VcfGajn5e](images/MDLVbBzasowGdNxIH7VcfGajn5e.png) |   |
| MK2-12\_normal\_z\_0.4m  | ![Image Token: DFR8b4cRDovLdjxX3pncAAbgnee](images/DFR8b4cRDovLdjxX3pncAAbgnee.png) | ![Image Token: O1VObtOJPoYQcIxz9GgcKOWWnzf](images/O1VObtOJPoYQcIxz9GgcKOWWnzf.png) |   |
| MK2-12\_normal\_z\_0.5m  | ![Image Token: NghJbXDyloUSr9xkX86cLT5Hnbd](images/NghJbXDyloUSr9xkX86cLT5Hnbd.png) | ![Image Token: N4fcbVEQNopH6pxW4RNc4e3snvb](images/N4fcbVEQNopH6pxW4RNc4e3snvb.png) |   |
| MK2-12\_normal\_z\_0.8m  | ![Image Token: CIxrblmdVoCNK2xB8CpceX2bn9c](images/CIxrblmdVoCNK2xB8CpceX2bn9c.png) | ![Image Token: ZSuvbTOA1oKJEixAXtmcgpgPn5b](images/ZSuvbTOA1oKJEixAXtmcgpgPn5b.png) |   |
| MK2-12\_normal\_z\_0.8m2 | ![Image Token: IREHbwaBsoLc6rxjWtrc6v0dn7Q](images/IREHbwaBsoLc6rxjWtrc6v0dn7Q.png) | ![Image Token: QlyFbF6RzokQloxInincjsZrnAb](images/QlyFbF6RzokQloxInincjsZrnAb.png) |   |



# B1-37

| sequence               | okvis2 private/songs/dev |                                                                                     |                                                                                     | okvis2 imu intrinsic补偿 |                                                                                     |                                                                                     |
| ---------------------- | ------------------------ | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ---------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
|                        | metric                   | traj                                                                                | bias 收敛曲线                                                                           | metric                 | traj                                                                                | bias 收敛曲线                                                                           |
| B1-37\_7.22\_78\_lake  | 0.724851                 | ![Image Token: Dl4CbpQrKo7JaAxqZXhcPN1ynee](images/Dl4CbpQrKo7JaAxqZXhcPN1ynee.png) | ![Image Token: BJOMb7isBofHNrxqkZVcDiEWnjg](images/BJOMb7isBofHNrxqkZVcDiEWnjg.png) | 0.509411               | ![Image Token: ONmHbk6OaodY7FxOCvecg6ADnsb](images/ONmHbk6OaodY7FxOCvecg6ADnsb.png) | ![Image Token: SUX9bhsLloIQkmxm5Q9c9WX2nYd](images/SUX9bhsLloIQkmxm5Q9c9WX2nYd.png) |
| B1-37\_7.22\_105\_lake | 0.837941                 | ![Image Token: ZGdhbcDUfooHNxxLKibcCWOvnCg](images/ZGdhbcDUfooHNxxLKibcCWOvnCg.png) | ![Image Token: GvC6bjhJvofaOXxswnucyD7rnug](images/GvC6bjhJvofaOXxswnucyD7rnug.png) | 0.379320               | ![Image Token: VC5ablRLqoffITxtdoVcoX99nEc](images/VC5ablRLqoffITxtdoVcoX99nEc.png) | ![Image Token: VjD1bQpvQoUfPex2583cuV19nmd](images/VjD1bQpvQoUfPex2583cuV19nmd.png) |

注：bias 曲线根据okvis2-vio-calib-final\_trajectory.csv文件绘制

imu参数

```yaml
# imu parameters
imu_parameters:
    use: True
    a_max: 176.0
    g_max: 7.8
    sigma_g_c: 0.002
    sigma_a_c: 0.02
    sigma_bg: 0.01
    sigma_ba: 0.1
    sigma_gw_c: 2e-05
    sigma_aw_c: 0.002
    g: 9.81007
 
    # 初始bias
    g0: [ 0.001, 0.001, 0.002 ]
    a0: [ 0.1, -0.04, -0.12 ]
    # g0: [ 0.0, 0.0, 0.0 ]
    # a0: [ 0.0, 0.0, 0.0 ]
    # transform Body-Sensor (IMU)
    T_BS:
        [1.0000, 0.0000, 0.0000, 0.0000,
         0.0000, 1.0000, 0.0000, 0.0000,
         0.0000, 0.0000, 1.0000, 0.0000,
         0.0000, 0.0000, 0.0000, 1.0000]

    # factory intrinsic Calibration
    bg: [0.0008738157921470702, 0.0003471509844530374, 0.0022113516461104155]
    sg: [1.0014069080352783, 1.0024261474609375, 1.0043200254440308]
    rg: [1,
         -0.00597250135615468,
         0.0012812841450795531,
         0.006941819563508034,
         1,
         0.00791317503899336,
         -0.0014196711126714945,
         -0.007227293215692043,
         1]

    ba: [0.014490509405732155, -0.0745948702096939, 0.1507956087589264]
    sa: [1.005057692527771, 1.00243616104126, 1.007644534111023]
    ra: [1,
         -0.0010287488112226129,
         0.00032652070512995124,
         0,
         1,
         0.0083936108276248,
         0,
         0,
         1]
```
