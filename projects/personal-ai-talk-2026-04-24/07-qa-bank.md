# 追问 Q&A 储备

> **使用方式**：
>
> - 周一到周四读完每个节点的材料后，对照这里的 Q&A **自我盘问**
> - 每个 Q 强迫自己用 30 秒口头回答一遍——能答得清楚 = 节点吃透
> - 答得不清楚的 → 回去再读一遍材料 → 在这份文件下面写下你**自己的答案版本**（不要原文抄）
> - 这份文件是"现场最大的安全网"——周五现场被追问，你脑子里有的就是这些答案
>
> **每个节点 4 个高频追问**（按"是什么 / 为什么 / 局限 / 与其他的关系"4 个维度组织）

---

# 节点 1：RNN / CNN

### Q1: CNN 为什么比手工特征（SIFT/HOG）好？

**A**: 手工特征的本质是工程师**先验定义**"什么是好特征"——SIFT 用梯度方向、HOG 用边缘直方图。这要求工程师对每类任务都有深刻理解，而且这种理解很难泛化（人脸的好特征不一定是车的好特征）。CNN 的本质是**让数据告诉模型什么是好特征**——卷积核的参数全部从数据里学，深层卷积自动学出"layer 1 边缘 → layer 2 纹理 → layer 3 部件 → layer 4 物体"这种层次化表示。在数据足够多的时候（ImageNet 130 万张），数据驱动的特征比人脑设计的更精确、更全面、更泛化。

### Q2: RNN 为什么会梯度消失？LSTM 怎么解决？

**A**: RNN 在反向传播时，梯度需要通过**时间步逐层传递**——每经过一步要乘一个 Jacobian 矩阵。如果矩阵的特征值小于 1，梯度会**指数级衰减**；大于 1，会**指数级爆炸**。LSTM 通过引入"门控机制"（input gate / forget gate / output gate）和"cell state"——cell state 在时间维度上的传递是**加法而不是乘法**，所以梯度可以更稳定地流过去。但 LSTM 只是缓解，没有根本解决——超长序列（>500 步）LSTM 也吃不消。

### Q3: 既然 Transformer 都把 RNN/CNN 替代了，为什么还要讲它们？

**A**: 两个原因。一是**历史角度**——CNN/RNN 是端到端深度学习能 work 的第一批证明，没有它们就没有后面所有事。二是**实用角度**——CNN 在小数据 + 边缘设备 + 实时性场景（如 TinyML、车载嵌入式）仍然不可替代；RNN/LSTM 在某些时序场景（如金融时序、IoT 传感器）也仍在用。Transformer 没有完全杀死它们，只是在大数据 + 大模型场景下取代了它们。

### Q4: AlexNet 是 2012 年，但深度学习 2006 年 Hinton 就在做 deep belief network 了，为什么要等到 2012 年才爆发？

**A**: 三件事在 2012 年同时到位：① **GPU 算力**——AlexNet 用了 2 块 GTX 580，是当时极少数能跑得动的；② **大规模数据集**——ImageNet 2009 年发布、130 万张图片，是当时最大的；③ **关键工程优化**——ReLU 激活、Dropout 正则、数据增强这些技巧组合起来。**算法 + 数据 + 算力，三者缺一不可**。Hinton 2006 年做的 deep belief network 缺数据和算力，所以没爆发。

---

# 节点 2：ResNet

### Q1: 网络做深为什么会"退化"？这不是过拟合吗？

**A**: 不是。过拟合是训练误差低、测试误差高。**退化是训练误差和测试误差都升高**。本质是**优化层面的问题**——深层网络的损失函数 landscape 太崎岖，SGD 很难找到一个好的局部最小值。ResNet 的残差连接让网络拥有一个**保底退路**：最差情况下中间几层学到恒等映射（让 F(x) ≈ 0），整体网络至少不会比浅层网络差。这给了优化器一个"安全的初始解"，从这个解出发再逐步学到更优。

### Q2: 残差连接 y = F(x) + x，为什么 + x 而不是其他形式？

**A**: identity mapping（恒等映射）有几个独特性质：① 反向传播时梯度可以**直接通过 + 这个分支无衰减地传到前面层**——所以再深的网络梯度也能传回去；② 前向传播时信息保留——浅层信息可以直接传到深层不丢失；③ 数学上是最优雅的——0 参数、0 计算开销。何恺明在 ResNet v2 论文里专门讨论了为什么 identity 是最佳选择——尝试过其他形式（gating、1x1 conv）效果都不如 identity。

### Q3: 残差连接除了 ResNet 还在哪里用？

**A**: **几乎所有现代深度学习架构都用**。Transformer 里的 "Add & Norm" 那个 "Add" 就是残差。Diffusion 模型的 U-Net 也大量用残差。VLM、LLM 内部的 Transformer block 全部用残差。你打开任何一篇 2017 年之后的深度学习论文，**找不到不用残差的**。所以我说残差连接是"跨架构的底层基础设施"——它的影响远超 CNN 本身。

### Q4: 现在还有人做 ResNet 吗？还是被 ViT 替代了？

**A**: 在大数据、大模型场景下 ViT（Vision Transformer）已经替代了 ResNet。但在**边缘设备、小数据、实时性要求高**的场景，ResNet 系列（ResNet-18/50）仍然是主流——结构简单、参数少、部署容易、推理快。**两条线在共存**：ViT 在云端 + 大模型，ResNet 在边端 + 实时。

---

# 节点 3：Transformer

### Q1: Self-attention 的 Q/K/V 物理意义是什么？

**A**: **Q (Query) = "我在找什么"，K (Key) = "我提供什么"，V (Value) = "我携带什么内容"**。具体过程：每个位置生成自己的 Q、K、V 三个向量。计算 Q 和所有位置的 K 的点积——**点积大 = 相关性高**。然后 softmax 归一化得到注意力权重，用这个权重加权求和所有位置的 V，得到当前位置的输出。**类比**：你在图书馆找资料——Q 是你的需求关键词，K 是每本书的标签，V 是每本书的内容。系统先匹配 Q 和 K 找到相关的书，再按相关度加权汇总书的内容。

### Q2: 为什么需要 multi-head attention？一个 head 不够吗？

**A**: 一个 head 只能捕捉一种关系。**多 head 让模型并行学习多种不同的关系**——比如有的 head 关注语法依赖（主谓宾）、有的关注语义相似（同义词）、有的关注位置关系（前后文）。论文里典型用 8 个 head。每个 head 输出维度变小（hidden_dim / 8），最后拼起来——**计算量不变，但表达能力大幅增加**。后续研究（如 BERT 的 attention 可视化）确实发现不同 head 学到了不同的语言学模式。

### Q3: Transformer 没有循环，怎么处理位置信息？

**A**: 通过 **positional encoding** 把位置信息加到输入里。原论文用 sin/cos 函数生成固定的位置编码，加到 token embedding 上。后来的工作发展出 **learnable positional embedding**（BERT）、**RoPE 旋转位置编码**（LLaMA、GPT-NeoX）、**ALiBi**（线性偏置）等多种变体。RoPE 是目前 LLM 主流——它能自然外推到训练时没见过的长度。

### Q4: 既然 attention 这么好，它的 limitation 是什么？

