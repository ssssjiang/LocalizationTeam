# 📘 第 5 课：CLIP 训练数据与零样本应用

> 学习目标：理解 4 亿 WIT 数据集的来源与意义；吃透零样本分类的数学机制；掌握 prompt engineering 的精髓；看清 CLIP 的能力边界。
>
> 预计阅读时间：30 分钟。读完本章，CLIP 主线**完整闭环**。

---

## 一、WIT 数据集：4 亿对从哪来

### 现有数据集的困境

CLIP 之前，公开的图文数据集长这样：

| 数据集 | 规模 | 特点 |
|---|---|---|
| MS-COCO | 60 万对 | 人工标注，质量高，**类别封闭**（80 类物体） |
| Visual Genome | 510 万对 | 密集标注 region + caption，质量极高 |
| Conceptual Captions (CC3M) | 330 万对 | Google 从 web alt-text 爬取并清洗 |
| YFCC100M | 1 亿张图 | Flickr 用户上传，但很多 caption 是噪声（如 "IMG_2345.jpg"） |

**核心矛盾**：

- 高质量数据集（MS-COCO, VG）→ 规模太小，且类别封闭
- 大规模数据集（YFCC100M）→ 噪声大、覆盖偏，对训练对齐用处有限

### OpenAI 的解法：自建 WIT

OpenAI 决定**自己爬一份满足两个条件的数据集**：

1. **规模超大**——至少和 GPT 系列的语言数据可比（数百亿 tokens 量级）
2. **覆盖广**——不要被某个领域偏置（如 Flickr 偏旅游、COCO 偏日常物体）

具体做法（论文 Section 2.2）：

1. 准备一个 **500K 词的查询词表**（query list），来源是 Wikipedia 上出现至少 100 次的所有英文词条 + WordNet 同义词集
2. 对每个查询词，从公开互联网搜索，把"图 + 配套文本"配对收集
3. 平衡每个查询词的样本数（每个最多 2 万对），保证覆盖均匀
4. 最终得到 **4 亿对**

> **关键设计**：用查询词表"撒网"，比纯随机爬取**覆盖更均匀**。这避免了"全是猫狗、没有显微镜"这种长尾失衡。

### WIT 没有公开

OpenAI 的政策是**只开源模型权重，不开源数据**。

后续的开源复现工作：

| 项目 | 数据 | 规模 |
|---|---|---|
| **OpenCLIP** (LAION) | LAION-400M / LAION-2B | 4 亿 / 20 亿 |
| **DataComp** (UW + Allen AI) | DataComp-1B | 12.8 亿（更精细的过滤） |

→ 今天主流开源 CLIP 模型（HuggingFace 上随手能下的）大多是用 LAION 训的 **OpenCLIP**，性能与原版 CLIP 持平甚至超越。

### 数据规模 vs 性能（CLIP 论文 Figure 9 简化版）

```
ImageNet zero-shot top-1
80% ┤                          ━━━ ResNet-50 监督训练 76%
    │                       ╱╱
70% ┤                    ╱╱
    │                 ╱╱
60% ┤              ╱╱
    │           ╱╱
50% ┤         ╱
    │       ╱
40% ┤      ╱
    │    ╱
30% ┤   ╱
    │  ╱
20% ┤ ╱
    │╱
    └──┬───┬────┬────┬────┬─────
       15M 100M 200M 400M 800M(假设)  数据规模
```

**关键观察**：

- 1500 万对：仅 11% top-1（接近瞎猜）
- 4 亿对：76.2% top-1（追平监督学习）

→ **数据规模是 CLIP 工作的"魔法"**。规模不到位，再好的对比学习架构也学不出零样本能力。

这一点很关键——它意味着 **CLIP 的成功无法在小规模上复现**。中小机构想训自己的 CLIP，至少要 LAION-400M 起步。

---

## 二、零样本分类：CLIP 最 Killer 的 App

### 它有多神奇？

把训练好的 CLIP 直接套到 27 个完全没见过的图像分类数据集上（不做任何 fine-tuning），结果：

