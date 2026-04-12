# VSLAM使用JPG测试

分别使用数据集四个场地的数据进行对比测试，评估轨迹rmse，前端跟踪质量统计值

1. jpg (95) 与png对比

   1. 前端跟踪质量轻微降低，主要体现在平均**连续跟踪**长度 (streak\_mean)

   2. rmse 整体略变低

   3. 长轨迹png优势会稍微明显一些

2. jpg (60) 与png对比

   1. 仅用于正确性验证，streak\_mean降低更多

## 1. jpg (95)

| sequence                            | png/rmse | jpg (95)/rmse | Track statistic                                                                     |                                                                                     |               | 轨迹                                                                                  | 备注             |
| ----------------------------------- | -------- | ------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------- | ----------------------------------------------------------------------------------- | -------------- |
| MK2-12\_circle                      | 0.240983 | 0.303674      | ![Image Token: FhmpbkI65ot1K9x0Aegct7JHnIe](images/FhmpbkI65ot1K9x0Aegct7JHnIe.png) | ![Image Token: O21pbZP6ToD4uAxKi7IcIgPCncg](images/O21pbZP6ToD4uAxKi7IcIgPCncg.png) | 8.700 / 8.553 | ![Image Token: Kxt0brteNo8AkHxqKYDcDipNnjg](images/Kxt0brteNo8AkHxqKYDcDipNnjg.png) |                |
|                                     | 0.192886 | 0.247963      | ![Image Token: PcR0bPlERoC33AxB5iFcmegmnFe](images/PcR0bPlERoC33AxB5iFcmegmnFe.png) | ![Image Token: Bnoeb4ZLboOWkix9vsjcBG3Nncb](images/Bnoeb4ZLboOWkix9vsjcBG3Nncb.png) | 8.774 / 8.461 |                                                                                     |                |
|                                     | 0.200546 | 0.211310      | ![Image Token: N1cmbdjcHoXRz4xT78IcCvzfn9e](images/N1cmbdjcHoXRz4xT78IcCvzfn9e.png) | ![Image Token: PyDvbZHOZo2eyvxVsUscdlfNndh](images/PyDvbZHOZo2eyvxVsUscdlfNndh.png) | 8.791 / 8.572 |                                                                                     |                |
| MK2-12\_lake2\_0.5m                 | 0.208479 | 0.259088      | ![Image Token: Uu2SbiIRso9xFlxN0cacajsinGd](images/Uu2SbiIRso9xFlxN0cacajsinGd.png) | ![Image Token: R7l4bX9HPoI1fCx8RdhcIorznBf](images/R7l4bX9HPoI1fCx8RdhcIorznBf.png) | 7.978 / 8.042 | ![Image Token: CJS2bKgWNo1MrwxXZo9cijccn1e](images/CJS2bKgWNo1MrwxXZo9cijccn1e.png) | 平均track长度无明显变化 |
|                                     | 0.204562 | 0.251294      | ![Image Token: ImZwbylwtoub5xxULRAcaqcWnIc](images/ImZwbylwtoub5xxULRAcaqcWnIc.png) | ![Image Token: XV04bRyVaoDCoPxt87bczspRnLg](images/XV04bRyVaoDCoPxt87bczspRnLg.png) | 7.922 / 8.008 |                                                                                     |                |
|                                     | 0.344020 | 0.248707      | ![Image Token: LgvrbrMdXonyEQxG5mGc2oxhn0g](images/LgvrbrMdXonyEQxG5mGc2oxhn0g.png) | ![Image Token: EztSbTW01om790xTD4gcu7Ebn4b](images/EztSbTW01om790xTD4gcu7Ebn4b.png) | 7.925 / 7.922 |                                                                                     |                |
| MK2-12\_normal\_z\_0.8m\_jpg        | 0.287595 | 0.269437      | ![Image Token: SNI6bvchPoGk2txUFhMcK9lQnqf](images/SNI6bvchPoGk2txUFhMcK9lQnqf.png) | ![Image Token: L2gEb1v2FoCpgdxx6OTclybNnoc](images/L2gEb1v2FoCpgdxx6OTclybNnoc.png) | 7.807 / 7.806 | ![Image Token: PsqObPvgsoH5xsxWr3OcC8ASnye](images/PsqObPvgsoH5xsxWr3OcC8ASnye.png) | 平均track长度无明显变化 |
|                                     | 0.447714 | 0.434448      | ![Image Token: ZPutbvqpDoZ3vYxvegGcO0Cvnpf](images/ZPutbvqpDoZ3vYxvegGcO0Cvnpf.png) | ![Image Token: BAxhb24Lfo6utsxlEJRcraS9nvd](images/BAxhb24Lfo6utsxlEJRcraS9nvd.png) | 7.747 / 7.826 |                                                                                     |                |
|                                     | 0.317058 | 0.328215      | ![Image Token: L3hwbTvs3oKwj2xSJe3cal6DnlW](images/L3hwbTvs3oKwj2xSJe3cal6DnlW.png) | ![Image Token: Oc4xbywc0oSLLAxY9eXcBkfFnlb](images/Oc4xbywc0oSLLAxY9eXcBkfFnlb.png) | 7.833 / 7.885 |                                                                                     |                |
| ydiff\_corrected\_B1-138\_corrected | 0.574777 | 0.615592      | ![Image Token: Baolb8qnto9BxAxUsuaczqACnIb](images/Baolb8qnto9BxAxUsuaczqACnIb.png) | ![Image Token: GwxGbpWdFoavBVx2CRfcIT6Rn8f](images/GwxGbpWdFoavBVx2CRfcIT6Rn8f.png) | 8.728 / 8.684 | ![Image Token: VWUNbmrEEoVfPFxcKFfcKi0xnBd](images/VWUNbmrEEoVfPFxcKFfcKi0xnBd.png) |                |
|                                     | 0.349510 | 0.462811      | ![Image Token: I2oEbaZhKovsibxMBAPc7jiynaf](images/I2oEbaZhKovsibxMBAPc7jiynaf.png) | ![Image Token: SiHIbD4cDoEr2CxTfb6cUcC7nl3](images/SiHIbD4cDoEr2CxTfb6cUcC7nl3.png) | 8.812 / 8.627 |                                                                                     |                |
|                                     | 0.322129 | 0.493829      | ![Image Token: EaIBbQD99oLuoFxLJBrchyZqnze](images/EaIBbQD99oLuoFxLJBrchyZqnze.png) | ![Image Token: AcDrbRoEZoAhhpxeiSxcnIwanVd](images/AcDrbRoEZoAhhpxeiSxcnIwanVd.png) | 8.759 / 8.657 |                                                                                     |                |