**A**: 三个主要问题：① **计算复杂度 O(n²)**——序列长度翻倍，计算量四倍。这就是为什么早期 Transformer 上下文长度只有 512，2000 年代后期才靠各种 efficient attention（FlashAttention、稀疏 attention、滑动窗口）扩展到 128k、1M。② **位置编码是后接的，不像 CNN/RNN 天然有归纳偏置**——所以 Transformer 在小数据上不如 CNN，必须靠大数据 + 预训练。③ **memory bandwidth bound**——attention 的 KV cache 是显存大头，端侧部署 Transformer 真正的瓶颈是 memory，不是 compute。

---

# 节点 4：LLM

### Q1: Scaling Law 的精确陈述是什么？

**A**: Kaplan 2020 年的论文给了精确公式：**Loss ≈ A · N^(-α) + B · D^(-β) + C · C^(-γ)**，其中 N 是参数量、D 是 token 数、C 是 compute。三者之间有最优配比——给定 compute 预算，应该用多大模型 + 多少数据。Kaplan 原始结论是"模型应该比当时常见的大很多"。后来 DeepMind 2022 年的 Chinchilla 论文修正了这个——**Kaplan 低估了 data 的重要性**，最优配比应该是 N 和 D 大致同等扩展（Chinchilla 用 70B 参数 + 1.4T token，效果超过 Gopher 280B + 300B token）。

### Q2: "涌现能力"到底是真的还是假的？

**A**: **学术界有争议**。Wei 2022 年那篇论文定义涌现是"小模型上完全不存在、大模型上突然出现"的能力——他举了多步算术、in-context learning 等例子。但 Stanford 2023 年那篇 "Are Emergent Abilities of LLMs a Mirage?" 反驳——所谓"涌现"是因为评测指标用了 hard accuracy（要么对要么错），如果换成 soft metric（部分正确给分），曲线就是连续的，不存在跃迁。**目前的共识是**：① 在某些具体任务上确实有"看起来不连续"的能力跃迁；② 但是否真的是"质变"还是评测人为造成的"假象"，没有定论；③ **涌现这个词被滥用了**——很多所谓涌现其实只是 scaling 带来的连续提升。

### Q3: LLM 为什么需要 RLHF？预训练不够吗？

**A**: 预训练让模型**学会预测下一个 token**——它知道什么是"流畅的英文"，但不知道"什么是用户想要的回答"。直接用预训练模型聊天，它会产生：① 拒绝回答 / 有害内容；② 回答冗长无关；③ 不遵循指令。RLHF 三步：① **SFT（监督微调）**——用人写的对话样例 fine-tune；② **训练 reward model**——人对模型多个回答打分，训练一个 reward model 学这个偏好；③ **PPO 强化学习**——用 reward model 作为信号，让 LLM 优化生成"人类喜欢"的回答。**RLHF 不是让模型变聪明，是让模型变"听话"**——智能上限由预训练决定。

### Q4: LLM 在做什么？真的"理解"语言吗？

**A**: 这是个哲学问题，但工程上可以有清晰回答。LLM 在做一件事——**学习海量文本里的统计规律，预测下一个 token 的概率分布**。它不"理解"语义（在人类的意义上），但它学到的统计规律足够丰富，可以**模拟出"理解"的行为**——回答问题、写代码、做推理。**这是不是"真理解"是争议焦点**——LeCun 等人坚持 LLM 永远不可能到 AGI，因为它没有 grounding（对物理世界的体验）；OpenAI/Anthropic 等人认为只要 scaling 足够 + 加上具身（VLA）/ 多模态，可以无限接近"理解"。**今天没有定论**。

---

# 节点 5：Diffusion

### Q1: Diffusion 为什么训练稳定，比 GAN 强？

**A**: GAN 的训练是**对抗博弈**——生成器和判别器互相博弈达到 Nash 均衡。这个博弈很容易卡住：① **mode collapse**——生成器只学会生成几种最容易骗过判别器的样本，丢掉多样性；② **训练发散**——一方学得快、一方跟不上，发散。Diffusion 的训练是**单一目标的回归问题**——预测每一步加的噪声。这是个**有标准答案的监督学习问题**，没有博弈，所以稳定。代价是**采样慢**（要迭代 N 步），但近期 diffusion 加速（DDIM、consistency model）已经把步数从 1000 降到 4-8 步。

### Q2: Latent Diffusion (Stable Diffusion) 和原版 Diffusion 的区别？

**A**: **原版 Diffusion 在像素空间做扩散**——一张 512x512 RGB 图是 78 万维向量，扩散过程极其耗算力。Latent Diffusion 的关键洞察——**先用一个 VAE 把图像压缩到 latent space**（比如 64x64x4 = 16k 维），在 latent space 里做扩散，最后再用 VAE decoder 还原成像素。这样训练和采样的算力降低 10-100 倍，让普通人在消费级 GPU 上也能跑。**SD 能开源 + 普及，latent space 这一招是关键**。

### Q3: Diffusion 怎么实现"用文字生成图像"的可控生成？

**A**: 通过 **classifier-free guidance + cross-attention**。具体做法：① 训练时把文本通过 CLIP encoder 编码成 embedding；② 在 U-Net 的多个层里加 cross-attention，让图像的每个位置都能 "看到" 文本 embedding；③ 训练时随机丢弃文本 condition（10-20% 概率）让模型同时学有文本和无文本的生成；④ 推理时用 classifier-free guidance —— `epsilon = epsilon_uncond + w · (epsilon_cond - epsilon_uncond)`，w 是 guidance scale，调大 = 更贴文本但多样性下降。

### Q4: Diffusion 的 limitation 是什么？

**A**: ① **采样慢**——即使加速到 4-8 步，仍然比 GAN 单 forward 慢得多。实时视频生成是大挑战。② **难以精确控制**——生成"3 个红苹果在一个蓝盘子里"这种带具体属性 + 数量 + 关系的图像，diffusion 经常出错。这反映 text-to-image 的对齐还是粗粒度的。③ **训练数据偏见**——LAION-5B 这种网络爬取的数据集有大量偏见、暴力、版权问题，diffusion 模型继承这些。④ **物理一致性差**——生成的图像在物理细节（手指数量、镜面反射、阴影方向）上经常出错，因为 diffusion 没有"世界模型"。

---

# 节点 6：VLM

### Q1: CLIP 的 contrastive learning 具体怎么训练？

**A**: 输入是 N 对 (image, text) batch，比如 N = 32k。对每个 image 用 image encoder 编码成向量 I_i，对每个 text 用 text encoder 编码成向量 T_j。计算 N×N 的相似度矩阵（cosine similarity）。**训练目标：让对角线（正确匹配的对）的 similarity 高，让非对角线（错误匹配）的 similarity 低**——本质上是 N-way classification（每个 image 在 N 个 text 里选对）。loss 是双向的——image 找 text + text 找 image，对称设计。OpenAI 用 4 亿对图文，训练 12 天 256 个 V100。

### Q2: VLM 和"多模态大模型"是同一个东西吗？

**A**: **不是**。VLM 是多模态大模型的一个子类——只处理 vision + language 两个模态。多模态大模型（MLLM）是更广的概念，可以涵盖 vision + language + audio + video + 3D + ... 多个模态。比如 Google Gemini 是"原生多模态"，从训练就同时处理多种模态；GPT-4V 严格说就是 VLM（视觉 + 语言）。**严谨用词**：VLM ⊂ MLLM。

### Q3: 现代 VLM（如 LLaVA、Qwen-VL）和 CLIP 的区别？

