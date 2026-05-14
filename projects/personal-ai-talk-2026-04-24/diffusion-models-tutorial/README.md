# 扩散模型 (Diffusion Models) 系统学习教程

> 本教程基于 Lilian Weng 的博客 [What are Diffusion Models?](https://lilianweng.github.io/posts/2021-07-11-diffusion-models/)
>
> 面向对概率论和扩散模型背景**不太熟悉**的读者，采用**深入浅出、逐步推导**的方式编写。

---

## 如何阅读这份教程

- 本教程使用 Markdown + LaTeX 数学公式编写。**推荐用以下工具打开**，公式才能正确渲染：
  - Typora（最推荐，所见即所得）
  - Obsidian
  - VS Code + Markdown Preview Enhanced 插件
  - 直接在 GitHub / GitLab 网页中查看
- 公式语法：行内公式用 `$...$`，独立公式用 `$$...$$`。
- 每一节末尾会有 **"自检小问题"**，建议你做完再进入下一节。

---

## 学习路线（10 章）


| 章节    | 文件                      | 内容简介                                             | 难度   |
| ----- | ----------------------- | ------------------------------------------------ | ---- |
| 第 0 章 | `00-直觉理解.md`            | 用比喻建立扩散模型的直觉                                     | ⭐    |
| 第 1 章 | `01-预备知识.md`            | 高斯分布、条件概率、贝叶斯、马尔可夫链、KL 散度、重参数化                   | ⭐⭐   |
| 第 2 章 | `02-前向扩散过程.md`          | 一步步加噪声的数学推导（含 nice property）                     | ⭐⭐   |
| 第 3 章 | `03-反向扩散过程.md`          | 反向条件分布的推导（贝叶斯展开 + 配方法）                           | ⭐⭐⭐  |
| 第 4 章 | `04-训练目标-VLB推导.md`      | 变分下界（VLB / ELBO）的完整推导                            | ⭐⭐⭐⭐ |
| 第 5 章 | `05-DDPM简化损失与算法.md`     | 从 VLB 到一行代码：DDPM 的训练 / 采样算法                      | ⭐⭐⭐  |
| 第 6 章 | `06-Score-based模型联系.md` | NCSN、Langevin dynamics、score 与 noise 的关系         | ⭐⭐⭐  |
| 第 7 章 | `07-条件生成.md`            | Classifier Guidance & Classifier-Free Guidance   | ⭐⭐⭐  |
| 第 8 章 | `08-加速采样.md`            | DDIM、Progressive Distillation、Consistency Models | ⭐⭐⭐  |
| 第 9 章 | `09-高分辨率与架构.md`         | LDM、Cascaded、unCLIP、Imagen、U-Net、DiT、ControlNet  | ⭐⭐   |


---

## 学习节奏建议

- **第 0~2 章**：直觉 + 预备知识 + 前向过程，是基础，必须完全搞懂再往下走。
- **第 3~5 章**：扩散模型最核心、最难、也最精彩的部分，建议跟着推导**自己手写一遍**。
- **第 6 章**：进阶视角，理解 score-based 模型与 DDPM 的等价性。
- **第 7~9 章**：应用与扩展，按需阅读即可。

---

## 关键符号表


| 符号                                              | 含义                                                                    |
| ----------------------------------------------- | --------------------------------------------------------------------- |
| $\mathbf{x}_0$                                  | 原始数据（如真实图像）                                                           |
| $\mathbf{x}_t$                                  | 第 $t$ 步加噪后的数据，$t \in 1, \dots, T$                                     |
| $\mathbf{x}_T$                                  | 最终的纯噪声（接近标准高斯）                                                        |
| $\beta_t$                                       | 第 $t$ 步加噪的方差，预先设定                                                     |
| $\alpha_t = 1 - \beta_t$                        | 信号保留比例                                                                |
| $\bar{\alpha}*t = \prod*{i=1}^t \alpha_i$       | 累积信号保留比例                                                              |
| $q$                                             | 前向过程的真实分布（不需要学习）                                                      |
| $p_\theta$                                      | 反向过程的近似分布（神经网络，参数 $\theta$）                                           |
| $\boldsymbol{\epsilon}$                         | 高斯噪声，$\boldsymbol{\epsilon} \sim \mathcal{N}(\mathbf{0}, \mathbf{I})$ |
| $\boldsymbol{\epsilon}_\theta(\mathbf{x}_t, t)$ | 神经网络预测的噪声                                                             |


---

祝你学习愉快！🚀