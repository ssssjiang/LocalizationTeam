# VSLAM使用JPG测试

分别使用数据集四个场地的数据进行对比测试，评估轨迹rmse，前端跟踪质量统计值

1. jpg (95) 与png对比
  1. 前端跟踪质量轻微降低，主要体现在平均**连续跟踪**长度 (streakmean)
  2. rmse 整体略变低
  3. 长轨迹png优势会稍微明显一些
2. jpg (60) 与png对比
  1. 仅用于正确性验证，streakmean降低更多

## 1. jpg (95)


| sequence                      | png/rmse | jpg (95)/rmse | Track statistic                          |                                          |               | 轨迹                                       | 备注             |
| ----------------------------- | -------- | ------------- | ---------------------------------------- | ---------------------------------------- | ------------- | ---------------------------------------- | -------------- |
| MK2-12circle                  | 0.240983 | 0.303674      | Image Token: FhmpbkI65ot1K9x0Aegct7JHnIe | Image Token: O21pbZP6ToD4uAxKi7IcIgPCncg | 8.700 / 8.553 | Image Token: Kxt0brteNo8AkHxqKYDcDipNnjg |                |
|                               | 0.192886 | 0.247963      | Image Token: PcR0bPlERoC33AxB5iFcmegmnFe | Image Token: Bnoeb4ZLboOWkix9vsjcBG3Nncb | 8.774 / 8.461 |                                          |                |
|                               | 0.200546 | 0.211310      | Image Token: N1cmbdjcHoXRz4xT78IcCvzfn9e | Image Token: PyDvbZHOZo2eyvxVsUscdlfNndh | 8.791 / 8.572 |                                          |                |
| MK2-12lake20.5m               | 0.208479 | 0.259088      | Image Token: Uu2SbiIRso9xFlxN0cacajsinGd | Image Token: R7l4bX9HPoI1fCx8RdhcIorznBf | 7.978 / 8.042 | Image Token: CJS2bKgWNo1MrwxXZo9cijccn1e | 平均track长度无明显变化 |
|                               | 0.204562 | 0.251294      | Image Token: ImZwbylwtoub5xxULRAcaqcWnIc | Image Token: XV04bRyVaoDCoPxt87bczspRnLg | 7.922 / 8.008 |                                          |                |
|                               | 0.344020 | 0.248707      | Image Token: LgvrbrMdXonyEQxG5mGc2oxhn0g | Image Token: EztSbTW01om790xTD4gcu7Ebn4b | 7.925 / 7.922 |                                          |                |
| MK2-12normalz0.8mjpg          | 0.287595 | 0.269437      | Image Token: SNI6bvchPoGk2txUFhMcK9lQnqf | Image Token: L2gEb1v2FoCpgdxx6OTclybNnoc | 7.807 / 7.806 | Image Token: PsqObPvgsoH5xsxWr3OcC8ASnye | 平均track长度无明显变化 |
|                               | 0.447714 | 0.434448      | Image Token: ZPutbvqpDoZ3vYxvegGcO0Cvnpf | Image Token: BAxhb24Lfo6utsxlEJRcraS9nvd | 7.747 / 7.826 |                                          |                |
|                               | 0.317058 | 0.328215      | Image Token: L3hwbTvs3oKwj2xSJe3cal6DnlW | Image Token: Oc4xbywc0oSLLAxY9eXcBkfFnlb | 7.833 / 7.885 |                                          |                |
| ydiffcorrectedB1-138corrected | 0.574777 | 0.615592      | Image Token: Baolb8qnto9BxAxUsuaczqACnIb | Image Token: GwxGbpWdFoavBVx2CRfcIT6Rn8f | 8.728 / 8.684 | Image Token: VWUNbmrEEoVfPFxcKFfcKi0xnBd |                |
|                               | 0.349510 | 0.462811      | Image Token: I2oEbaZhKovsibxMBAPc7jiynaf | Image Token: SiHIbD4cDoEr2CxTfb6cUcC7nl3 | 8.812 / 8.627 |                                          |                |
|                               | 0.322129 | 0.493829      | Image Token: EaIBbQD99oLuoFxLJBrchyZqnze | Image Token: AcDrbRoEZoAhhpxeiSxcnIwanVd | 8.759 / 8.657 |                                          |                |


## 2. jpg (60)


| sequence                      | png/rmse | jpg (60)/rmse | Track statistic                          |                                          |               |
| ----------------------------- | -------- | ------------- | ---------------------------------------- | ---------------------------------------- | ------------- |
| MK2-12circle                  | 0.200546 | 0.228091      | Image Token: Fq7Fb189uoOoGDx0FyccFBUDnlf | Image Token: XxkpbIYLool36WxpQ9Vc1r8MnFc | 8.791 / 7.329 |
| MK2-12lake20.5m               | 0.344020 | 0.219863      | Image Token: RjRxb6kvRornisxSD3JcEnX1nJd | Image Token: Oy2qb9ijboHhXNx9tNHcn2Hxngb | 7.925 / 7.023 |
| MK2-12normalz0.8m             | 0.317058 | 0.357895      | Image Token: R8mfb4VDMoOlPWxhRsPcT82rnrh | Image Token: CihSbFWMLonsWSxruCUcvFOLnxe | 7.833 / 6.557 |
| ydiffcorrectedB1-138corrected | 0.322129 | 0.584125      | Image Token: P2YibsYzWoGpvex83xOcBEnhnwd | Image Token: LuiXbPWBPoZ3qOxBjaFcNrisnlb | 8.759 / 7.622 |
