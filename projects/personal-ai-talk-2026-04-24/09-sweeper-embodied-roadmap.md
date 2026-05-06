# 扫地机具身新项目调研路线图

> **状态**：第一稿 §1-§3 骨架（2026-05-05）；§4-§8 待第二轮起草。
>
> **关联 doc**：
>
> - `specs/2026-05-04-sweeper-embodied-roadmap-design.md`（设计 spec，12 决定 + G1-G5 修订）
> - `specs/2026-05-04-sweeper-embodied-roadmap-brainstorm-checkpoint.md`（brainstorm 历史）
> - `08-knowledge-doc.md`（AI 演进笔记，技术 reference 锚点）
> - `specs/08-drift-staging-for-09.md`（行业 frontier raw material）

---

## 1. 摘要 / 战略结论

公司具身新项目以 **wheel-legged biped + 1 arm**（双足轮足混合 base + 单臂，可蹲伏扫地、可站立爬楼或抓物）为 3+ 年 north star，分三阶段推进：

- **Phase 1**（2026-05 ~ 2027-Q4，13-15 月）：复用现有扫地机轮式 base + 加单臂，完成 **language-grounded pickup-and-place**——拾取地面散落物（袜子 / 玩具 / 充电线）+ 物品归位（按用户指令送指定家具）+ 垃圾分类（投分类垃圾桶）三 task 共享 capability bundle
- **Phase 2**（~12-15 月）：加 lift 机构延伸到桌面 / 沙发物体抓取
- **Phase 3**（~30-48 月）：进入 full wheel-legged biped 含爬楼

Phase 1 关键 commit：


| 维度           | Commit                                                                                                                                                                                |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **形态**       | 现有扫地机 base + 1 arm；BOM target ¥6000-8000（NX 量产）/ ¥9000-11000（AGX fallback）                                                                                                            |
| **算法 base**  | fork **NVIDIA GR00T N1.7**（3B Cosmos-Reason2-2B + 32-layer Diffusion Transformer，NVIDIA Open Model License）[1]；M0 parallel benchmark + M3 trigger 评估，threshold 触发 OpenVLA fallback[2] |
| **数据**       | 三栈 combined：web video pretrain (EgoScale-style)[1] + Isaac Sim + Cosmos Transfer[3] + AgiBot World 100 万 demo[4] + Open X-Embodiment[5] + 真机 5-10 万 episode                           |
| **算力**       | dev/pilot Orin AGX 275 TOPS → 量产 Orin NX 100 TOPS（M5-M6 trigger 评估，failover AGX 量产）；GPU cluster hybrid（dev 云租 + pretrain 自购 16×H100）                                                  |
| **团队**       | 三层 model — 核心 ML/VLA + sim 5-8 人新招 + 公司既有 ME/EE / ML infra / product 5-8 FTE × ⅓ 复用 + teleop 操作员 16-20 人外包；学术合作补 sim2real / VLM grounding 关键模块                                        |
| **deadline** | demo 锚 **WAIC 2027-07** + 量产首发锚 **IFA 2027-09 / 双 11 2027-11**（buffer 1-5 月）                                                                                                          |
| **总投资**      | baseline **¥3000-5500 万**                                                                                                                                                             |


**行业战略判断**（基于公开 release，截至 2026-05-04）：VLA frontier (RT-2 / π₀ / GR00T / Helix / GraspVLA) 已 reach pilot 与有限量产阶段[1, 2, 6, 7, 8]，2026-2027 间是消费级具身落地窗口；扫地机公司具备 SLAM + 量产硬件 + 渠道三项 leverage，与 Physical Intelligence / Figure 类纯具身公司相比，在 distribution 与 cost-down 上有结构性优势。



### References