| 数据集 | CLIP zero-shot | 监督训练 | 是否超越监督 |
|---|---|---|---|
| ImageNet | 76.2% | 76.5% (ResNet-50) | 几乎追平 |
| Stanford Cars | 65.7% | 65.6% | ✅ 追平 |
| Food101 | 88.8% | 88.7% | ✅ 追平 |
| OxfordPets | 93.5% | 95.6% | 略低 |
| **MNIST** | **57.1%** | 99.7% | ❌ 远低 |
| EuroSAT (卫星) | 41.1% | 84.1% | ❌ 远低 |

→ **CLIP 在"自然世界的常见物体"上极强；在"训练数据稀少的领域"（卫星、医学、手写数字）上很弱。**

后面会讲为什么。先看零样本分类的运行机制。

### 零样本分类的数学机制

设 ImageNet 1000 类。我们从来没在 ImageNet 上 fine-tune 过 CLIP，怎么用它分类？

**步骤 1：把 1000 个类名变成 1000 句话**

```
"tench"          →  "a photo of a tench."
"goldfish"       →  "a photo of a goldfish."
"great_white_shark" → "a photo of a great white shark."
...
"toilet_tissue"  →  "a photo of a toilet tissue."
```

**步骤 2：用 text encoder 一次性编码 1000 句话**

得到 1000 个文本向量 $\mathbf{T}_1, \mathbf{T}_2, \ldots, \mathbf{T}_{1000} \in \mathbb{R}^{512}$。

**这 1000 个向量可以预先算好缓存——这就是双塔架构的优势。**

**步骤 3：来一张测试图 $\mathbf{x}$**

用 image encoder 编码：$\mathbf{I} = f_I(\mathbf{x}) / \|\cdot\|_2$。

**步骤 4：算这张图和 1000 个文本向量的余弦相似度**

$$
s_i = \mathbf{I}^\top \mathbf{T}_i, \quad i = 1, \ldots, 1000
$$

**步骤 5：取相似度最大的那个 $i$ 作为预测类别**

$$
\hat{y} = \arg\max_i s_i
$$

完了。这就是 CLIP zero-shot 分类的全部。

### 用 pseudo-code 表达

```python
# 准备阶段（每个数据集只做一次）
class_names = ["tench", "goldfish", ..., "toilet tissue"]   # ImageNet 1000 类
prompts = [f"a photo of a {c}." for c in class_names]
text_features = clip.encode_text(prompts)                   # [1000, 512]
text_features = F.normalize(text_features, dim=-1)

# 推理阶段（每张图）
image_features = clip.encode_image(x)                       # [1, 512]
image_features = F.normalize(image_features, dim=-1)

similarity = image_features @ text_features.T               # [1, 1000]
predicted_class = similarity.argmax(dim=-1).item()
```

### 为什么这样能 work？

回到 CLIP 训练目标：**让 $(\mathbf{I}_i, \mathbf{T}_i)$ 配对的相似度高、与其他文本相似度低**。

经过 4 亿对训练，CLIP 的图像表征空间和文本表征空间**对齐**了——在共享空间里：

- 一张猫的图，它的 $\mathbf{I}$ 向量会**靠近**所有描述猫的句子（"a cat"、"a kitten"、"a tabby cat"）的 $\mathbf{T}$ 向量
- 它会**远离**所有不描述猫的句子（"a car"、"a bridge"）

所以测试时，给 1000 个候选类名，最匹配的类名就是这张图的预测类别。

> 🎯 **零样本的本质**：
>
> CLIP 没在 ImageNet 上学过，但它学过"猫"这个概念（因为 4 亿对里大量出现）。
> 我们不需要"教它 ImageNet 类别"，只需要"问它：这张图最像哪个候选描述？"

### 这件事为什么以前做不到？

监督学习时代，"分类器"和"类别集合"是绑死的——ResNet-50 在 ImageNet 上训完，最后一层是 1000 维 softmax，**只能输出这 1000 类**。换数据集就要换最后一层，然后用新数据集重新训。

CLIP 把"分类器"和"类别"**解耦**了：
- 视觉部分：image encoder 输出语义嵌入
- 类别部分：text encoder 把任意类名变成嵌入

