# CLIP → VLM → LLaVA 系统学习教程

> **教学目标**：把 CLIP（OpenAI 2021）、VLM 全景图、LLaVA（Visual Instruction Tuning）这条主线打通；
> 关注 **「问题 → 设计思想 → 应用」**，不陷数学推导。
>
> **适合人群**：熟悉 CNN / Transformer / BERT / ViT，但对**对比学习**和**多模态对齐**不熟的研究者。
>
> 主线参考材料（来自个人 reading list `06-reading-list.md` §5）：
> - [OpenAI Blog — CLIP: Connecting Text and Images](https://openai.com/research/clip)
> - [Radford et al. — Learning Transferable Visual Models From Natural Language Supervision (CLIP)](https://arxiv.org/abs/2103.00020)
> - [Liu et al. — Visual Instruction Tuning (LLaVA)](https://arxiv.org/abs/2304.08485)
> - [LLaVA GitHub](https://github.com/haotian-liu/LLaVA)
>
> 对比学习预热补充材料：
> - [Lilian Weng — Contrastive Representation Learning](https://lilianweng.github.io/posts/2021-05-31-contrastive/)
> - [Chen et al. — SimCLR](https://arxiv.org/abs/2002.05709)
> - [van den Oord et al. — Representation Learning with Contrastive Predictive Coding (InfoNCE)](https://arxiv.org/abs/1807.03748)

---

## 如何阅读这份教程

- 全部 Markdown + LaTeX 数学公式。**推荐用以下工具打开**：
  - Typora（最推荐，所见即所得）
  - Obsidian
  - VS Code / Cursor 内置 Markdown 预览
- 公式语法：行内 `$...$`，独立 `$$...$$`。
- 每章末尾有 **"自检小问题"+ 参考答案**，建议做完再进入下一章。
- 推荐节奏：**每章一次坐下读完**，中间不打断；卡壳的句子直接贴出来问我。

---

## 学习路线（共 10 章）

| 章节 | 文件 | 内容简介 | 难度 |
|---|---|---|---|
| 第 0 章 | `00-课程总览与符号表.md` | 完整学习地图、符号表、阅读策略 | ⭐ |
| **第一阶段：对比学习预热（CLIP 的母体）** | | | |
| 第 1 章 | `01-从监督学习到对比学习.md` | 监督学习的天花板、自监督的两条死胡同、对比学习的祖师爷洞察 | ⭐⭐ |
| 第 2 章 | `02-对比学习损失函数演进.md` | Triplet → N-pair → InfoNCE 三步演进，InfoNCE 公式逐项拆解 | ⭐⭐⭐ |
| 第 3 章 | `03-SimCLR与三个工程细节.md` | SimCLR 完整管线，augmentation / projection head / large batch 三个反直觉细节 | ⭐⭐⭐ |
| **第二阶段：CLIP 精读** | | | |
| 第 4 章 | `04-CLIP核心思想与架构.md` | 封闭词表困境、双塔架构、对称 InfoNCE、N×N 矩阵图 | ⭐⭐⭐ |
| 第 5 章 | `05-CLIP训练数据与零样本应用.md` | 4 亿 WIT 数据集、prompt engineering、零样本分类的数学机制、应用与局限 | ⭐⭐⭐ |
| **第三阶段：从 CLIP 走向对话** | | | |
| 第 6 章 | `06-VLM三种范式全景.md` | 双编码器（CLIP）/ 编解码器（BLIP-2）/ LLM-based（LLaVA）三大范式对比 | ⭐⭐⭐ |
| **第四阶段：LLaVA 精读** | | | |
| 第 7 章 | `07-LLaVA架构与GPT-4造数据.md` | 极简架构、用纯文本 GPT-4 造视觉指令数据 | ⭐⭐⭐ |
| 第 8 章 | `08-LLaVA两阶段训练与演进.md` | 特征对齐 → 端到端指令微调；LLaVA-1.5 / NeXT 关键升级 | ⭐⭐⭐ |
| **第五阶段：贯通** | | | |
| 第 9 章 | `09-贯通CLIP到LLaVA设计哲学.md` | 三个跃迁、数据规模 vs 质量、未解决问题 | ⭐⭐ |

附：`术语小词典.md` —— 全教程关键术语速查。

---

## 学习节奏建议

- **第 1-3 章：对比学习预热**——CLIP 的母体，必须吃透，第 4 章一切才能水到渠成。
- **第 4-5 章：CLIP**——主线核心，建议**对照官方博客和论文 Figure 1/3** 一起看。
- **第 6 章：VLM 全景**——一节带过，建立分类学，不必每个模型精读。
- **第 7-8 章：LLaVA**——重点理解"GPT-4 造数据"的机巧，和"为什么投影器能这么简单"。
- **第 9 章：贯通**——把整条主线提炼成 3 句话，能讲给同事听就算过关。

---

## 关键符号表

> 完整符号见 `00-课程总览与符号表.md`。这里只列最高频的。

| 符号 | 含义 |
|---|---|
| $\mathbf{x}$ | 图像（image） |
| $\mathbf{t}$ | 文本（text，如 caption） |
| $f_I(\cdot)$ | 图像编码器（image encoder，如 ViT） |
| $f_T(\cdot)$ | 文本编码器（text encoder，如 Transformer） |
| $\mathbf{I}_i, \mathbf{T}_i$ | 第 $i$ 张图、第 $i$ 段文本的归一化嵌入向量 |
| $\text{sim}(\cdot, \cdot)$ | 相似度函数，通常是余弦相似度 |
| $\tau$ | temperature，softmax 锐度系数（CLIP 中是可学习的） |
| $\mathcal{L}_{\text{InfoNCE}}$ | 对比学习的核心损失 |
| $N$ | batch size（对比学习里 = 负样本数 + 1） |

---

## 反馈与定制

每章末尾留有 **"我的回答 / 我的疑问"** 留白，建议你边学边写。如果某节讲得不够清楚或太啰嗦，告诉我节号和具体段落，我会重写。

祝学习愉快。