**A**: CLIP 只做"对齐"——把图像和文本嵌入到同一空间，不能生成。现代 VLM 是 **CLIP-style vision encoder + LLM**——视觉编码器（往往用 CLIP）把图像变成视觉 token，再喂给 LLM 做下游生成。所以现代 VLM 能"看图说话、看图问答、看图推理"。**架构上**：vision encoder（提特征）→ projector（对齐到 LLM 的 token 空间）→ LLM（生成）。

### Q4: VLM 现在的瓶颈在哪？

**A**: ① **细粒度感知差**——VLM 数清楚图里有几个人、识别小字、判断精确空间关系（"杯子在书的左边还是右边"）经常出错。② **视觉推理 vs 语言推理的不平衡**——VLM 经常"用语言知识猜"而不是"看图回答"，比如问"这张医学影像里是什么病"它可能根据图周围的文字描述猜，而不是真的看影像。③ **训练数据规模**——视觉数据比文本数据少几个数量级，VLM 的视觉部分还远没到 LLM 那种 scaling 程度。

---

# 节点 7：World Models 起源

### Q1: David Ha 2018 那篇 World Models 的核心架构？

**A**: 三件套 V + M + C：① **V (Vision)** = VAE，把环境观察（一帧游戏画面）压缩成低维 latent z；② **M (Memory)** = MDN-RNN（混合密度网络 + RNN），输入当前 z 和动作 a，预测下一个 z 的分布；③ **C (Controller)** = 一个非常简单的线性层（约 1000 参数），输入 z 和 RNN 隐状态，输出动作 a。**关键设计**：C 在 latent space 里训练，不接触原始像素。可以完全在"梦里"（V + M 模拟出来的环境里）训练 C，然后部署到真实环境。

### Q2: 为什么 World Models 这个方向 2018 提出后停滞了 6 年？

**A**: 三个原因：① **VAE 编码精度差**——latent space 信息损失大，复杂场景压缩后失真；② **RNN 预测能力有限**——MDN-RNN 对长程预测（>50 步）不准，agent 在"梦里"训练但在真实环境失效；③ **缺乏大规模数据 + 算力**——2018 年的 GPU 跑不动大规模 world model 训练。这些问题 2024 年之后才被解决——**Diffusion 替代 VAE 做编码、Transformer 替代 RNN 做预测、LLM 时代的算力规模到位**。这就是为什么 Genie 3、Cosmos 现在才出现。

### Q3: LeCun 的 JEPA 路线和 LLM 路线有什么本质分歧？

**A**: 两条路线对"AGI 的核心是什么"判断不同。**LLM 路线**（OpenAI/Anthropic）：智能 = 从海量文本预测下一个 token 学到的统计规律。语言是最浓缩的人类知识载体，scaling 文本 + 多模态 + 推理 = 通用智能。**JEPA 路线**（LeCun）：语言只是世界的薄薄一层。真正的智能必须建立在**对物理世界动力学的预测**上——一个 baby 都能预测"球会掉到地上"，但 LLM 没有这种 grounding。LeCun 认为只有 world model 才能给 AGI 提供这个基础。**两条路线目前都没有给出 AGI 的最终答案，还在博弈中**。

### Q4: 既然 World Models 6 年没进展，为什么还要把它讲在第四阶段？

**A**: 因为它是**演进的"种子"**。AI 发展史里有很多这种"提出很早但等了很久才落地"的例子——卷积神经网络 1989 年就提出了，等到 2012 年才爆发；attention 1990 年代神经科学就在讨论，2017 年 Transformer 才用对。**好的概念会等到基础设施到位才落地**。World Models 也是——它指明了方向（"AI 需要建立对世界的模拟"），但需要等 LLM、Diffusion、规模化训练这些基础设施齐备，2024-2026 才真正起飞（节点 11）。

---

# 节点 8：GEN-1

### Q1: GEN-1 在技术上有什么创新？

**A**: 它的核心创新是**把 latent diffusion 扩展到视频**，并解决两个特有挑战：① **时间一致性**——同一个物体在连续帧里要保持一致（颜色、纹理、形状），不能闪烁；② **structure preservation**——可以让生成视频保持输入视频的结构（如人物姿态、运动轨迹）。具体做法：在 U-Net 里加入时间维度的 attention（temporal attention），让模型同时处理空间和时间。

### Q2: GEN-1 / Sora / 可灵这些视频生成模型的核心区别？

**A**: ① **GEN-1（2023.02）**：早期工程实现，基于 latent diffusion + temporal attention，质量基础但实用；② **Sora（2024.02）**：OpenAI 用 diffusion transformer (DiT) 架构 + 极大规模训练，质量大幅提升，OpenAI 称之为 "world simulator"；③ **可灵（2024.06）**：快手发布，国内代表，强项是真实人物动作；④ **Veo 3（2025）**：Google 最新，质量对标 Sora。**整体趋势**：架构从 U-Net diffusion → Diffusion Transformer，规模和质量都在指数级增长。

### Q3: Sora 是 world model 吗？

**A**: **争议焦点**。OpenAI 在技术报告里明确称 Sora 为 "world simulator"——理由是 Sora 学到了一些物理规律（液体流动、物体遮挡、相机运动）。**反对意见**：① Sora 经常违反物理（手指数量、物体穿模）——如果真懂物理不该犯这种错；② 它没有 agent 在里面交互，不能称为 "world model"——只是 "video generator"；③ LeCun 公开反对，说 Sora 只是 "高级的 video generation"，离真正的 world model（能预测动力学、支持规划）还很远。**目前业界倾向认为**：Sora 是优秀的 video generator + 一些 world model 的雏形，但还不是完整的 world model。

### Q4: 为什么 GEN-1 在你的演讲里只占 15 分钟？感觉不公平。

**A**: 因为 GEN-1 在演进里**更像是"diffusion 走向视频"的标志节点**，不是独立的范式跃迁。它不像 Transformer / Diffusion / VLA 那样开创了新范式，而是把已有范式（diffusion）扩展到新模态（video）。所以分量自然小一点。**但它在产业意义上很重要**——Runway 把 GEN 系列做成了 SaaS 产品，是 AI 商业化最早成功的案例之一。

---

# 节点 9：推理大模型

### Q1: o1 / R1 这种推理大模型，"想得久"具体在做什么？

**A**: 在生成长链 chain-of-thought（CoT）。具体过程：模型在回答问题之前，先在内部生成一长串"思考过程"——分析问题、列举可能性、自我质疑、修正错误、最终给答案。**这个 CoT 有时候是隐藏的（o1）、有时候是显式输出的（R1 可以看到）**。CoT 的本质是**用更多 token 数量换更高质量答案**——模型把"瞬间反应"换成"逐步推理"，每一步犯错的概率小，累计起来正确率大幅提升。

### Q2: Test-time compute scaling law 的精确陈述？

**A**: DeepMind 2024 年那篇论文给了精确公式（用 best-of-N 或 search-based 方法）——**给定 LLM 性能，让它在推理时多想 K 倍时间，性能提升大致等价于把模型参数 scale 到 X 倍后的效果**。论文展示了一个非常震撼的图——**一个小模型 + 长推理时间，可以匹敌一个大模型 + 短推理时间**。这意味着推理 compute 和训练 compute 之间存在 trade-off，可以根据成本预算动态选择。

### Q3: DeepSeek R1 凭什么和 o1 性能对标？技术细节？