→ **新增类别只需要给类名，不需要任何训练数据。** 这就是"开放词表"的真正含义。

---

## 三、Prompt Engineering：被严重低估的细节

### 一个反直觉的发现

CLIP 论文 Section 3.1.4 实验：在 ImageNet 上做零样本分类，**用什么 prompt 决定了 5-10 个百分点的精度差**。

| Prompt 形式 | Top-1 |
|---|---|
| `"{class}"`（裸类名） | 67.1% |
| `"a photo of a {class}"` | **76.2%** |
| `"a photo of a {class}, a type of pet."`（领域提示） | 80%+（在 OxfordPets 上） |

**裸类名 vs "a photo of"**：差 9 个百分点。

### 为什么会这样？

回想 CLIP 的训练数据：4 亿对来自互联网的"图 + 文"。这些文本**绝大多数是完整的句子**：

- "A golden retriever playing in the park."
- "Photo of a beautiful sunset over the Pacific."
- "An old steam locomotive at the station."

模型从来没见过单独的、孤立的词（"goldfish"）作为完整文本输入。所以测试时给它 `"goldfish"`，它会用"我训练时见过的孤立词"的分布来理解——这种分布**罕见且偏**，效果差。

而 `"a photo of a goldfish"` 是一个**像训练分布的句子**。模型立刻进入"识别图片描述"模式，效果好得多。

> 🎯 **Prompt engineering 的本质**：
>
> 让推理时输入的格式**逼近训练数据的分布**。
>
> 对 CLIP，这意味着用完整句子；对 LLM，这意味着用对话格式或指令格式。

### Prompt Templates 与 Prompt Ensemble

CLIP 论文实测发现某些数据集需要特定模板：

| 数据集 | 推荐 prompt |
|---|---|
| OxfordPets | `"a photo of a {class}, a type of pet."` |
| Food101 | `"a photo of {class}, a type of food."` |
| EuroSAT | `"a centered satellite photo of {class}."` |
| RESISC45 | `"satellite imagery of {class}."` |

**Prompt Ensemble**：同一个类名用多个 prompt 编码，平均得到的文本向量当作类别向量：

```python
templates = [
    "a photo of a {class}.",
    "a blurry photo of a {class}.",
    "a black and white photo of a {class}.",
    "a low contrast photo of a {class}.",
    "a high contrast photo of a {class}.",
    "a bad photo of a {class}.",
    "a good photo of a {class}.",
    # ... 80 个模板
]

class_features = []
for c in class_names:
    prompts = [t.format(c) for t in templates]
    feats = encode_text(prompts).mean(dim=0)   # 平均
    feats = F.normalize(feats, dim=-1)
    class_features.append(feats)
```

CLIP 用 **80 个 templates** 的 ensemble，又涨 1-2 个点。

### 这件事为什么重要

Prompt engineering 不是工程细节——它揭示了 CLIP 的一个深刻局限：

> **CLIP 学到的不是"概念"，而是"概念在它见过的文本分布里的样子"。**
>
> 你必须用 CLIP 训练分布喜欢的语言风格 prompt，才能激活它学到的知识。

这点会在 LLaVA 那里再次出现——LLM 的"指令跟随"能力同样要求"指令格式贴近训练分布"。

---

## 四、CLIP 的应用全景

CLIP 不只是分类器，它是一个**通用的"图文相似度判别器"**。这催生了一整代应用：

### 应用 1：跨模态检索

- **文找图**：在 1 亿张图的库里找"a sunset over Mount Fuji"
- **图找文**：给一张图，从库里找最匹配的描述
- **以图搜图**：把图编码成向量，做最近邻

工业界部署：Pinterest、TikTok 等用 CLIP 做视觉搜索的核心组件。

### 应用 2：CLIP-Guided 生成

把 CLIP 当成"美学评判官"，引导生成模型：

- **CLIP-Guided Diffusion**：扩散模型每步生成时，用 CLIP 评估"当前图像和目标 prompt 有多像"，把这个相似度的梯度加到 diffusion 的 score 上。
- **DALL·E 1（2021）**：生成大量候选图，用 CLIP 排序，选最匹配的。
- **Stable Diffusion** 用 CLIP-ViT-L 的 text encoder 作为文本条件输入（cross-attention 的 key/value 来源）。