- [1] NVIDIA, GR00T N1.7: Action Cascade and EgoScale, huggingface.co/blog/nvidia/gr00t-n1-7 2026-04-17.
- [2] Stanford OpenVLA team, OpenVLA: An Open-Source Vision-Language-Action Model, arXiv 2024-06. arXiv:2406.09246
- [3] NVIDIA, Cosmos World Foundation Models, developer.nvidia.com/cosmos 2025-01 (CES).
- [4] AgiBot, GO-1 + AgiBot World 数据集 release, agibot.com 2025-03-10.
- [5] Open X-Embodiment Collaboration, Open X-Embodiment: Robotic Learning Datasets and RT-X Models, robotics-transformer-x.github.io 2023-10.
- [6] Physical Intelligence, π₀.5 release, physicalintelligence.company/blog/pi05 2025-04-22.
- [7] Figure AI, Helix 02 release, figure.ai/news/helix 2026-01.
- [8] 银河通用, GraspVLA + 七大泛化金标准, 银河通用 blog 2025-01-09.

---

## 2. 行业技术现状地图

具身新项目相关技术栈分 3 个 capability layer：**VLA**（具身决策层 / 输出 action）、**World Models**（仿真训练层 / sim-to-real）、**几何重建**（感知层 / 与 SLAM 对接）。本节按层级展开 frontier 厂商 + mature 度，章末用跨层矩阵 wrap-up。

时间锚点：截至 **2026-05-04**。

### 2.1 VLA frontier（具身决策层）

VLA (Vision-Language-Action) 把视觉 + 语言 model 输出端从 token 改为 action，直接输出机器人执行序列。frontier 由国际四主线 + 国内三家驱动；Phase 1 fork base 选 GR00T N1.7。

#### 2.1.1 国际线

国际 VLA 主线四条：Google DeepMind RT-2 → Physical Intelligence π 系列 → Figure AI Helix → NVIDIA GR00T。截至 2026-05-04 主流 release：


| Model      | 公司                    | Release    | Robot 形态             | 训练数据                           | 关键贡献                                                      |
| ---------- | --------------------- | ---------- | -------------------- | ------------------------------ | --------------------------------------------------------- |
| RT-2       | Google DeepMind       | 2023-07    | dual-arm RT robot    | web-scale + RT-1               | VLM 直接转 VLA 的首个工业级工作[1]                                   |
| π₀         | Physical Intelligence | 2024-10    | 7 个 embodiment       | ~10k hrs 真机                    | generalist policy 跨形态[2]                                  |
| π₀.5       | Physical Intelligence | 2025-04-22 | + open-world         | + open-world data              | open-world generalization[3]                              |
| π₀.7       | Physical Intelligence | 2026-04-16 | steerable foundation | scaled                         | step-change in generalization[4]                          |
| Helix 02   | Figure AI             | 2026-01    | Figure 02 humanoid   | full-body                      | 单一神经网络（10M 参数）替代 109,504 行 C++；4 分钟洗碗机连续自主[5]             |
| GR00T N1   | NVIDIA                | 2025-03    | humanoid (open)      | open + sim                     | 首个开源 humanoid foundation[6]                               |
| GR00T N1.7 | NVIDIA                | 2026-04-17 | humanoid             | EgoScale 20,854 hrs egocentric | Action Cascade dual-system + dexterity scaling law 首报告[7] |


数据点：GR00T N1.7 公开报告中提出 robot dexterity scaling law（1k → 20k hrs 训练数据 → dexterity 表现 doubling），是 VLA 领域第一次报告 scaling law 现象[7]。

详细架构与 8 doc §7.1.1 对齐（完整时间线 / 每 model 设计点 / fork license）。

#### 2.1.2 国内线

国内 VLA 主线三家：银河通用 GraspVLA / 智元 GO-1 / 宇树 UnifoLM-VLA-0：