**A**: R1 论文里给出了完整 pipeline：① **DeepSeek-R1-Zero**——完全用 RL 训练（没有 SFT），仅用 rule-based reward（数学题答案对错），意外发现模型自动"涌现"出 self-reflection、verification 等推理行为；② **DeepSeek-R1**——加入少量 cold-start data 和多阶段训练（SFT → RL → SFT → RL），解决 R1-Zero 输出可读性差的问题；③ **关键发现**——RL 训练 reasoning 不需要复杂奖励模型，rule-based reward 就够。这彻底打破了 o1 的护城河。

### Q4: 推理大模型的 limitation 是什么？

**A**: ① **推理成本高**——一个问题要算几十秒，每次都要跑长 CoT，**推理 cost 是普通 LLM 的 10-100 倍**。这限制了它在 latency-sensitive 场景的应用。② **不是所有任务都吃推理**——简单问题（"今天天气怎么样"）让模型想 30 秒纯属浪费。需要"自适应推理"——按问题难度动态调整推理深度。③ **CoT 可能是表演**——研究显示 LLM 的 CoT 有时和最终答案不一致，模型可能"先有答案，再编 CoT"。④ **奖励黑客**——RL 训练可能让模型学会"骗 reward"，比如生成看起来推理很 deep 但其实没意义的 CoT。

### Q5（2026 新增）: DeepSeek R2 vs OpenAI o3，开源真的全面追平了？

**A**: **接近追平，但 SOTA 仍在 o3 系列**。需要先纠正一个常见误解——**R2 不是之前传言的 670B MoE，而是 32B dense transformer**（2025 年的传言版本最终没发布）。具体看维度：① **数学/推理 benchmark**：R2 在 AIME 2025 拿 92.7%；OpenAI o3-pro（2025.06）在 MATH-500 98.1% / SWE-bench 61.5% 仍领先；② **价格**：R2 比西方 frontier 模型便宜约 70%，但**真正的性价比突破**是它能在单张 24GB 消费 GPU（如 RTX 4090）上跑；③ **License**：MIT，可商用；④ **可部署性**：完全开源 vs o3 闭源 API。**结论**：性能上 o3 仍 SOTA，但 R2 选择了不同的路线——**放弃堆参数，押注"小模型 + 后训练优化"**。**护城河从模型规模转向了：数据飞轮 / 后训练工艺 / 部署生态 / 应用场景**。

### Q6（国内 LLM 追问）: Qwen / GLM / Kimi / DeepSeek 这几家国内 LLM 的差异化路线分别是什么？

**A**: 四家选了四种完全不同的差异化打法：

- **Qwen（阿里）**：**走 scaling + 全家族开源**。Qwen3 全家族从 0.6B 到 235B MoE 全开源，Qwen3-Max 1T 参数 / 36T tokens 训练，最近 Qwen3.5 Omni 走原生多模态。打法是"覆盖全场景 + 生态构建"。
- **GLM（智谱）**：**走"中尺寸高性能 + 国产芯片适配"**。GLM-4.6 是 355B MoE / 32B 激活，在国产芯片（Moore Threads）上做了 FP8+Int4 混合量化部署。打法是"国内供应链友好"。
- **Kimi（Moonshot）**：**直接押 agent 路线**。K2.5 主打"100 sub-agent 并行 + 1500 tools 同时"——不在比"单模型推理多强"，而是在比"模型作为 agent 编排器有多强"。打法是"agent-first"。
- **DeepSeek**：**走"小而精 + 后训练"**。R2 用 32B dense 做出 frontier 推理，强调"消费 GPU 可部署"。打法是"民主化 + 工程效率"。

**这四种路线在 2026 年同时存在**——说明 LLM 赛道已经进入"多元化竞争"阶段，不再是"做一个对标 GPT 的模型"那种单一目标。

---

# 节点 10：VLA ⭐⭐ 全场命门

### Q1: VLA 和"机器人 + LLM"有什么本质区别？

**A**: **本质区别在于动作 token 化 + 端到端训练**。"机器人 + LLM" 是 pipeline 架构——LLM 把自然语言指令解析成 high-level plan，然后调用专用的 motion planner 生成动作。VLA 是端到端 — **一个模型同时输入图像 + 语言，输出动作 token**（直接是机器人关节角度或末端位置）。这意味着：① 视觉、语言、动作三个模态在一个 latent space 里互相影响；② 训练时机器人动作直接被监督，不靠 LLM 的中间输出。**现代 VLA（π₀、GR00T N1）的标准架构**：vision encoder + LLM backbone + diffusion-based action expert。

### Q2: π₀ 为什么用 diffusion 来生成动作？

**A**: **Diffusion policy（Chi 2023）的核心洞察**——机器人动作是连续、多模态的。比如"把杯子放下"可以有很多种合理动作（轻放、稍微滑、转着放）。如果用普通的 token 预测（autoregressive），模型会输出"平均动作"——这往往是物理上不可行的（比如左手往左 + 右手往右的平均 = 站着不动）。Diffusion 可以建模整个动作分布，**采样时随机选一个 mode 执行**。π₀ 用了一个独立的 "action expert" 模块（参数从 LLM 共享），通过 diffusion 生成连续动作。

### Q3: VLA 的训练数据从哪来？这是不是最大瓶颈？

**A**: **是最大瓶颈之一**。当前主要数据来源：① **遥操作数据**——人戴 VR 操控机器人完成任务，记录视频 + 动作。每条数据成本几美元到几十美元，规模难上去（典型 VLA 数据集 100k-1M 条）；② **仿真数据**——在 Isaac Sim、MuJoCo 里跑大量 episode，便宜但有 sim-to-real gap；③ **互联网视频**——最新趋势，用 YouTube 上的人类做事视频做预训练，但视频里没有显式的动作标签，需要自监督方法（如 RT-Trajectory）。**关键挑战**：VLA 需要的"动作"数据本质上是稀缺的，不像文本（互联网海量）。这是 VLA 跟 LLM 的根本区别——VLA 没法靠 scaling 数据来打。

### Q4: VLA 路线 vs 传统机器人控制 vs 完全 world model 驱动，哪条路会赢？

**A**: 我的判断是**融合**。三条路线各有强项：① **VLA**——端到端简单、跨任务泛化好，但数据稀缺、对长程任务力不从心；② **传统分层控制**——已有的 motion planning / control 算法非常成熟，对精度要求高的工业场景仍是 SOTA，但泛化差；③ **World model 驱动**——理论最优，但目前 world model 还不够 robust。**未来 1-2 年的趋势**：VLA 处理感知 + 高层动作生成，传统控制处理底层精确执行，world model 提供训练环境 + 长程规划。**Figure Helix 02 的三级架构（System 0 实时平衡 1kHz / System 1 视觉运动 200Hz / System 2 高层推理）就是这个融合的早期例子**——而且它已经能完成洗碗机 4 分钟连续自主任务。

### Q5（2026 新增）: Helix 02 和 GR00T N1.6 的具体技术差异？

**A**: 两者都是当前 VLA 的最强代表，但路线略有不同：

**Helix 02（Figure AI, 2026.01）**：

- **三级架构**：System 0（1kHz 实时平衡） + System 1（200Hz 视觉运动） + System 2（高层推理）
- 单一神经网络（10M 参数）替代了 109,504 行 C++ 代码
- 训练数据：1000+ 小时人类动作 + 200,000+ 仿真环境
- 强项：**全身协调、长程任务**（洗碗机 4 分钟）
- 部署：嵌入式低功耗 GPU

**GR00T N1.6（NVIDIA, 2026.04.15）**：