→ **没有 CLIP，就没有今天的文生图。**

### 应用 3：图像聚类与数据集分析

- 把一个数据集的所有图编码成 CLIP 嵌入
- 用 K-means 或 UMAP 聚类
- 类内是"语义相似"的图——这种聚类比传统视觉特征聚类（颜色直方图、HOG）有意义得多

LAION 数据集的去重、毒性过滤都用 CLIP。

### 应用 4：作为下游 VLM 的视觉编码器

这是和我们这门课最相关的应用：

- BLIP-2、LLaVA、MiniGPT-4、InternVL、Qwen-VL...
- **它们的视觉编码器全是 CLIP-ViT**（通常用 ViT-L/14 或 ViT-bigG）

为什么？因为 CLIP 的图像表征**已经和语言对齐**——后续接 LLM 时，桥接难度大大降低。

我们第 7 章会看到 LLaVA 是怎么利用这一点的。

### 应用 5：弱监督下的细粒度任务

- **零样本目标检测**（OWL-ViT, GLIP）：把"找出图里所有 'cat'" 转化为"图里哪些 region 的 CLIP 特征和 'cat' 文本特征最相似"
- **零样本分割**（Segment Anything + CLIP）

---

## 五、CLIP 的能力边界

CLIP 不是万能的。论文 Section 5 列了它的几大短板：

### 短板 1：细粒度识别

| 任务 | CLIP zero-shot |
|---|---|
| 识别"猫"（粗粒度） | 95%+ |
| 识别"金毛 vs 拉布拉多 vs 拉布拉多金毛混血"（细粒度） | 大幅下降 |
| 识别 200 种鸟（CUB-200） | 远低于专业模型 |
| 识别 102 种花（Oxford Flowers） | 表现一般 |

**原因**：互联网爬来的文本描述大多是粗粒度的（"a dog"、"a bird"），细粒度类别（具体品种）的训练样本少。

### 短板 2：抽象 / 系统性任务

CLIP 在以下任务表现差：
- **MNIST**（手写数字识别）：仅 57%——因为训练数据里几乎没有"手写数字"
- **CLEVR**（合成物体计数）：差——CLIP 不会数数
- **DMLab**（迷宫导航）：差——和视觉概念无关的任务

**原因**：CLIP 学到的是"自然语言中描述图像的方式"，对**抽象推理**（计数、比较、空间关系）无能为力。

### 短板 3：文本中的复杂结构

CLIP 不擅长理解：

- **空间关系**："a cat to the LEFT of a dog" vs "a cat to the RIGHT of a dog" → CLIP 几乎区分不开
- **属性绑定**："a red cube and a blue sphere" vs "a blue cube and a red sphere" → 经常搞混
- **否定**："a photo NOT containing a cat" → 处理失败

**原因**：CLIP 的文本编码器只学到了"词袋"（bag-of-words）级别的图文匹配，结构语义弱。

### 短板 4：分布外（OOD）数据

CLIP 在自然图像上极强，但在以下数据上崩溃：

- **医学影像**（X-ray, MRI, CT）：训练数据里没有
- **遥感**（卫星、航拍）：偏离自然视角
- **手绘 / 草图**：风格偏移

→ 这些领域需要重新训 domain-specific CLIP（如 BiomedCLIP）。

### 短板 5：社会偏见

CLIP 复刻了互联网文本的偏见：
- 性别 / 种族 stereotyping（"doctor"→ 男性图，"nurse"→ 女性图）
- 西方中心（"wedding" → 白色婚纱，不会想到中式婚礼）

OpenAI 在论文 Section 7 长篇讨论了这些问题。

---

## 六、本章一句话总结

> 🎓 **CLIP = 4 亿图文对 + 双塔 + 对称 InfoNCE → 在共享语义空间里把图和文对齐 → 零样本分类、检索、生成的统一基础。**
>
> 它的强：开放词表、零样本、跨模态。
> 它的弱：细粒度、空间结构、抽象推理、专业领域。
>
> 这些"弱"正是后续 BLIP / LLaVA 要解决的问题。

