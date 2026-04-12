# Deep Image Matching

# 初步结论

基于割草机数据，5070显卡，评估各pretrained model，Metric包括：Matching Score、相对pose精度与速度：

1. aliked与disk综合较优（aliked > disk），aliked特征点为亚像素，disk为整数像素

2. lightglue内点率与相对pose精度优于NN（最近邻），速度略低于NN，在共视小的情况下，lightglue优势会更明显

3. superpoint 尾部点质量较差，相对pose精度中等

4. xfeat 比较轻量，速度最快，精度略低

5. dedode内点率较低，相对pose精度较高，速度较慢

# model

![Image Token: PEfUbYcg2oNPsqxQ6yrc2yjznmd](images/PEfUbYcg2oNPsqxQ6yrc2yjznmd.png)



| model      | 描述子维度 | pretrained model             | 输入channel | 关键点精度 |
| ---------- | ----- | ---------------------------- | --------- | ----- |
| xfeat      | 64    | verlab/accelerated\_features | 3         | 整数像素  |
| DeDoDe     | 256   | L-upright / B-upright        | 3         | 整数像素  |
| aliked     | 128   | aliked-n16                   | 3         | 亚像素   |
| disk       | 128   | depth                        | 3         | 整数像素  |
| r2d2       | 128   | r2d2\_WASF\_N16              | 3         | 亚像素   |
| superpoint | 256   | superpoint\_v1               | 1         | 整数像素  |
| sift       | 128   | -                            | 1         | 亚像素   |

# pipeline

## 1. Matching Score

low level指标Matching Score的计算逻辑为：检测得到$$\mathrm{K}$$个关键点，Feature Match后得到匹配经RANSAC后，内点数与$$\mathrm{K}$$的比值，横向对比基于相同的$$\mathrm{K}$$。

$$\mathrm{Matching\ Score} = \frac{\mathrm{RANSAC}内点数}{\mathrm{K}}\tag{1}$$

## 2. 相对pose评估

两视图几何可以估计$$\hat{\boldsymbol{R}}$$，与平移方向$$\hat{\boldsymbol{t}}$$（up to scale），Maplab提供6DoF真值，由此可以评估旋转误差与平移方向误差

旋转误差

$$\Delta \boldsymbol{\theta}^{\mathrm{rot}}_{i}=\mathrm{arccos}\left(\frac{1}{2}\left(\mathrm{tr}\left(\boldsymbol{R}_i^{T}\cdot\hat{\boldsymbol{R}}_i\right)-1\right)\right)\tag{2}$$

平移误差

$$\Delta\boldsymbol{\theta}^{\mathrm {trans}}_i=\mathrm{arccos}\left( \frac{\hat{\boldsymbol t}_i^{T}\boldsymbol{t}_i}{\Vert\hat{\boldsymbol t}_i\Vert\Vert \boldsymbol{t}_i \Vert} \right)\tag{3}$$

取旋转平移最大的误差作为pose误差



$$\epsilon_i = \mathrm{max}\left(\Delta \boldsymbol{\theta}^{\mathrm{rot}}_{i},\ \Delta\boldsymbol{\theta}^{\mathrm {trans}}_i\right)\tag{4}$$

评估不同误差阈值下的成功率，AUC ( Area Under the Curve ).

## 3. 速度

统计模型推理时间，包括一次检测模型推理时间与一次match模型推理时间，NN的match使用双向最近邻 + ratio-test，测试平台：NVIDIA GeForce RTX 5070

# 评估结果

## 4. Matching Score vs 速度

### K=2000

模型输出topK=2000，同时评估不同图像间隔的两帧图像Matching Score 与 Inference Time

#### Interval = 1

![Image Token: TAXtbL6TAonbxFxCRubcKAyenKh](images/TAXtbL6TAonbxFxCRubcKAyenKh.png)

#### Interval = 3

![Image Token: QEbLbUhgoo2mmLxC7cZc5NldnAc](images/QEbLbUhgoo2mmLxC7cZc5NldnAc.png)

#### Interval = 5

![Image Token: QXwxbMvZ1oqBTNxludvcVGCUnGe](images/QXwxbMvZ1oqBTNxludvcVGCUnGe.png)

### K=400

在模型输出2000个点的基础上进一步使用 nms + topK 筛选出400个关键点