- **双系统架构** + **内部 VLM 升级到 Cosmos-Reason-2B**（自家 world model）
- Diffusion Transformer 翻倍（32 层 vs 16 层）
- 训练时解冻 VLM 顶部 4 层
- 强项：**VLA + World Model 融合**——这是产品级首次
- 开源：可商业使用

**核心差异**：Helix 02 强在"全身控制 + 长程任务"，GR00T N1.6 强在"world model 集成 + 开源生态"。**两者代表了 VLA 在 2026 年的两个发展方向**——一个往"任务复杂度"走，一个往"模型能力上限"走。

### Q6（2026 新增）: 为什么 Elon Musk 要质疑 Helix 02 的 demo？

**A**: 几个原因：① **商业利益**——Tesla Optimus 是 Figure AI 的直接竞品，Musk 自然会唱反调；② **行业有信任问题**——之前有些机器人 demo 是遥操作伪装成自主，Musk 这种质疑符合"内行直觉"；③ **Figure 没撤 demo 反而出新视频**（3 月份的客厅整理）——这增加了真实性。**整体来看 Helix 02 的能力是真实的**——技术路线（三级架构 + 10M 神经网络）是公开的，Cosmos / NVIDIA 等多家也在做类似工作，互相印证。但**对外讲这个 demo 的时候要小心措辞**——可以说"Figure AI 称 Helix 02 完成了..."，不要说"Helix 02 真的做到了..."，给自己留余地。

### Q7（国内具身追问）: 国内具身公司（智元 / 银河通用 / 宇树）和 Figure / Pi-0 比，差距在哪？或者优势在哪？

**A**: **不是简单的差距，是不同的路线选择**：

**国外路线（Figure / Physical Intelligence）**：

- 重金投入 + 全栈自研（从硬件到 VLA 全部自己做）
- 估值高（Figure $39B，Physical Intelligence $24B），数据收集靠重金 teleoperation
- 单台机器人价格高（Figure 02 数十万美元）
- 优势：技术指标突出、demo 惊艳

**国内路线（智元 / 银河通用 / 宇树）**：

- **硬件价格压低 + 开源 + 数据规模**——宇树 G1 售价 $13.5K，比 Figure 02 低一个数量级
- **数据集开源**——智元 AgiBot World 100 万条轨迹 / 217 任务全部开源；银河通用主推合成数据预训练
- **生态绑定**——宇树 UnifoLM-VLA-0 直接基于 Qwen2.5-VL，国内 LLM + 国内具身互相用
- 优势：**研究门槛降到消费级、数据共享、迭代快**

**两条路线的根本差异**：国外押"垂直整合 + 高价值"，国内押"开源生态 + 低价格 + 大规模"。**哪条会赢？很可能不是单一答案——国外的高端工业场景（Figure 进宝马工厂）和国内的研究/教育/中端场景（宇树 G1 进高校实验室）会并行存在**。

### Q8（国内具身追问）: ViLLA 架构（智元 GO-1）和传统 VLA 有什么本质区别？

**A**: 核心区别在于**Latent Action 这一层**。传统 VLA 是 V → L → A（看图 + 理解语言 + 直接生成动作）。ViLLA 在 L 和 A 之间加了一层 **Latent Planner**：

- **Latent Planner**：从跨形态（cross-embodiment）数据 + 人类操作视频里学"动作意图"的潜在表示——不绑定具体机器人形态
- **Action Expert**：基于 100 万条真实机器人 demonstration 训练，把 latent 动作 decode 成具体关节角度
- 配合 MoE 架构

**好处**：① 可以从人类视频学习（不需要总靠机器人 teleoperation 收集数据）；② 跨形态适应更好；③ 数据效率高。

**这个思路和 Physical Intelligence 的 π₀ 有点像**（都强调 cross-embodiment + 用 diffusion-based action expert），但 ViLLA 的"latent action"中间层是 GO-1 的独特创新——**这是国内团队对 VLA 范式的一个原创性贡献**。

---

# 节点 11：World Models 突破

### Q1: Genie 3 和 2018 年 David Ha 那个 World Models 有什么本质突破？

**A**: 三个本质突破：① **规模**——Ha 的 model 是 VAE + RNN，几百万参数，只能跑 CarRacing 这种玩具任务。Genie 3 是 LLM 级别的参数规模，可以生成 720p 多分钟可交互 3D 环境；② **可交互性**——Ha 的 model 只能让一个固定 agent 在 latent space 里训练。Genie 3 让用户可以**实时操控**生成的世界——按方向键探索 3D 空间，模型动态生成下一帧；③ **通用性**——Ha 的 model 必须为每个任务重新训练 V/M/C。Genie 3 是 foundation model，从一张图或一段文本生成新世界。**这三个突破靠的就是 LLM 时代的算力 + Diffusion + Transformer 这些基础设施**。

### Q2: NVIDIA Cosmos 和 Genie 3 的定位有什么不同？

**A**: ① **Cosmos** 定位为"机器人和自动驾驶的训练 world model"——目标是用户可以**用 Cosmos 生成大量物理可信的训练数据**，喂给 VLA 或者自动驾驶模型。强调**物理一致性**（重力、碰撞、光照）和**可控性**（用户能精确指定场景）。② **Genie 3** 定位为"通用交互式世界生成"——更偏游戏 / 创意 / 探索方向，强调**视觉质量**和**交互流畅度**。**简单说**：Cosmos 是"训练 agent 的虚拟道场"，Genie 3 是"给人类玩的可生成世界"。两者都属于 world foundation model 范畴。

### Q3: World Model 和 SLAM/3DGS 这种重建方法有什么关系？

**A**: 这是个好问题。**SLAM/3DGS 是"重建已存在的世界"**——你需要先用相机、雷达扫描真实场景，然后算法重建出 3D 表示。**World Model 是"生成可能的世界"**——从训练数据学到"世界长什么样、怎么变化"，然后可以生成新世界。**两者正在某种程度上汇合**：① Genie 3 这种 world model 已经能生成"近似可信的物理"——输出的 3D 环境物体不会随便穿模、光照基本正确；② 反过来 3DGS 的最新工作（如 4DGS）在做"动态场景重建"，预测下一帧也是某种 world model；③ 未来 world model 可能用 SLAM/3DGS 作为训练数据源，SLAM/3DGS 也可能用 world model 做先验。**这两条线长期会越来越近**。

### Q4: World Model 的 limitation 是什么？

**A**: ① **物理一致性还不够**——Genie 3 的 demo 里仍然有物体穿模、光照错乱。距离"真正可信的物理仿真"差很远。② **长时一致性差**——Genie 3（2025.08）做到了几分钟级别的一致性，但生成更长时间（10+ 分钟）的连续世界仍然会出现物体"记不住"——你转过身再转回来，原来的椅子可能消失或变形。720p 分辨率也仍然不够"工业级"。③ **可控性 vs 多样性的 trade-off**——精确控制每个物体（"红椅子在窗前 30cm 处"）很难做到，往往是"模糊控制"。④ **训练成本极高**——Cosmos 用了大规模数据（NVIDIA 公布约 9000 万亿 tokens 量级，需要再核实）。能训这种规模的全球只有几家。⑤ **还没找到"杀手级应用"**——除了机器人/自动驾驶训练这个明确场景，其他场景（游戏、影视）还在探索。

### Q5（2026 新增）: Genie 3（2025.08）发布之后，World Models 这个方向有什么实质进展？

