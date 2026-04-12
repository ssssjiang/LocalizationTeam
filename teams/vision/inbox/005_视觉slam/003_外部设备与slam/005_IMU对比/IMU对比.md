# IMU对比

# 1. gyro性能



| 指标                                                                                      | BMI088（割草机）                        | BMI323（扫地机）                        | IIM-42652（激光割草机AiryLite,库玛甄选）                                 |
| --------------------------------------------------------------------------------------- | ---------------------------------- | ---------------------------------- | ------------------------------------------------------------- |
| ADC分辨率                                                                                  | 16 bit                             | 16 bit                             | 16 bit（FIFO支持20-bit格式）                                        |
| 量程 (°/s)                                                                                | ±125 / ±250 / ±500 / ±1000 / ±2000 | ±125 / ±250 / ±500 / ±1000 / ±2000 | ±15.625 / ±31.25 / ±62.5 / ±125 / ±250 / ±500 / ±1000 / ±2000 |
| 灵敏度初始误差Sensitivity tolerenceSensitivity errorSensitivity Scale Factor Initial Tolerance | ±1 %                               | ±0.7 %（自校准后）/ ±3 %（无自校准）           | ±0.5 %                                                        |
| 灵敏度温漂 TCS                                                                               | ±0.03 %/K                          | ±0.02 %/K                          | ±0.005 %/°C                                                   |
| 非线性（FS表示满量程范围，这个百分比也是以满量程为参考）                                                           | ±0.05 %FS（FS1000/2000）             | 0.15 %（best fit, FS=2000）          | ±0.1 %                                                        |
| 交叉轴灵敏度（a轴数据对b、c轴的影响）                                                                    | ±1%                                | ±0.3%                              | ±1.25 %                                                       |
| 零偏（ZRO）Initial ZRO Tolerance Zero rate offset                                           | ±1 °/s（typ）                        | ±1 °/s（typ, over life）             | ±0.5 °/s（25°C, board-level）                                   |
| 零偏温漂（ZRO vs T）                                                                          | ±0.015 °/s/K                       | ±0.04 °/s/K                        | ±0.02 °/s/°C                                                  |
| 噪声密度Rate Noise Spectral DensityNoise densityOutput noise                                | 0.014 °/s/√Hz                      | 0.007 °/s/√Hz（HP mode）             | 0.0038 °/s/√Hz（@10Hz）                                         |
| 总RMS噪声                                                                                  | 0.1 °/s-rms（BW=47Hz）               | —                                  | 0.038 °/s-rms（BW=100Hz）                                       |
| ODR范围Output Data RateData rate                                                          | 100\~2000Hz                        | 12.5 \~ 6400 Hz                    | 12.5 \~ 32000 Hz                                              |



# 2. Acc性能



| 指标                                                                  | BMI088 Acc                            | BMI323 Acc                                                               | IIM-42652 Acc                              |
| ------------------------------------------------------------------- | ------------------------------------- | ------------------------------------------------------------------------ | ------------------------------------------ |
| ADC分辨率                                                              | 16 bit                                | 16 bit                                                                   | 16 bit                                     |
| 量程 (g)                                                              | ±3 / ±6 / ±12 / ±24                   | ±2 / ±4 / ±8 / ±16                                                       | ±2 / ±4 / ±8 / ±16                         |
| 灵敏度初始误差Sensitivity Scale Factor Initial Tolerance Sensitivity error | —                                     | ±0.5 %（soldered, over life 焊板后 + 全寿命）                                    | ±0.5 %（component-level器件级初始值）              |
| 灵敏度温漂 TCS                                                           | 0.002 %/K                             | ±0.005 %/K                                                               | ±0.005 %/°C                                |
| 非线性                                                                 | 0.5 %FS(±3g)                          | 0.1 %FS（best fit, ±2g）                                                   | ±0.1 %（best fit, ±2g）                      |
| 交叉轴灵敏度                                                              | 0.5 %                                 | ±0.3 %(Non-orthogonality比例耦合项)&#xA;±0.5 度(Alignment error，IMU和封装参考边对齐角度) | ±1 %                                       |
| 零g偏置（Zero-g offset）ZERO-G OUTPUT Initial Tolerance                  | 20 mg（typ, 25°C, FS±6g）               | ±35 mg（soldered焊板后）；&#xA;±50 mg（soldered,over life焊板后+全寿命）               | ±20 mg（board-level, all axes）              |
| 零g温漂（Zero-g vs T）                                                   | <0.2 mg/K                             | ±0.3 mg/K                                                                | ±0.15 mg/°C                                |
| 噪声密度Noise densityPower Spectral Density                             | 160 µg/√Hz (X/Y), &#xA;190 µg/√Hz (Z) | 180 µg/√Hz（HP, ±8g）                                                      | 70 µg/√Hz（@10Hz）                           |
| RMS噪声                                                               | —                                     | —                                                                        | 0.70 mg-rms（BW=100Hz）                      |
| ODR范围                                                               | 12.5 \~ 1600 Hz                       | 12.5 \~ 6400 Hz                                                          | 1.5625 \~ 32000 Hz                         |
| 带宽/LPF响应                                                            | 3dB: 5\~280Hz（Z:245Hz）                | 3dB: 6.2\~1677 Hz（随ODR）                                                  | 9.6\~500Hz（ODR<1k）；&#xA;42\~3979Hz（ODR≥1k） |
| PCB应变致零偏                                                            | —                                     | ±0.016 mg/µstrain                                                        | —                                          |