![Image Token: HvpbbunY4o5iHrx2RHkcTPw2nKd](images/HvpbbunY4o5iHrx2RHkcTPw2nKd.png)

## 5. 相对pose评估

| Detector-Descriptor | Matcher     | Keypoints = 2000          |                                                                                     |                                                                                     | Keypoints = 400           |                                                                                     |                                                                                     |
| ------------------- | ----------- | ------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
|                     |             | **Pose auc**              | Angle auc curve                                                                     | Trans auc curve                                                                     | **Pose auc**              | Angle auc curve                                                                     | Trans auc curve                                                                     |
| aliked              | lightglue   | **57.73 / 76.56 / 87.77** | ![Image Token: VGJSbkmVUonK1LxZjCecLK6ZnAh](images/VGJSbkmVUonK1LxZjCecLK6ZnAh.png) | ![Image Token: DiIcb0SawoBm9kxkYuRcXLpvnTc](images/DiIcb0SawoBm9kxkYuRcXLpvnTc.png) | **55.95 / 73.60 / 85.15** | ![Image Token: HWn7bZB3ionVAnxznrOcphFmnjh](images/HWn7bZB3ionVAnxznrOcphFmnjh.png) | ![Image Token: CXdgbBrmZojv0Gx5i7LcXzArnOf](images/CXdgbBrmZojv0Gx5i7LcXzArnOf.png) |
| disk                | lightglue   | **57.77 / 75.97 / 87.13** | ![Image Token: SUVSbMcFvoI74PxytM0cx7JPnsh](images/SUVSbMcFvoI74PxytM0cx7JPnsh.png) | ![Image Token: WbF9bly2AoIJulxZSJCcqJ37nqg](images/WbF9bly2AoIJulxZSJCcqJ37nqg.png) | **42.20 / 61.42 / 76.28** | ![Image Token: XwJ7bLz7wolZkJxfF34cekl3nff](images/XwJ7bLz7wolZkJxfF34cekl3nff.png) | ![Image Token: VLYUb5CWpoLLOBx7mMFcM7yFnhe](images/VLYUb5CWpoLLOBx7mMFcM7yFnhe.png) |
| dedode              | MNN-ratio   | 43.89 / 63.82 / 78.24     | ![Image Token: LOV6b34HJoZMmPxUIQIcBHNMnOc](images/LOV6b34HJoZMmPxUIQIcBHNMnOc.png) | ![Image Token: WtTNbn4GKoRJh5xoCBMcsl9jnBb](images/WtTNbn4GKoRJh5xoCBMcsl9jnBb.png) | 39.15 / 56.21 / 70.03     | ![Image Token: QuHIbwZNqoEtFtxaQttcAXxQnbU](images/QuHIbwZNqoEtFtxaQttcAXxQnbU.png) | ![Image Token: GGzSbapbso9lBQx49SCciCIknNe](images/GGzSbapbso9lBQx49SCciCIknNe.png) |
| superpoint          | superglue   | 40.09 / 57.19 / 71.57     | ![Image Token: V3WwbeiluoSt7dx2EfTcVWdBnsf](images/V3WwbeiluoSt7dx2EfTcVWdBnsf.png) | ![Image Token: KUYlbAoiaoGSI3xwewucH1jUndh](images/KUYlbAoiaoGSI3xwewucH1jUndh.png) | 41.80 / 59.09 / 72.82     | ![Image Token: NfQob7m1aoYEaQxK1JDcUXL3nob](images/NfQob7m1aoYEaQxK1JDcUXL3nob.png) | ![Image Token: RcS9bn19ooCgPsx8pPZcszrunC5](images/RcS9bn19ooCgPsx8pPZcszrunC5.png) |
| aliked              | MNN-ratio   | 38.58 / 58.95 / 75.40     | ![Image Token: EZlSbIY58oSdvSxaWLPcCChKnze](images/EZlSbIY58oSdvSxaWLPcCChKnze.png) | ![Image Token: BvGybnDybogYusxDjGMcxPH0nx4](images/BvGybnDybogYusxDjGMcxPH0nx4.png) | **45.05 / 63.81 / 78.75** | ![Image Token: VCOxbRIuqoXslExWbOZc032GnLh](images/VCOxbRIuqoXslExWbOZc032GnLh.png) | ![Image Token: JhbEbEdvxoANyoxDMgWck52ennV](images/JhbEbEdvxoANyoxDMgWck52ennV.png) |
| superpoint          | lightglue   | 36.79 / 55.16 / 70.42     | ![Image Token: X0Vub1hFOox4OixdF40cMm9Fnqh](images/X0Vub1hFOox4OixdF40cMm9Fnqh.png) | ![Image Token: DN50b3ANao7iQZxced8cPZQWnbd](images/DN50b3ANao7iQZxced8cPZQWnbd.png) | 39.01 / 57.56 / 73.11     | ![Image Token: QN5QbUbsDo5FQ7xhjfdcMcawnmj](images/QN5QbUbsDo5FQ7xhjfdcMcawnmj.png) | ![Image Token: MmChb2VIvo1tVRxwTdTclhu4nTf](images/MmChb2VIvo1tVRxwTdTclhu4nTf.png) |
| sift                | lightglue   | 34.33 / 54.02 / 70.96     | ![Image Token: J9UxbSJCeoGo9lxb3Avcthj2nVg](images/J9UxbSJCeoGo9lxb3Avcthj2nVg.png) | ![Image Token: TroBbK3p4oaZuQxYLcJc6xecnod](images/TroBbK3p4oaZuQxYLcJc6xecnod.png) | 27.05 / 46.49 / 65.12     | ![Image Token: Ef3JbIhBLomkRVxwiNMcXVS0n1g](images/Ef3JbIhBLomkRVxwiNMcXVS0n1g.png) | ![Image Token: NDsLb859boaVtpx1j6Uc7b0Fnnf](images/NDsLb859boaVtpx1j6Uc7b0Fnnf.png) |
| xfeat               | lighterglue | 30.50 / 49.20 / 66.46     | ![Image Token: AEltbqe2NocHkMx1vG2cfdJJnzb](images/AEltbqe2NocHkMx1vG2cfdJJnzb.png) | ![Image Token: PDB5bbaRjo7Wt0xG8fGcqySCnro](images/PDB5bbaRjo7Wt0xG8fGcqySCnro.png) | 23.46 / 39.00 / 55.76     | ![Image Token: NfS4bGGbNo1ML7xs8AAcdW05nAc](images/NfS4bGGbNo1ML7xs8AAcdW05nAc.png) | ![Image Token: Paf7ba60uoMNZQxHpZCc07cunWh](images/Paf7ba60uoMNZQxHpZCc07cunWh.png) |
| superpoint          | MNN-dist    | 30.15 / 49.28 / 67.06     | ![Image Token: VLdQb984JoFOtOxsilMcRzbtniC](images/VLdQb984JoFOtOxsilMcRzbtniC.png) | ![Image Token: MclSbqmZUoAcJjxUK10cmXX3ndd](images/MclSbqmZUoAcJjxUK10cmXX3ndd.png) | 30.35 / 49.91 / 67.94     | ![Image Token: MRWAb1dHGoIf2wxw0rAc8OdlnEd](images/MRWAb1dHGoIf2wxw0rAc8OdlnEd.png) | ![Image Token: DcHzbFF8ioXL5kxLzv9c7PNNnWf](images/DcHzbFF8ioXL5kxLzv9c7PNNnWf.png) |
| sift                | MNN-ratio   | 27.50 / 46.13 / 63.26     | ![Image Token: ZNmGbnnBJoQrQYx0THScttknnJh](images/ZNmGbnnBJoQrQYx0THScttknnJh.png) | ![Image Token: G9hPbow0wow3oXxxz32cZVadnYR](images/G9hPbow0wow3oXxxz32cZVadnYR.png) | 20.17 / 37.75 / 56.49     | ![Image Token: VIn1bxRONo8NR3xJaCUcriLanrb](images/VIn1bxRONo8NR3xJaCUcriLanrb.png) | ![Image Token: RJWQbds6RoZmCnxrv8nc6dbvn3Q](images/RJWQbds6RoZmCnxrv8nc6dbvn3Q.png) |
| disk                | MNN-ratio   | 23.78 / 45.43 / 65.65     | ![Image Token: RYiKbKZZiox9uBx38dJcjCFwnMb](images/RYiKbKZZiox9uBx38dJcjCFwnMb.png) | ![Image Token: MXGrbe9QmoTh5kx2WiGcUm7KnZd](images/MXGrbe9QmoTh5kx2WiGcUm7KnZd.png) | 26.14 / 43.83 / 61.83     | ![Image Token: Se9vb4dgUoR0ZQxD5wtcYrbonUJ](images/Se9vb4dgUoR0ZQxD5wtcYrbonUJ.png) | ![Image Token: T2JVbx5U8oKtClxJQrHcPwIVnk9](images/T2JVbx5U8oKtClxJQrHcPwIVnk9.png) |
| xfeat               | MNN-ratio   | 16.71 / 33.58 / 53.98     | ![Image Token: CJGKbu52soShIOxpPzmct6jCnjd](images/CJGKbu52soShIOxpPzmct6jCnjd.png) | ![Image Token: XrGcbAZP7okMuMx0OOAc1rebnnh](images/XrGcbAZP7okMuMx0OOAc1rebnnh.png) | 12.30 / 27.50 / 47.20     | ![Image Token: QQTfbEcdhoLRoIxdbZycCiqNnJc](images/QQTfbEcdhoLRoIxdbZycCiqNnJc.png) | ![Image Token: IKDKbGakWo5RLKx0Yydc30Pqnrj](images/IKDKbGakWo5RLKx0Yydc30Pqnrj.png) |
| r2d2                | MNN-ratio   | 12.26 / 27.50 / 45.88     | ![Image Token: DtFTbMp3nowN9uxhNipc45xCnhe](images/DtFTbMp3nowN9uxhNipc45xCnhe.png) | ![Image Token: HZ7ibHqyCo9Yr4xifQOcLJ2envh](images/HZ7ibHqyCo9Yr4xifQOcLJ2envh.png) | 17.59 / 34.60 / 53.28     | ![Image Token: BXDhbHNRooAhbpxsWH7cOTp3nBV](images/BXDhbHNRooAhbpxsWH7cOTp3nBV.png) | ![Image Token: GvRybGgtaommMGx7RjicZpsvncd](images/GvRybGgtaommMGx7RjicZpsvncd.png) |