**A**: 几个关键进展：① **Genie 3 自身的影响**——它是第一个公众可访问的实时交互通用 world model（720p / 20-24 fps / 几分钟一致性），证明 world model 已经可以从 demo 走向实际产品；② **Cosmos 成为基础设施层**——NVIDIA 在 2025.01 CES 发布的 Cosmos，到 2026 年下载量已超 200 万，被 Figure AI / Uber / Waabi 等具身和自动驾驶厂商采用；③ **VLA + World Model 融合进入产品级**——4 天前发布的 GR00T N1.6 直接用 NVIDIA 自家 Cosmos-Reason-2B 作为内部 VLM，这是融合不再停留在论文层面的标志；④ **路线之争升级**——LeCun 的 JEPA / world model 路线继续推进，与 OpenAI 的 LLM scaling 路线之间的张力在增大。但**目前哪条路会主导 AGI 还没有定论**。

### Q6（重建侧追问）: VGGT / DUSt3R 这些"transformer 替代 SfM"的工作，传统 SLAM 还有没有用？

**A**: **传统 SLAM 还会用很久，但角色在变**。

**VGGT / DUSt3R 解决了什么**：

- 输入未标定图像，直接输出 3D 几何（相机参数 + 深度 + 点云）
- **完全跳过传统 SLAM 的 feature matching → bundle adjustment → 后处理优化** pipeline
- 在 map-free 场景（没有先验地图、相机不标定）效果惊人

**VGGT / DUSt3R 还做不到的**：

- ① **实时性**——VGGT "1 秒内"是 offline 重建；传统 VIO/SLAM 是 100Hz+ 的实时 6DOF 估计
- ② **大规模长期建图**——VGGT 能处理几百张图，但城市级地图（百万张图）还得靠传统方法
- ③ **传感器融合**——传统 SLAM 处理 IMU / GPS / 激光雷达 / 多相机融合的 mature pipeline，VGGT 目前只是纯视觉
- ④ **可解释性 + debug**——传统 SLAM 的每一步（feature / matching / pose / map）都可观察、可调；端到端 transformer 是黑盒

**未来 1-2 年的趋势**：**两条线会融合**——VGGT 提供"快速 init + 全局结构感知"，传统 VIO/SLAM 处理"实时跟踪 + 局部精化 + 多传感器融合"。**这恰好是我做的 VIO / 重定位方向最近的演进方向**。

### Q7（重建侧追问）: 3DGS 已经讲了 3 年了，现在还有什么新进展？

**A**: 3DGS 一直在快速演进，2024-2026 主要方向：

- ① **动态场景**：4D Gaussian Splatting / Dynamic 3DGS——把"静态场景重建"扩展到"动态视频重建"
- ② **大规模场景**：Hierarchical 3DGS / Block-based GS——把 3DGS 从单个房间级扩展到城市级
- ③ **几何精度提升**：2D GS / Gaussian Surfels——传统 3DGS 在表面精度上不够，新工作把 Gaussian 退化到 2D 圆盘改善 mesh 质量
- ④ **生成 + 重建融合**：把 diffusion 模型作为 3DGS 的 prior，用文本 prompt 编辑 3DGS 场景
- ⑤ **VGGT 的影响**：VGGT 输出的 dense pointmap 可以直接初始化 3DGS，跳过 SfM 这一步——这是 2025 之后的新 pipeline

**对你 SLAM 工作的影响**：3DGS 已经从"纯渲染技术"变成"3D 表征的标准选项之一"——和 mesh / voxel / SDF / point cloud 并列。**未来 SLAM 的输出可能不只是稀疏点云 + 关键帧，而是直接输出 3DGS 表征**。

### Q8（个人视角追问）: 你做 SLAM/3DGS，怎么看 World Models 这条线对你工作的影响？

**A**: 三个层次的影响：

- ① **技术层**：World Models 用的 transformer + 大规模预训练这套，正在反向影响 SLAM——VGGT 就是直接的例子。**我们这些做 SLAM 的人必须主动去理解 transformer 范式**，否则会被时代抛下。
- ② **应用层**：具身智能（VLA）需要 SLAM 提供环境理解，World Models 提供"想象的场景"训练 agent——**SLAM 不再是孤立学科，是具身智能 stack 的底层组件**。
- ③ **职业层**：做 SLAM 的人未来会有两个方向——一个是"SLAM as foundation infrastructure for embodied AI"，另一个是"SLAM 工程师转向 3D foundation model 研究"。**两条路都有未来，但都需要主动跟进 AI 主流的演进**——这恰好是我这次准备这个分享的个人收获。

---

# 综合性追问（跨节点）

### Q-X1: 你今天讲的这些技术里，哪个对你的工作影响最大？

**A**: 这是个"对我个人"的问题，**用 SLAM 视角答**——目前对我影响最大的是 **VLA + World Models 这两条线的汇合**。我做 SLAM 和 3DGS，做的就是"AI 怎么理解三维世界"。VLA 让我看到 SLAM 在具身智能里有了**新的 downstream consumer**——不是给人类看的地图，而是给机器人 agent 用的环境表征。World Models 让我看到 3DGS 这种"世界重建"技术，**未来可能和"世界生成"汇合**。这两件事让我觉得我做的方向，跟 AI 主流不再是平行线，而是**变成主流的一部分**。

### Q-X2: 这些技术演进的"驱动力"是什么？算法、算力、数据？

**A**: 不同阶段不同。① **2012 年深度学习爆发**：算力（GPU）+ 数据（ImageNet）+ 算法（ReLU、Dropout）三者同时到位；② **Transformer + LLM**：算法（attention）打破了串行约束，让 scaling 成为可能；③ **Diffusion**：算法（DDPM）+ 算力（更大 GPU）；④ **LLM 时代到现在**：**算力 + 数据 + 工程**才是主导，纯算法创新边际收益递减。但 **2024 推理大模型 + DeepSeek R1**：又是算法（RL training of reasoning）的回归——证明在已有 LLM 基础上，新的训练范式可以打开新维度。**所以我的判断是**：算法、算力、数据三者交替主导，不存在单一驱动力。

### Q-X3: 如果让你预测下一个 5 年 AI 最大的方向，是什么？

**A**: 我个人押**具身智能 + world model + 推理 这三者的融合**——也就是今天讲的 3 节点闭环。具体形态可能是：通用 agent foundation model，能在虚拟 world model 里训练，部署到现实做长程任务。**为什么押这个**：① 它是当前 3 个最热方向的自然融合；② 它对应"AI 走出屏幕进入物理世界"这个范式跃迁；③ 它能解锁的市场（机器人、自动驾驶、家庭服务）巨大。**反对论据**：纯 LLM 路线的拥趸（OpenAI/Anthropic）认为"先把 LLM 做到 AGI，再考虑具身"。**两条路都有道理，谁赢看 2026-2028 年**。

### Q-X4: 你这个分享里最不确定的是哪个判断？

**A**: 最不确定的是**节点 4 LLM 那段关于"涌现是真是假"的判断**——这个学术界还在吵。我倾向"涌现是真的有，但被滥用了"，但这是个争议话题，欢迎讨论。其次不确定的是**节点 11 World Models 突破的"重建 vs 生成汇合"**——这是我从 SLAM 视角的判断，但目前业界还没有共识，可能我看错。**我说这些，是因为应该让大家知道哪些是事实、哪些是判断、哪些是猜测——不应该把猜测当事实讲**。

### Q-X5: 2025-2026 最新的进展里，哪个对你这次分享的判断有冲击？

