# 📘 第 8 课：范式 5 —— Latent-Space WM（不画像素，只在表征空间预测）

> 对应论文章节：**Sec 3.6 + Fig. 4(b) + Table 1 第五组**（第 14–15 页）
> 学习目标：理解 JEPA 路线在机器人领域的最新落地；看完后你能拿下整章 Sec 3 的 5 大范式。

---

## 0. 30 秒温习前 4 课

| 范式 | 核心思路 | 未来预测形式 |
|---|---|---|
| 第 4 课 IDM-Style | 两个独立模型，先想象再行动 | 显式像素视频 |
| 第 5 课 Single-Backbone | 一个 backbone 通吃 | 同一个去噪过程 |
| 第 6 课 MoE/MoT | 双专家 + 共享 attention | 视频专家分工 |
| 第 7 课 Unified VLA | VLA 内化 + auxiliary loss | future image as 辅助监督 |

注意：**前 4 课多多少少都涉及"未来图像/视频的生成"**——
- 第 4–6 课显式生成像素
- 第 7 课至少在训练时生成 future image

> 🎯 **今天的 Latent-Space WM 干的事最激进**：
> **彻底放弃"画出未来图像"，所有未来建模都搬到 representation space 里做。**

---

## 一、先搞清楚一件事：什么是 JEPA？

这节课和 **Yann LeCun 力推的 JEPA**（Joint Embedding Predictive Architecture）路线高度相关。
你不熟也没关系，30 秒讲清楚：

### JEPA 的核心信念

> 🎯 **预测下一帧"长什么样"是浪费——你应该预测下一帧的"语义表征"。**

举个例子：
- **生成式（pixel-level）**：你看到现在的画面，预测下一帧每个像素 RGB 值是多少
- **JEPA（representation-level）**：你看到现在的画面，预测下一帧在某个 encoder 输出的 **latent 向量**是多少

### 为什么 JEPA 这么坚持？

| 维度 | Pixel Prediction | JEPA |
|---|---|---|
| 预测目标 | 整张图（百万级像素） | 一个语义向量（千级维度） |
| 模型容量浪费 | 大量算力花在背景、光照 | 算力集中在语义 |
| 训练稳定性 | 像素 L2 / 感知 loss 难调 | embedding loss 更稳定 |
| 信噪比 | 低（10% 信息有用） | 高（90% 信息有用） |
| 可解释性 | 高（能看到画面） | 低（看不到，只有向量） |

> 💡 **类比**：你描述一个朋友，你不会一根根头发地描述他的样子，而会说"高个子、戴眼镜、爱笑"——
> 这种**抽象 + 紧凑**的描述，就是 JEPA 想要的预测目标。

代表作：I-JEPA（图像）、V-JEPA / V-JEPA 2（视频）。
**今天的范式正是把这种思想搬到机器人 policy learning 里。**

---

## 二、一句话定义这个范式

> 🎯 **Latent-Space WM = 把"未来预测"完全搬到 representation space 里做，不再走像素空间。**
> **预测目标不是图像，而是 future-aware embedding / latent target / compact control condition。**

论文第 14 页 Fig. 4(b) 长这样（我用文字画出来）：

```
                ┌──────────────────────────────────────┐
观察 ──▶│                                                  │
       │           MLLM backbone                          │
指令 ──▶│           (内部带 world modeling)                 │
       │                                                  │
       └──────────────────────────────────────────────────┘
                              │
                ┌─────────────┴─────────────┐
                ▼                           ▼
         World Representation          Action 输出
         (内部 latent，不解码)             (主任务)
              │
              └────► 影响 action 生成
                    （但永远不画出来）
```

注意三件事：
1. **没有 future image 输出**（和第 7 课的关键差异）
2. **World modeling 完全内化进 backbone 的 latent space**
3. **Action 生成被这个 latent 表征"指导"，但永远看不到具体未来画面**

---

## 三、和第 7 课 Unified VLA 的关键区别（最容易混的两节）

第 7 课的 Unified VLA 也号称"内化"，那它和今天有什么区别？