# Detail

| model                  | K = 2000, interval = 1                                                              |
| ---------------------- | ----------------------------------------------------------------------------------- |
| Xfeat + lightglue      | ![Image Token: SRlCbS9rxoDOPUxseRZc3hxjnMc](images/SRlCbS9rxoDOPUxseRZc3hxjnMc.png) |
| Xfeat + NN             | ![Image Token: A7Dib2YYJo6DsHx7bwJctYBlndh](images/A7Dib2YYJo6DsHx7bwJctYBlndh.png) |
| Dedode + NN            | ![Image Token: C3dGb3DwLotLAJxb62AcGToVnce](images/C3dGb3DwLotLAJxb62AcGToVnce.png) |
| Aliked + lightglue     | ![Image Token: WxoXbAe3moWhLbxHsrWch12WnQK](images/WxoXbAe3moWhLbxHsrWch12WnQK.png) |
| Aliked + NN            | ![Image Token: YF9vbYhOpocnbSxXEV2cPb1VnAb](images/YF9vbYhOpocnbSxXEV2cPb1VnAb.png) |
| Disk + lightglue       | ![Image Token: NwMnbeTJFoZpqPxKn0acdLv2nmb](images/NwMnbeTJFoZpqPxKn0acdLv2nmb.png) |
| Disk + NN              | ![Image Token: P0zYbN3WGoBSXDxU0DEcHskynmh](images/P0zYbN3WGoBSXDxU0DEcHskynmh.png) |
| r2d2 + NN              | ![Image Token: FjVobpTgnoUiVjxFX2OcLtuNnlg](images/FjVobpTgnoUiVjxFX2OcLtuNnlg.png) |
| Superpoint + superglue | ![Image Token: K5CvbwjacoOfVDxtCpGcXkQ6n4d](images/K5CvbwjacoOfVDxtCpGcXkQ6n4d.png) |
| Superpoint + lightglue | ![Image Token: NMLIb8kZaoM1swxFdOicvCfgnUb](images/NMLIb8kZaoM1swxFdOicvCfgnUb.png) |
| Superpoint + NN        | ![Image Token: KXExbb35vocYj5xU8t3chLs0ndg](images/KXExbb35vocYj5xU8t3chLs0ndg.png) |