**A**: 有几个，按冲击程度排序：

① **GR00T N1.6 + Cosmos Reason 2（2026.04.15，4 天前）** —— NVIDIA 把自家 world model（Cosmos-Reason-2B）直接作为内部 VLM 集成进 GR00T。**这件事不是研究 paper，是产品 release**。意味着 VLA + World Model 融合不再是我嘴上说的"未来趋势"，而是**已经发生了**。这是我这次分享 3 节点闭环判断最强的证据。

② **Helix 02（2026.01.27）的洗碗机 4 分钟连续自主任务** —— 61 separate loco-manipulation actions，目前人形机器人最长最复杂的自主任务。Figure AI 称之为"the longest horizon, most complex task completed autonomously by a humanoid robot to date"。说明 VLA 已经从 demo 走到"工业级长程任务"。

③ **DeepSeek R2（2026.04）的架构选择** —— **不是之前传言的 670B MoE，而是 32B dense**——能在单张 RTX 4090 上跑 frontier 级推理。这件事让我重新想了一下"开源 vs 闭源" 的格局：DeepSeek 选择了"小而精 + 后训练"路线，这可能是另一种主流路径，不只是"追赶闭源"。

④ **Mamba-3（2026.03.16）** —— Transformer 架构垄断了 9 年的局面正在被打破，但不是替代，而是分化成"专业化生态位"。

⑤ **Genie 3（2025.08）** —— world model 第一次走向公众，720p 实时交互 3D 环境生成。结合 Cosmos 的产业落地（200 万下载量，Figure / Uber / Waabi 采用），world model 这条线已经从"前瞻方向"变成"产品基础设施"。

这些都让我意识到一件事——**AI 演进的速度比我们想象的快**。所谓"经典节点"和"前沿节点"的区分在加速消失，而**真正可信的判断必须基于跟得上 release timeline 的事实**——这也是我这次准备过程的最大教训：我之前对几个关键时间点（如 Genie 3 是 2025.08 不是 2026.03）和几个具体数字（如 R2 架构）有误，是通过事实核查才修正的。**讲 AI 趋势千万不能凭印象**。

---

# 应对策略：被问到完全不会的问题

如果有人问到稿件 + 这份 Q&A 都没覆盖的问题，**3 步应对**：

1. **重复问题确认理解**：「你的意思是 ……？」——给自己 2 秒思考时间
2. **诚实但不慌**：「这个具体细节我没研究过 / 我不太确定」
3. **抛回讨论或承诺会后看**：「我的初步直觉是 ……，但你是不是有更专业的 take 想分享？」 / 「会后我会去查一下，回头我们聊」

**最忌讳的**：硬编一个答案。Leader 视角看，**承认不知道 > 编错答案**。曹丽娜本人懂 AI，编错她大概率听得出来。

---

# 学习建议

按这个顺序用这份 Q&A：

1. **周一-周三晚**：每读完一个节点的材料（按 `06-reading-list.md`），就过对应节点的 Q1-Q4，自己用 30 秒口头答。答不出来 → 回去读材料 → 再答。
2. **周四晚**：过一遍**综合性追问 Q-X1 到 Q-X4**——这些是对全局判断的考验，需要你把 11 个节点串起来思考。
3. **周五现场前**：再快速过一遍每个节点的 Q1（"是什么"）——保证最基础的事实答得上来。

**最高优先级**：节点 3 Transformer + 节点 4 LLM + 节点 9 推理 + 节点 10 VLA + 节点 11 World Models 突破——这 5 个节点的 Q&A **必须吃透**，它们是被追问概率最高的。

---

# 附录 M：机制档新增追问（2026-04-27 扩充版）

> **背景**：稿件从 ~34 min 扩到 50 min 的"机制档"——讲了 self-attention QKV、scaling law 公式、Mamba SSM、DDPM L_simple、CLIP InfoNCE、V+M+C、JEPA 等更多机制和公式骨架。
> **这一段专门覆盖机制档新增内容引发的追问**——**这些是听众在听到公式骨架后最可能追问的问题**，必须自己先答得清楚。
> **本场（前 4 阶段）才会被问的**：M1–M9。**延伸段如果被现场拉出来讲才会被问的**：M10–M12（保底准备，不重点演练）。

## M1：Transformer 里 attention 公式那个 √d_k 是干嘛的？

**A**：是为了**防止 softmax 饱和**。Q 和 K 都是 d_k 维向量，点积 QKᵀ 的方差会随 d_k 增大——维度越大，点积值越大。如果不除 √d_k，softmax 输出会接近 one-hot（最大值的概率几乎是 1，其他都接近 0），这时候**梯度直接消失**，模型学不到东西。除以 √d_k 让点积保持在合理量级（约 N(0, 1)），softmax 输出"软选择"而不是"硬选择"。这是 Vaswani 2017 论文 §3.2.1 专门讨论的工程细节，不是数学优雅，是工程必要。

## M2：为什么 GPT 系把 encoder 拿掉了？只用 decoder 不会丢信息吗？

**A**：不会丢。原始 Transformer 的 encoder–decoder 是为机器翻译设计的——encoder 看源语言，decoder 看目标语言加 cross-attention 看源语言。GPT 系做的是**单一语言建模**（next-token prediction），没有"两种语言"的概念，所以**不需要 cross-attention，也不需要 encoder**。**关键好处是数据规模**：causal mask + next-token prediction 让任意一段文本都自带监督信号——下一个词就是 label。这把训练数据从"标注的语料"扩到了**全互联网**——这是 GPT 路线能 scale 到 175B 的根本原因。Encoder–decoder 路线（T5、BART）至今没 scale 到 GPT 量级，根本原因不是架构差，是它们更难找到这么大规模的"配对数据"。

## M3：Chinchilla 修正了 Kaplan 什么？这个修正后来的影响是什么？

**A**：**Kaplan 2020 认为算力主要应该堆给模型规模，data 是次要的**——所以 OpenAI 当时做了 GPT-3 175B + 300B token，认为这是最优。**Chinchilla 2022 用更细的实验告诉大家：模型规模和数据应该同步 scale，每翻一倍参数，data 也应该翻一倍**——他们用 70B + 1.4T token，**性能反而超过 GPT-3 175B 和 Megatron-Turing 530B**。**后来的影响很大**：① Llama-2 70B 用 2T token、Llama-3 70B 用 **15T token**——都是 Chinchilla 配比的延续；② 行业意识到"data 才是真护城河"，开源社区开始疯狂囤数据（C4、RedPajama、FineWeb 这些都是 Chinchilla 之后才出现的大规模 open dataset）。

## M4：你说"涌现"可能是评估幻觉，那它到底是真的还是假的？

**A**：**两边都有一部分**——这是 NeurIPS 2023 那篇 Schaeffer "Are Emergent Abilities of LLMs a Mirage?" 之后的共识。**Schaeffer 的论点**：如果用 0/1 准确率（要么全对要么 0 分），就会看到"突然涌现"的曲线；但用 token-level log-prob（连续指标），曲线就变平滑、可预测。这部分"涌现"是评估指标不连续造成的幻觉。**但同时**：某些能力（比如 chain-of-thought 推理、in-context learning）即使用连续指标也确实有相对清晰的"出现阈值"——这部分是真现象。**我现场会用的安全表述**：「'涌现'在科普语境里被讲得有点神秘，但学界本身还在争论它是真现象还是评估幻觉，我倾向于'两者都有'，但这是个 open question。」——**不下定论 = 不犯错**。