| Model         | 公司   | Release    | Robot 形态    | 训练数据                             | 开源 / 闭源                   |
| ------------- | ---- | ---------- | ----------- | -------------------------------- | ------------------------- |
| GraspVLA      | 银河通用 | 2025-01-09 | Galbot 上半身  | 10 亿帧合成 + 真机                     | 闭源；七大泛化金标准[8]             |
| AgiBot GO-1   | 智元   | 2025-03-10 | 多形态         | AgiBot World 100 万 demo / 217 任务 | model 闭源 + **数据集开源**      |
| UnifoLM-VLA-0 | 宇树   | 2026-01-29 | G1 humanoid | 真机 + sim                         | **开源**；基于阿里 Qwen2.5-VL-7B |


国内线对 Phase 1 的实际意义：

- **AgiBot World 100 万 demo / 217 任务公开数据集** 是 Phase 1 数据三栈中"公开数据集"主力源之一，与 GR00T N1.7 fork 直接组合可用
- GraspVLA 七大泛化金标准（光照 / 背景 / 平面位置 / 空间高度 / 动作策略 / 动态干扰 / 物体类别）可直接作为 Phase 1 自有真机数据采集的覆盖维度 spec[8]
- UnifoLM-VLA-0 验证国产 VLM (Qwen2.5-VL) 可作 VLA backbone，Phase 2 国产 SoC 迁移时是 reference

### 2.2 World Models 工具链（仿真训练层）

World Models 给 VLA 提供 sim training playground / sim-to-real 数据增强 / reasoning 子模块。两大主线：DeepMind Genie（consumer 向）+ NVIDIA Cosmos（physical AI / robot industry 向）。Phase 1 重点用 **Cosmos Transfer**（sim-to-real data augmentation）+ **Cosmos-Reason2-2B**（GR00T N1.7 内置 VLM grounding）。

#### 2.2.1 DeepMind Genie 系列

主线 Genie 1 (ICML 2024) → Genie 2 (2024-12) → Genie 3 (2025-08-05) → Project Genie (2026-01-29)[9]。Genie 3 在 720p / 24 fps real-time interactive 下保持几分钟级一致性，是 World Models 公众级 demo 的标志[9]。

对 Phase 1 的实际意义：**间接**——Genie 闭源、暂无 sim 引擎绑定，主要作为 paradigm reference；不进入 Phase 1 工具链。

#### 2.2.2 NVIDIA Cosmos

Cosmos (2025-01 起) 是 physical AI 的 world model 工具链，与 NVIDIA Isaac Sim / GR00T humanoid foundation 配套形成 stack。3 个子族 (2025-2026)[3, 10]：

- **Cosmos Predict (Predict 2.5, 2026-04)**：flow-based world prediction；统一接口（text-to-world / image-to-world / video-to-world）
- **Cosmos Transfer (Transfer 2.5, 2026-04)**：multi-controlnet 可控生成；用于 sim-to-real data augmentation（sim renderer 输出 → diffusion 改造为 real-distribution）
- **Cosmos Reason (Reason 2, 2026-04)**：VLM 增强 spatial-temporal 理解的 reasoning model；GR00T N1.6 / N1.7 直接用 Reason2-2B 作为 System 2 backbone[7]

Cosmos 工具链定位为 NVIDIA "physical AI stack" 的 foundation 层（Foundation models + Isaac Sim + GR00T humanoid + Jetson 硬件）[10]。

对 Phase 1 的实际意义：**核心**——Cosmos Transfer 直接进入 Phase 1 数据栈（sim-to-real）；Cosmos-Reason2-2B 已内置在 fork base GR00T N1.7 中。

### 2.3 几何重建（感知层 / 与 SLAM 对接）

几何重建近期工作沿两条路线：3DGS 系列（real-time render）+ feed-forward Transformer 大模型化（DUSt3R / VGGT）。这是公司现有 SLAM / 定位建图能力的直接外延，是 Phase 1-3 的 leverage 点。

#### 2.3.1 3DGS / 4DGS