---

## 七、为下一章铺路

到这里 CLIP 主线讲完。但 CLIP 有个**致命短板**没在论文里说：

> **CLIP 只能"判别"，不能"生成"。**
>
> - 给一张图 + 候选文本：CLIP 能告诉你哪个最匹配 ✅
> - 给一张图：CLIP 不能告诉你"图里有什么" ❌
> - 给一张图 + 一句问题：CLIP 不能回答 ❌

为什么？因为 CLIP 的两个 encoder 学的是**对齐**，不是**生成**。文本 encoder 把"a photo of a cat"压成一个向量，然后扔了——它不知道怎么从向量"反向"生成文本。

→ 第 6 章我们看 **VLM 三种范式**怎么解决这个问题：
- **双编码器派**（CLIP, ALIGN, SigLIP）—— 强检索，弱生成
- **编解码器派**（BLIP, BLIP-2, CoCa）—— 引入生成头
- **LLM-based 派**（Flamingo, LLaVA）—— 把视觉特征接到现成的 LLM

LLaVA 走的是第三条路——也是当前最强的对话型 VLM 路线。

---

## ✅ 课后检查

### Q1（必答 · 理解题）
"CLIP 的零样本能力" 到底"零"在哪？为什么以前的监督模型做不到？

### Q2（必答 · 应用题）
你想用 CLIP 在自定义数据集上做"开心的猫 vs 不开心的猫"二分类。你怎么设计 prompt？给至少 3 种方案。

### Q3（必答 · 边界题）
为什么 CLIP 在 MNIST（手写数字）上仅 57%？这反映了 CLIP 的什么本质局限？

### Q4（选答 · 综合题）
回顾全章，CLIP 的"魔法"由哪两个因素决定？如果只用 1500 万对数据训 CLIP，零样本能力会保留吗？为什么？

---

## 📝 我的回答（你来填）

> Q1:
>
> Q2:
>
> Q3:
>
> Q4:

## 🤔 我的疑问（你来填）

> -
> -

---

## 📋 参考答案

<details>
<summary>点开看 Q1 参考</summary>

**"零"在哪**：

CLIP 在目标分类任务上**完全没有训练过**——没见过这个数据集的图、没见过这个数据集的标签集合、没微调过任何参数。从 ImageNet → Stanford Cars → CIFAR-100 → OxfordPets，27 个数据集都是同一份模型权重直接评估。

**以前监督模型做不到的原因**：

监督学习的"分类器"和"类别集合"绑死。ResNet-50 最后一层是 `Linear(2048, 1000)`，只能输出 ImageNet 1000 类。换到 Cars 数据集（196 类），必须：

1. 把最后一层换成 `Linear(2048, 196)`
2. 重新训练（至少 fine-tune）
3. 需要 Cars 数据集的标注数据

CLIP 的范式根本不需要这些步骤。"分类"被重新定义为"在图像表征空间里找最近的文本表征"——而新增类别只需要给类名（一句话），不需要任何训练。

→ **这是"封闭词表"到"开放词表"的范式转变**。
</details>

<details>
<summary>点开看 Q2 参考</summary>

3 种 prompt 方案：

**方案 1：直接对比**
```python
prompts = [
    "a photo of a happy cat",
    "a photo of a sad cat",
]
```

**方案 2：加领域提示**
```python
prompts = [
    "a photo of a happy cat, smiling and playful",
    "a photo of an unhappy cat, looking grumpy or scared",
]
```

**方案 3：Prompt Ensemble（多模板平均）**
```python
templates_happy = [
    "a happy cat", "a smiling cat", "a playful cat",
    "a cat looking joyful", "a content cat purring",
]
templates_sad = [
    "an unhappy cat", "a grumpy cat", "a scared cat",
    "a cat looking miserable", "an angry cat hissing",
]
# 每个类别用模板平均文本向量
```

**实战经验**：