| 维度 | 第 7 课 Unified VLA | **第 8 课 Latent-Space WM（今天）** |
|---|---|---|
| 是否预测 future image | ✅ 预测（至少在训练时） | ❌ **完全不预测像素** |
| 预测目标 | future RGB / latent video | **抽象 representation / embedding** |
| 是否需要 video decoder | 是（哪怕只在训练时） | **否，永远不需要 decoder** |
| 受 JEPA 影响 | 弱 | **强**（直接借鉴 JEPA 思想） |
| 训练稳定性 | 中（像素 loss 难调） | **高**（embedding loss 更稳） |
| 推理速度 | 快（推理时关 future head） | **更快**（连 future head 都没有） |

> 🔑 **一句话区分**：
> - **第 7 课 Unified VLA**：训练时**画**未来图像当辅助监督
> - **第 8 课 Latent-Space WM**：连画都不画，只在 latent 空间里**模拟**未来

---

## 四、4 个代表作（按时间和激进程度排序）

论文 Sec 3.6 列了几个代表作，我按出现时间和"放弃像素的彻底程度"排序：

### ① FLARE（Zheng et al., 2025）— 早期奠基者

**全称**：**F**uture **L**atent **R**epresentation **A**lignment

**关键设计**：
- 让 action denoising network 的隐藏特征**对齐**未来观测的 latent embedding
- 不预测像素，只让 policy 的内部状态"暗暗地"包含未来信息

**直觉**：
> "Policy，你脑子里想动作的时候，给我顺手对齐一下未来 embedding。"

这是这一支的最简单实现——**不引入新的预测 head，只在 hidden state 上加约束**。

### ② VLA-JEPA（Sun et al., 2026）— 把 JEPA 思想完整搬过来

**关键设计**：
- 引入 JEPA 风格的预训练目标，专门为 VLA 设计
- 核心创新：**leakage-free state prediction**——future frame 只用来产生 latent target，**不让模型直接看到 future pixel**

**为什么巧妙**：
- 像素预测容易让模型"shortcut"（学到一些 spurious correlation）
- 强制 latent 预测，反而让模型学到 **action-relevant state transitions**

**直觉**：
> "我给你看现在和未来的图片，但你只能预测未来的 embedding，不能复制 pixel。"

### ③ JEPA-VLA（Miao et al., 2026）— 直接拿 V-JEPA 当 backbone

**关键设计**：
- 不在 VLA 内部加 latent prediction head
- 而是直接论证：**V-JEPA 2 学到的 embedding 比静态视觉表征更好**
- 然后用 V-JEPA 2 的 embedding 当 VLA 的 backbone

**直觉**：
> "我不教 VLA 怎么预测未来——我直接给它换一个'已经会预测未来'的眼睛。"

这种**"用预训练的 JEPA 模型做 backbone"**的思路，是把整个表征学习和 VLA 训练**完全解耦**——
和 Unified VLA 的"端到端联合训练"形成鲜明对比。

### ④ WoG / DIAL — 把 latent WM 移到"条件空间"

**WoG**（Worlds of Generation, Su et al., 2026）：

**关键设计**：
- 不预测 future image / future latent
- 而是预测 **compact future-oriented conditions** —— 直接和 action 一起被生成
- 这些 conditions 是"对未来动作最有用的部分"

**DIAL**（Chen et al., 2026c）：

**关键设计**：
- 把 high-level intent 和 low-level action **解耦**
- 用 latent visual foresight 当作两者之间的 **structured bottleneck**
- 这个 bottleneck 在 VLM feature space 里，永远不解码到像素

> 💡 **这两个工作代表了最激进的方向**：
> 不仅放弃像素，连"预测一个完整的未来"都放弃——
> 只预测**对决策最有用的那一部分未来**，**最大化信噪比**。

---

## 五、一条补充支线：Symbolic World Model（论文 Sec 3.6 末尾）

论文在这一节最后还提了一个**完全不同的方向**——**符号世界模型**：

| 方法 | 预测什么 |
|---|---|
| Silver et al. 2021 | Predicates（谓词）、object relations |
| Shah et al. 2025 | Affordances（可供性） |
| Liang et al. 2025c, 2026 | Operators（操作子）、causal processes |
| Athalye et al. 2026 | 用 pretrained VLMs 学 symbolic world model |

**核心思路**：
> 🎯 **不是预测 latent embedding，而是预测离散的、结构化的符号变量。**
> 比如"杯子在桌上"、"夹爪打开"、"红色方块在盘子里"。