3DGS (Kerbl et al., SIGGRAPH 2023)[11] 把 3D 场景表示为 explicit 3D Gaussians（位置 / 协方差 / 颜色 / opacity），可微分 splatting 渲染。1080p 100+ fps real-time render；训练几分钟达到 Mip-NeRF360 PSNR。后续 4DGS（含时间维，CVPR 2024）/ Deformable GS / SuperSplat / GS-LRM (ECCV 2024)[12] 把训练 feed-forward 大模型化，去除 SfM 初始化 + per-scene optimization。

对 Phase 1-3 的实际意义：**Phase 2-3 中度**——用于 sim 场景重建 + visual servo backend；Phase 1 不直接进入 critical path。

#### 2.3.2 DUSt3R / VGGT

DUSt3R (Wang et al., CVPR 2024)[13] / MASt3R (Leroy et al., ECCV 2024)[14] 把 3D 重建从 SfM + MVS + BA 多阶段 pipeline 改为单 Transformer feed-forward。VGGT (Wang et al., CVPR 2025)[15] 进一步把 SfM / MVS 整合为单一大型 feed-forward Transformer，1 秒级 inference 同时输出 camera params + per-pixel depth + 3D point cloud + tracking。

对 Phase 1-3 的实际意义：**Phase 2 中-高度**——可作为 SLAM front-end / map 初始化；与公司现有 SLAM stack 的对接 demo 可在 Phase 1 末期 (M6 cost-down) 时启动评估。

**跨层 × 跨厂商 cover 矩阵**（§2 wrap-up，不开三级标题以避免 §2 sibling 超 3）：


| Layer                 | 国际 frontier               | 国内 frontier               | mature 度       | Phase 1 进入工具链                      |
| --------------------- | ------------------------- | ------------------------- | -------------- | ---------------------------------- |
| **VLA**（决策层）          | π₀ / GR00T / Helix / RT-2 | GraspVLA / GO-1 / UnifoLM | pilot + 有限量产   | ✅ fork GR00T N1.7（核心）              |
| **World Models**（仿真层） | Genie / Cosmos / V-JEPA   | （国内 frontier 暂未独立产品化）     | demo + tool 阶段 | ✅ Cosmos Transfer + Reason2（核心子组件） |
| **几何重建**（感知层）         | 3DGS / DUSt3R / VGGT      | 智源 / 港大 / 上海 AI Lab 等高校工作 | 学术 + 工业早期      | ⚠️ Phase 2 评估接入                    |


时间锚点：截至 2026-05-04 公开 release 整理；后续 frontier 月度迭代，整理周期 ≤ 1 月。

### References

- [1] Brohan et al., RT-2: Vision-Language-Action Models Transfer Web Knowledge to Robotic Control, arXiv 2023. arXiv:2307.15818
- [2] Black et al. (Physical Intelligence), π₀: A Vision-Language-Action Flow Model for General Robot Control, arXiv 2024. arXiv:2410.24164
- [3] NVIDIA, Cosmos World Foundation Models, developer.nvidia.com/cosmos 2025-01 (CES).
- [4] Physical Intelligence, π₀.7 release, physicalintelligence.company/blog/pi07 2026-04-16.
- [5] Figure AI, Helix 02 release, figure.ai/news/helix 2026-01.
- [6] NVIDIA, GR00T N1 release, developer.nvidia.com 2025-03.
- [7] NVIDIA, GR00T N1.7: Action Cascade and EgoScale, huggingface.co/blog/nvidia/gr00t-n1-7 2026-04-17.
- [8] 银河通用, GraspVLA + 七大泛化金标准, 银河通用 blog 2025-01-09.
- [9] DeepMind, Genie 3: A new frontier for world models, deepmind.google/en/blog/genie-3 2025-08-05.
- [10] NVIDIA, Advancing Physical AI with Cosmos 2.5 + Reason2, developer.nvidia.com/blog 2026-04.
- [11] Kerbl et al., 3D Gaussian Splatting for Real-Time Radiance Field Rendering, SIGGRAPH 2023. arXiv:2308.04079
- [12] Zhang et al., GS-LRM: Large Reconstruction Model for 3D Gaussian Splatting, ECCV 2024. arXiv:2404.19702
- [13] Wang et al., DUSt3R: Geometric 3D Vision Made Easy, CVPR 2024. arXiv:2312.14132
- [14] Leroy et al., Grounding Image Matching in 3D with MASt3R, ECCV 2024. arXiv:2406.09756
- [15] Wang et al., VGGT: Visual Geometry Grounded Transformer, CVPR 2025. arXiv:2503.11651