- 方案 2 通常比方案 1 涨 3-5 个点（因为"happy/sad"本身在 CLIP 训练分布里出现频率低，加上"smiling/playful"等具体描述能激活更准确的视觉特征）。
- 方案 3 需要更多调试，但上限最高。

**如果效果还是不好**——这可能反映 CLIP 的局限：**情绪识别不是 CLIP 的强项**（互联网图文对里很少标注猫的情绪）。这种情况下只能用**少样本微调**（CLIP-Adapter, CoOp 等技术）。
</details>

<details>
<summary>点开看 Q3 参考</summary>

**为什么 MNIST 仅 57%**：

CLIP 训练数据是互联网爬取的"自然图像 + 描述"。互联网上几乎不存在"手写阿拉伯数字 0-9"的孤立图像 + caption。所以 CLIP 没学到"如何把手写体数字 → 数字概念"的映射。

更深层原因：

1. **MNIST 是合成 / 预处理过的数据**（黑底白字、28×28），与"自然摄影图像"分布完全不同
2. **手写数字的语义** = "这是数字 7" 这种抽象映射，需要的不是视觉相似度，而是**字符识别能力**——而 CLIP 没接受过 OCR 任务训练

**反映了什么本质局限**：

CLIP 学到的是"**自然语言中描述图像的方式**"——它的视觉概念集合 = 互联网图文对里出现频率高的概念。

任何分布外的领域都会失败：
- 手写体（MNIST）
- 医学影像（X-ray）
- 遥感图像
- 工业检测图像
- 抽象示意图、UI 截图

→ 这些领域要么需要 domain-specific CLIP（如 BiomedCLIP），要么需要少量标注数据做 fine-tune。

**这给我们的启示**：CLIP 的"零样本"是相对**自然世界常见概念**的零样本，不是真正的"任意概念零样本"。
</details>

<details>
<summary>点开看 Q4 参考</summary>

**CLIP 魔法的两个核心因素**：

1. **数据规模**（4 亿对）
2. **数据多样性**（覆盖互联网全域）

两者缺一不可。论文 Figure 9 给的数据：

| 数据规模 | ImageNet zero-shot |
|---|---|
| 1500 万 | 11% |
| 1 亿 | ~50%（推测） |
| 4 亿 | 76% |

**1500 万对训出来的 CLIP 几乎没有零样本能力**——只比瞎猜（0.1%）高 100 倍，但完全不可用。

**为什么会这样？**

零样本能力的本质是 **"模型见过这个概念的足够多变化形式"**。
- "猫" 这个概念在 1500 万对里可能出现 3 万次 → 不够覆盖所有视角、姿势、品种、场景
- 在 4 亿对里出现 80 万次 → 足以覆盖

**对 ImageNet 1000 类**，每个类需要至少几万次出现才能学到稳定表征——这要求总数据规模到亿级。

**对长尾类别**（"草莓奶昔"、"霓虹灯招牌"），每类可能只在大数据集里出现几千次——所以 4 亿是当时大家公认的"最低有效门槛"。

**这给我们的启示**：

1. **不要试图在小规模上复现 CLIP** —— 没有这个数据规模，零样本能力出不来。
2. **想训自己的 CLIP，至少 LAION-400M 起步**——这是开源社区能找到的最大公开图文数据集。
3. **CLIP 的成功是 OpenAI "data + compute + 朴素方法" 哲学的胜利**——这个哲学后来在 GPT-4、Sora 上一再印证。
</details>

---

**下一课预告**：

➡️ [`06-VLM三种范式全景.md`](./06-VLM三种范式全景.md)

CLIP 主线收官。第 6 章我们站到更高的视角，看整个 VLM 领域的**三大范式**：

1. **双编码器派**（CLIP / ALIGN / SigLIP）：强检索、弱生成
2. **编解码器派**（BLIP / BLIP-2 / CoCa）：加生成头，引入 **Q-Former** 这一关键设计
3. **LLM-based 派**（Flamingo / LLaVA / MiniGPT-4）：把视觉接到现成 LLM，撬动其推理能力

第 6 章读完，你会**俯瞰整个 VLM 领域**——再看到一篇新模型论文，能秒判断它属于哪个流派、强在哪、弱在哪。