**为什么这是个独立支线**：
- 上面 4 个工作都是"神经 latent prediction"
- 这一支是"符号 prediction"——更接近经典 AI / planning 领域
- 优点：长时序推理特别稳定、可解释性极强、容易做 task-and-motion planning
- 缺点：需要"感知 → 符号"的对齐，复杂任务容易难以预定义符号系统

> 💡 这一支会在第 12 课（开放挑战）里再次出现，作为"符号结构整合"的未来方向之一。

---

## 六、用第 3 课的"切片视角"回看

第 3 课的联合分布：

$$
p\bigl(o_{t+1:t+k},\; a_{t+1:t+k} \;\big|\; o_t,\; l\bigr)
$$

### Latent-Space WM 怎么处理这个分布

它做了一个**关键变换**——把"未来观测 $o$" 替换成"未来 latent $z$"：

$$
p\bigl(z_{t+1:t+k},\; a_{t+1:t+k} \;\big|\; o_t,\; l\bigr)
$$

其中 $z = E(o)$，$E$ 是某个 encoder（可以是 V-JEPA、CLIP visual encoder、DINO 等）。

然后建模这个**新的联合分布**，但**永远不需要把 $z$ 解码回像素**。

> 🎯 **这种范式的本质 = 把"未来的预测对象"从高维像素压缩到低维 embedding。**
> 数学结构和 Unified VLA 一样，**但预测目标的空间完全变了**。

---

## 七、Table 1 第五组的横向对比（论文第 8 页）

| 方法 | 推理时的未来生成 | Backbone | 耦合方式 |
|---|---|---|---|
| **FLARE** | Latent alignment | MLLM | Latent internalization |
| **VLA-JEPA** | Latent target prediction | MLLM | Latent internalization |
| **JEPA-VLA** | Predictive embeddings | MLLM | Latent internalization |
| **WoG** | Future condition only | MLLM | Latent internalization |
| **DIAL** | Latent visual foresight | MLLM | Latent internalization |

> 📌 **共同点**：全部 backbone 是 MLLM，全部"latent 内化"
> **差异点**：latent 的"角色"——alignment / target / backbone / condition / bottleneck

---

## 八、Latent-Space WM 的优缺点

### ✅ 优点

1. **训练最稳定**：embedding loss 比像素 loss 好调得多
2. **推理最快**：完全没有视频生成步骤
3. **信噪比最高**：所有算力都花在"对决策有用的信息"上
4. **避开"视觉合理 ≠ 物理合理"问题**：第 4 课的核心痛点之一
5. **理论基础强**：和 JEPA 的成熟研究路线对接

### ❌ 缺点

1. **可解释性最差**：你看不到机器人脑子里"想象"了什么——只有一堆 embedding
2. **不适合 imagination-driven planning**：没法把 latent 解码出来给人类看，也很难做 visual rollout 比较
3. **对 encoder 质量敏感**：encoder 不好，latent 就垃圾，policy 就废
4. **Benchmark 上的优势不显著**：因为放弃了 video pretraining 的物理先验，在长时序 / 复杂任务上**未必比 video-based 范式强**

> 🔑 **何时该用**：
> - 你在乎**部署速度**和**训练稳定性** → 选 Latent-Space
> - 你在乎**可解释性**或要做**imagination planning** → 选前 3 课的范式

---

## 九、🎉 Sec 3 全景终结图：5 大范式终极对比

这是过去 5 节课（第 4–8 课）的终极总结。建议你打印一张贴墙上：

```
═══════════════════════════════════════════════════════════════════
              5 种范式按"预测什么 + 怎么预测"分类
═══════════════════════════════════════════════════════════════════

预测形式            范式               Backbone   推理时跑 WM 吗
─────────────────────────────────────────────────────────────
显式像素视频     →  IDM-Style          VGM        ✅ 必须
                   (第 4 课)
                                                
联合视频+动作   →  Single-Backbone    VGM        看选择
                   (第 5 课)                    
                                                  
专家分工 + 视频  →  MoE/MoT            VGM        看选择
                   (第 6 课)                    
                                                
未来图像辅助    →  Unified VLA        MLLM       ❌ 通常不
                   (第 7 课)                    
                                                
仅 latent 表征  →  Latent-Space WM    MLLM       ❌ 永远不
                   (第 8 课)                    
─────────────────────────────────────────────────────────────
完全外挂                                                完全内化
                                                       
"用一段话总结整个 Sec 3"：                              
WM 与 Policy 的耦合可以从"两个独立模型流水线"，         
经过"参数共享 + 联合训练"，                              
一直走到"完全放弃像素，只在表征空间预测"。              
每一步都解决了上一步的一个痛点，                        
但同时也牺牲了一些上一步的优点。                        
没有"最好"的范式，只有"最合适当前任务"的范式。           
═══════════════════════════════════════════════════════════════════
```