---

## 3. Phase 路线图

north star = **wheel-legged biped + 1 arm**（双足轮足混合 base + 单臂）：base 蹲伏时是低 profile 扫地，base 站起时可爬楼或抓物。该形态在 2026-05 公开 release 中无 commercial pre-production case（最相近是 ETH Ascento Pro / Disney BDX，均无 manipulation arm），是行业空白 + 消费级痛点的交集。

直接 Phase 1 落地 wheel-legged biped 需要 humanoid biped 平衡控制 + biped ↔ wheeled 模式切换 + arm × biped whole-body coordination 三块公司现状 0 储备的能力，1-2 年内量产不可达。因此分三 phase 渐进：每 phase 在前 phase 量产能力上叠加一项新 capability，每 phase 都直接 ship 量产产品而非纯研发。

### 3.1 Phase 1：轮式 base + 1 arm + language-grounded pickup-and-place

**目标 task**：language-grounded pickup-and-place with multi-target placement——用户语言指令理解 → 视觉 grounding 物体 → 机械臂拾取 → 按指令或类别送达 multi-target placement。三个 product narrative 共享同一 capability bundle：

- **N1 散落物清场**：扫地前自动拾起袜子 / 玩具 / 充电线，放收纳框（单 placement）
- **N2 物品归位**：用户语言指令"把这个放洗衣篮 / 抽屉 / 桌面"（VLM open-vocab grounding，multi-target placement）
- **N3 垃圾分类辅助**：识别垃圾 → 投分类垃圾桶（~4 类，自动判定 / 用户确认）

**关键 capability**：

- mobile base SLAM（公司现有能力 100% 复用）
- single-arm grasp policy（fork GR00T N1.7，新增）
- VLM language grounding（Cosmos-Reason2-2B 内置于 GR00T N1.7，新增）
- multi-target placement（家居家具 / 收纳框 / 垃圾桶 detection + 导航到位）

**form factor & BOM**：

- 现有扫地机轮式 base + 1 arm（蹲伏模式）
- BOM target：¥6000-8000（NX 量产）/ ¥9000-11000（AGX fallback，trigger 失败时切换）
- 整机定位：中高端家居机器人

**时间表**（13-15 月，含 buffer，详 spec §3 milestone）：

- M0-M3 (1-6 月)：团队 + dev kit + 真机 prototype + fork GR00T adaptation pretrain
- M4 (9-10 月累计) WAIC 2027-07 demo target：N1 散落物清场成功率 ≥ 70%
- M5-M6 (11-15 月累计)：multi-task + 语言 grounding + cost-down 评估
- IFA 2027-09 / 双 11 2027-11：量产首发

**risk + fallback**（详 §7.3）：

- GR00T transfer fail (humanoid → wheeled + 1 arm) → M0 parallel benchmark + M3 trigger evaluation → OpenVLA fallback
- NX 量产部署 fail (3B model 量化 INT4 + 蒸馏到 100 TOPS) → M5-M6 trigger → AGX 量产 fallback（高端定位）

### 3.2 Phase 2：+ lift 机构 + 桌面 / 沙发抓取

**目标增量**：桌面 / 沙发等高度物体抓取，覆盖比 Phase 1 更高的 workspace。

**关键新增 capability**：