## M5：Mamba 的 selective SSM 关键创新到底是什么？为什么 A 矩阵不动而 B、C、Δ 动？

**A**：**关键创新是让 B、C、Δ 三个参数 input-dependent**——也就是**根据当前 token 的内容动态决定"保留还是丢弃信息"**——这其实就是 attention 的"软选择"思想，但保留了 SSM 的 O(n) 复杂度。**Δ（离散化步长）尤其关键**——它控制状态更新的速度，input-dependent 之后就能根据 token 重要性动态加快/放慢状态变化。**为什么 A 不能 input-dependent**？因为 Mamba 的训练效率依赖一个叫 **hardware-aware parallel scan** 的算法——这个算法要求 A 矩阵在序列上是 time-invariant（每一步用同一个 A），否则 GPU 上没法并行计算。**这是工程约束，不是数学美感**——A 矩阵保持 HiPPO 初始化、time-invariant，是为了"训得动"。

## M6：DDPM 那个 L_simple 损失为什么这么简单？这就是个 L2 回归吧？

**A**：**对，就是个 L2 回归**——给 (x_t, t) 预测加进去的噪声 ε。论文里 Ho et al. 也确实从 ELBO（变分下界）推导过更复杂的形式，但**最后实验发现，简化成这个 L2 回归反而效果更好、更稳定**。这是 Diffusion 的优雅之处——**训练目标极简，没有 GAN 的 min-max 博弈，没有 VAE 的高斯单峰假设**——两边的痛点同时被绕开。**为什么预测 ε 不预测 x_0**？两种参数化都试过，**预测噪声 loss 更平滑、训练更稳**——这是工程发现，不是数学必然。**为什么稳**？因为每一步只学一个"小的噪声差"——任务被切成 1000 个简单子任务，每个都很容易。

## M7：Stable Diffusion 和原始 DDPM 最大的区别是什么？为什么 SD 能在消费级 GPU 跑、DDPM 不能？

**A**：**最大区别是 latent diffusion** ——SD 不在像素空间扩散，先用一个 VAE 把 512×512 RGB 压到 64×64 latent，**在 latent 空间扩散，最后再 decode 回像素**。**计算量降一个数量级**：512×512×3 ≈ 79 万维 vs 64×64×4 ≈ 1.6 万维。**这是 Rombach 2022 那篇 CVPR 论文的核心贡献**，也是 SD 能开源跑起来的真正机制核心。**还有第二件事是 DDIM 采样加速**：DDPM 训练时 1000 步、推理也要 1000 步，慢；DDIM 把 SDE 重写成 ODE，可以**跳步采样**——20-50 步达到 1000 步同等质量。**两件事合起来**——latent + DDIM——SD 才能在 RTX 3060 上 5 秒出图。

## M8：CLIP 的对比学习训练时，N×N 矩阵里负样本怎么挑？为什么 4 亿对数据是关键？

**A**：**negative sample 不需要专门挑**——对比学习的优雅之处就是**一个 batch 里 N 对 (图, 文)**，对角线是真实配对，**所有非对角线 N²−N 个组合自动就是负样本**。所以一个 batch N=32K 时，每张图自动就有 ≈32K 个负样本去对比，**完全免费**。**为什么 4 亿对是关键**？因为对比学习的负样本质量决定一切——你能从多大的池子里挑出多难的负样本，模型就能学到多细的语义区分。4 亿对覆盖了互联网各种长尾概念（"a photo of a quagga"、"a sketch of a 1960s Cadillac"），所以 CLIP 能 zero-shot 识别这些罕见概念。**数据规模本身就是模型质量**——这是后来所有 VLM 都遵循的规律。

## M9：JEPA 路线 LeCun 提了 4 年了，至今没有 GPT 量级的爆点产品，是不是这条路有问题？

**A**：**两个事实必须同时承认**：① JEPA 至今确实没有 GPT 量级的爆点产品（V-JEPA、I-JEPA 都是研究 demo 级别）；② 但 JEPA 的核心思想——**在表示空间预测、不在像素/token 空间预测**——已经渗透到 2025-2026 最强的几个 world model 里：Genie 3 在 latent 上做世界模拟而不是直接预测像素、NVIDIA Cosmos Reason 是个 reasoning over latent 的模型、GR00T N1.6 把 Cosmos VLM 集成进 VLA 也是这条思路。**我的态度**：「JEPA 这条路'独立成军'还没成功，但它的核心机制其实已经被借鉴去和 LLM 路线汇合。'谁替代谁'不是 LeCun 期待的剧本，但'两条路汇合'可能是真实的剧本。」——**不站队，但承认 JEPA 影响力**。

## M10：Helix 02 的"三级架构"具体是哪三级？为什么要做三级而不是两级？（仅在被现场拉出延伸段时才会问）

**A**：① **System 0** — 1 kHz 实时平衡控制（关节级 PID 类控制）；② **System 1** — 200 Hz 视觉运动控制（端到端神经网络出关节力矩）；③ **System 2** — 高层任务规划（LLM 级推理）。**为什么三级而不是两级**？借鉴 Kahneman 《Thinking, Fast and Slow》——**人脑也有这种分层**：脊髓反射（System 0）、潜意识动作（System 1）、显意识思考（System 2）。**工程上的好处**是**把不同时间尺度的控制隔离开**——平衡需要 1 kHz、视觉运动 200 Hz 够、推理 1-10 Hz 就行——同一个网络做不到这种跨 3 个数量级的频率，必须分层。

## M11：DeepSeek R2 既然是 32B dense，那为什么之前传言是 670B MoE？传言是怎么来的？（仅在被追问时）

**A**：**670B MoE 是 2025 年的 DeepSeek 内部 rumor + 一些泄漏**——当时业界普遍预测 R2 会沿用 V3 的 671B MoE 架构、用 37B 激活做推理。但 2026.04 实际发布的 R2 走的是完全不同的路线——**32B dense transformer，单张 24GB GPU 可部署**，AIME 2025 92.7%。**这是 DeepSeek 团队的产品判断**——他们认为"小而精的 dense + 后训练优化" 在推理任务上比"大 MoE" 更有市场（部署成本低 + 微调容易）。**我的安全表述**：「2025 年的传言数字大家可能记得是 670B MoE，但 2026.04 实际 release 是 32B dense——产品形态变了，团队选了'部署友好'路线。」

## M12：VGGT 真的能完全取代 SfM/SLAM 吗？bundle adjustment 的精度优势怎么办？（你的 SLAM 主业被追问时）

**A**：**短期不能取代精度敏感场景**——VGGT 是 feed-forward transformer，1 秒内出相机参数+点云，**速度碾压、精度还差一截**。在测绘、文物数字化、AR 厘米级定位这些精度敏感场景，bundle adjustment 仍然是 ground truth。**但 VGGT 给了一条新路**——**先用 VGGT 在 1 秒内出粗解，再用传统 BA 在这个粗解上精化**——比传统从零做 SfM 快 10-100 倍。**长期看**——transformer + 海量预训练数据这条路，在精度上追上 BA 是迟早的事，因为 BA 只用单序列内的几何信息，transformer 可以借用整个互联网的几何先验。**我的判断**：「BA 还有 3-5 年优势，但 VGGT 已经在'速度 + 鲁棒性'上完胜——下一代 SLAM 系统大概率是混合架构。」——**这是你 SLAM 主业的核心立场，必须答得稳**。