## 2. jpg (60)

| sequence                            | png/rmse | jpg (60)/rmse | Track statistic                                                                     |                                                                                     |               |
| ----------------------------------- | -------- | ------------- | ----------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- | ------------- |
| MK2-12\_circle                      | 0.200546 | 0.228091      | ![Image Token: Fq7Fb189uoOoGDx0FyccFBUDnlf](images/Fq7Fb189uoOoGDx0FyccFBUDnlf.png) | ![Image Token: XxkpbIYLool36WxpQ9Vc1r8MnFc](images/XxkpbIYLool36WxpQ9Vc1r8MnFc.png) | 8.791 / 7.329 |
| MK2-12\_lake2\_0.5m                 | 0.344020 | 0.219863      | ![Image Token: RjRxb6kvRornisxSD3JcEnX1nJd](images/RjRxb6kvRornisxSD3JcEnX1nJd.png) | ![Image Token: Oy2qb9ijboHhXNx9tNHcn2Hxngb](images/Oy2qb9ijboHhXNx9tNHcn2Hxngb.png) | 7.925 / 7.023 |
| MK2-12\_normal\_z\_0.8m             | 0.317058 | 0.357895      | ![Image Token: R8mfb4VDMoOlPWxhRsPcT82rnrh](images/R8mfb4VDMoOlPWxhRsPcT82rnrh.png) | ![Image Token: CihSbFWMLonsWSxruCUcvFOLnxe](images/CihSbFWMLonsWSxruCUcvFOLnxe.png) | 7.833 / 6.557 |
| ydiff\_corrected\_B1-138\_corrected | 0.322129 | 0.584125      | ![Image Token: P2YibsYzWoGpvex83xOcBEnhnwd](images/P2YibsYzWoGpvex83xOcBEnhnwd.png) | ![Image Token: LuiXbPWBPoZ3qOxBjaFcNrisnlb](images/LuiXbPWBPoZ3qOxBjaFcNrisnlb.png) | 8.759 / 7.622 |