---

## 十、一句话总结今天

> 🎓 **Latent-Space WM = 把"未来"从像素空间压缩到表征空间。
> 它的本质是把 JEPA 思想搬到机器人 policy 里——预测 future embedding 而非 future image。
> 优点是训练稳定、推理快、信噪比高；缺点是不可解释、不适合做 imagination planning。
> 它代表了"WM 内化"的最极致形式，也是和 Yann LeCun 大方向最接近的机器人路线。**

---

## 十一、Sec 3 总结：你已经掌握了整个领域最难的一章

恭喜你！如果你认真看完了第 4–8 课，你现在已经掌握了：

- ✅ 5 种主流的 WM-Policy 耦合范式
- ✅ 它们的数学本质（联合分布的不同切法）
- ✅ 它们的工程权衡（训练成本、推理速度、可解释性）
- ✅ 它们的代表作（每种 3–5 个）
- ✅ 它们的演进逻辑（每个范式都在解上一个范式的痛点）

> 🔑 **如果你能用 5 分钟向同事讲清楚 5 种范式的差异，你的 Sec 3 就算彻底通关了。**

---

## ✅ 课后检查（这次答对 Q1 就可以毕业 Sec 3 了）

### Q1（必答 · 终极对比题）⭐⭐⭐
请你**用一段话**（不超过 200 字）把 5 种范式的本质差异讲清楚。
（提示：用"backbone 类型 + 预测形式 + 推理时是否生成 future"三个维度）

### Q2（必答 · 选型挑战题）
现在你是 Cursor 公司的机器人项目 lead，下面是几个真实场景，给每个场景挑一种最合适的范式：

- **(a)** 你要做一个 demo：让机器人在脑内预演 5 种抓取策略，挑成功率最高的执行（强可视化）
- **(b)** 你部署在边缘设备，每秒决策频率必须 ≥ 100Hz（极致推理速度）
- **(c)** 你做研究项目，想"不用视频生成模型"也能拿到 future prediction 的好处
- **(d)** 你团队已经有一个基于 V-JEPA 2 的视觉 backbone，想在它之上做机器人 policy
- **(e)** 你拿到 200 万段未标注的人类操作视频，想最大化利用它们

### Q3（选答 · 思辨题）
论文 Sec 3.6 提到 **JEPA-VLA** 的设计很有趣：**直接把 V-JEPA 2 的 embedding 当作 VLA 的 backbone**。
这种"模块替换"的思路，本质是把 **表征学习** 和 **下游任务** 完全解耦。
你觉得这种思路有没有可能扩展到——
**直接用大型语言模型的 hidden state 做 robot policy backbone**？为什么？

---

## 📝 我的回答（你来填）

> Q1:
>
> Q2:
> - (a)
> - (b)
> - (c)
> - (d)
> - (e)
>
> Q3:

## 🤔 我的疑问（你来填）

> -
> -

---

**下一课预告**：
**第 9 课 — World Model as Simulator（替代真机 RL 与 Policy 评测）**

下节课我们离开 Sec 3，进入论文的 **Sec 4**——一个**完全不同的 WM 用法**：
**WM 不是用来做 policy 的一部分，而是当做"虚拟环境"，让 policy 在里面做强化学习和评测。**

代表作：World-Env、VLA-RFT、WMPO、Ctrl-World、WorldEval、WoVR。
看完后你会理解：**为什么"WM 是一个低成本的真机替代品"是这个领域最有商业价值的方向之一。**

> 💡 这是从"WM 是 policy 的一部分"到"WM 是 policy 的环境"的视角转换——
> 同样的 WM，扮演完全不同的角色。