- **lift 机构**（telescoping / scissor lift，工业 mature；类似 Stretch RE2 / Hello Robot 形态[16]）
- 桌面 / 沙发 specific 训练数据（重新采集 ~5 万 episode）
- model retrain on 扩展 workspace（在 Phase 1 GR00T fork 基础上 incremental fine-tune）

**form factor & BOM**：

- Phase 1 base + lift 机构（垂直行程 ~300-600 mm）
- BOM 增量 ¥800-1500（lift 机构 + 桌面级 sensor）
- 整机定位：~¥7500-10000（NX 量产）

**时间表**（12-15 月）：

- 从 Phase 1 量产首发后启动（2027-11 起）
- M7 lift 机构集成 / M8 桌面 dataset retrain / M9 量产 SoC cost-down 国产替代评估
- 软锚点：双 11 2028 / IFA 2028 量产（2028-Q4）

**Phase 2 leverage Phase 1**：fork base / 数据 pipeline / teleop 工位 / 团队全部继承；新增专属于 lift 形态的训练 + ME / EE 集成工作。

### 3.3 Phase 3：wheel-legged biped + 全 manipulation + stair climb

**目标增量**：达到 north star——wheel-legged biped + arm 形态，可爬楼梯（解决扫地机跨楼层痛点）+ 站立完整 manipulation。

**关键新增 capability**：

- **wheel-legged biped 平衡控制**（whole-body MPC / RL-based locomotion；ETH / BD / Figure 量级团队的核心 IP，公司 0 储备）
- **biped ↔ wheeled 模式切换 policy**（站起 / 蹲下 / stair entry，non-trivial transition control）
- **manipulation arm × biped base whole-body coordination**（站起来后重心高，抓取 reaction force destabilize biped，需 whole-body controller）
- safety certification（消费级家庭楼梯 + 老人 / 儿童触碰防护）

**form factor & BOM**：

- wheel-legged biped + arm；末端可滚动；可蹲扫地、可站爬楼 / 抓物
- BOM 难以早期估算，参考海外 humanoid（Figure / 1X）量产规模 BOM ¥30000+，国内宇树 G1 类形态 ¥13.5k 起；扫地机定位下目标整机 ¥15000-25000
- 整机定位：高端家居机器人

**时间表**（30-48 月，从 Phase 2 量产起算）：

- 软锚点：WAIC 2030 demo / 量产 2031-2032
- M11 biped 团队搭建 (3-6 月，扩 8-12 人 locomotion + whole-body MPC + RL) / M12 wheel-leg 平衡 RL (6-12 月) / M13 transition policy + stair climb (6-12 月) / M14 manipulation × biped coupling (6-12 月) / M15 量产 + safety cert (12 月)

**Phase 3 是 strategic R&D 阶段**，不是 incremental product extension。是否真正进入 Phase 3 视 Phase 1-2 retrospective 后再决策（团队规模 / 量产能力 / 行业窗口三方面）。可能的 alternative：Phase 2 量产后 spin-off 独立公司或与 humanoid 大厂 acqui-hire。

### References

- [16] Hello Robot Inc., Stretch RE2 Specifications, hello-robot.com 2023.

---

## 4. Phase 1 候选技术方案

> 待第二轮起草。骨架见 spec §5：
>
> - 4.1 VLA model fork 选型 + fork chain（M0 parallel benchmark + M3 trigger evaluation；G4）
> - 4.2 数据 pipeline 设计（三栈 combined 落地 + streaming fine-tune）
> - 4.3 端侧推理 stack（Orin AGX / NX + 量化 + 蒸馏 + M5-M6 trigger；G5）
> - 4.4 风险与 fallback 矩阵

## 5. 计算资源选型

> 待第二轮起草。骨架见 spec §5。

## 6. 团队能力 gap + 可行性评估

> 待第二轮起草。骨架见 spec §5；三层 model 落地见 G2。

## 7. 路线图 + Risk

> 待第二轮起草。骨架见 spec §5。

## 8. 开放问题

> 待第二轮起草。

