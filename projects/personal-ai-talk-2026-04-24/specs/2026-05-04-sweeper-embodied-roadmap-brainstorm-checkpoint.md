# 扫地机具身新项目调研 doc — Brainstorming Checkpoint

> **状态**：brainstorm phase 1 完成（12 项 root decision + 5 项 spec grill 修订 G1-G5 closed-loop，2026-05-05）；剩 Q5.2 / Q6.2 / Q6.3 / Q6.4 细化层 open（09 doc 起草中 inline 处理）；spec 已落 `2026-05-04-sweeper-embodied-roadmap-design.md`。
>
> **2026-05-05 spec grill 修订** G1-G5（详 spec §6）：
>
> - G1 milestone 改并行 13-15 月（修 timeline 不一致）
> - G2 团队拆三层 model（核心 + 既有复用 + teleop 外包）
> - G3 加 ¥3000-5500 万 cost breakdown + 预算 scenario
> - G4 GR00T fork chain + M0/M3 trigger + OpenVLA fallback
> - G5 量产 NX trigger evaluation + AGX fallback（高端定位 ¥9000-11000）
>
> **trigger 原话**（2026-05-04）：
>
> > 我们调研的目的，其实是给我们扫地机公司的，具身新项目一些启发 & 方向上的指导，以及希望了解行业技术的现状，以及我们可以考虑什么样的方案，用什么样的计算资源；当然从 CNN 说起，是为了掌握发展的脉络，不会悬浮。

## 1. 真实需求识别

现有产出 `projects/personal-ai-talk-2026-04-24/08-knowledge-doc.md` 是 **AI 演进笔记**（2012-2026 客观 record），但 user 真实需要的是 **扫地机具身新项目调研结论**——两类产出目的不同：

| 维度 | 现 doc（08-knowledge-doc.md） | 待写新 doc |
| --- | --- | --- |
| 目的 | 技术演进客观 record | 给具身新项目的 启发 / 方向 / 资源选型 |
| reader 视角 | 任意技术读者 | 内部技术团队 |
| 输出形式 | 演进时间线 + 客观陈述 | 现状地图 + 候选方案 + decision support |
| 风格 | 不下判断 | 必须有 implication / 推荐 / trade-off（基于客观证据 derive） |
| 计算资源 | 不涉及 | 端侧 SoC / 云端训练 / 推理 latency 必须明确 |

现 doc 不动（保持 self-contained 演进 reference 价值），新 doc 引用 §4.X 而不重复演进细节。

## 2. 已确认决定（2026-05-05 grill 完成 12 项 root）

| ID | 决定 | 选择 | 关键 reasoning |
| --- | --- | --- | --- |
| Q1 | 产出形式 | 单独新 doc | `09-sweeper-embodied-roadmap.md`（~10-15K 字）；现 doc 不改 |
| Q2 | reader 视角 | 内部技术团队 | 平等技术语言；可有 hypothesis 但需标注 |
| Q3 | form factor north star | wheel-legged biped + 1 arm（可蹲扫地、站爬楼 / 抓物） | leverage 现有扫地机 SLAM 蹲伏模式；爬楼 + 抓物组合 cover 主要消费级痛点 |
| Q3.2 | Phase 拆分 | Phase 1 = 轮式 base + 1 arm；Phase 2 = + lift；Phase 3 = full wheel-legged biped | 直接 jump 到 biped 跨度过大；从 wheeled + arm 起步对接 π₀ / GraspVLA mature 路径 |
| Q3.4 | Phase 1 task | language-grounded pickup-and-place with multi-target placement（N1 散落物清场 + N2 物品归位 + N3 垃圾分类） | 三 task 共享 capability stack；reframe 为 "language-grounded pick-and-place"；时间表 push 到 12-18 月 |
| Q4.1 | 推理分配 | 全端侧 | 行业 frontier (GR00T / Helix / π₀ / GraspVLA) 全端侧；家居网络 + 隐私 + 长期 cloud cost 三重 risk |
| Q4.2 | SoC 选型 | dev/pilot Orin AGX 275 TOPS → 量产 Orin NX 100 TOPS → Phase 2 国产 SoC（地平线 J6P / 黑芝麻 A2000 Pro） | AGX 是行业 dev standard；NX 量化后跑 3B VLA 量产 BOM 可承受；国产替代推到 Phase 2 toolchain mature 后 |
| Q4.3a | 数据策略 | D 三栈 combined：web video pretrain (EgoScale-style) + sim (Isaac Sim + Cosmos Transfer) + 公开数据集 (AgiBot World 100 万 demo / Open X-Embodiment) + 真机 5-10 万 episode | 全真机 18-24 月不可达；行业 frontier 默认三栈；π₀ / GR00T / GraspVLA 已 prove |
| Q4.3b | GPU cluster | Hybrid：dev 云租 + pretrain 自购 16×H100（约 ¥1500-2000 万） | dev 阶段不确定性高云租按需；pretrain 进入 stable phase 自购 cluster cost-effective |
| Q4.4 | VLA model fork base | **GR00T N1.7** (NVIDIA Open Model License, 3B Cosmos-Reason2-2B + 32-layer DiT) 主线 + Mobile Aloha teleop pipeline reference + OpenVLA 作 fallback | 2026 dexterity scaling law 唯一报告；NVIDIA toolchain 与 SoC 选型对齐；dual-system 架构直接 fit Phase 1 task |
| Q5.1 | Phase 1 deadline | demo 锚 WAIC 2027-07 + 量产首发锚 IFA 2027-09 / 双 11 2027-11（~21 月含 buffer） | WAIC 国内具身展会主场；IFA / 双 11 消费机器人量产首发经典窗口；vs CES 2027 buffer 足够 |
| Q6.1 | 团队主路线 | B fork 开源 + 5-8 核心团队 + 学术合作 | fork GR00T N1.7 / OpenVLA / AgiBot World / Mobile Aloha 省 6-12 月自研；学术合作补关键模块；与具身大厂合作是战略陷阱 |

**Phase 2 / Phase 3 indicative timeline**（未硬锁）：

- Phase 2: Phase 1 量产 + 12-15 月（约 2028-Q4，双 11 2028 / IFA 2028 量产）
- Phase 3: Phase 2 量产 + 30-48 月（约 2031-2032 量产；WAIC 2030 demo）

## 3. 剩余 open question（09 doc 起草中 inline 处理）

| ID | Topic | 处理 | 重要度 |
| --- | --- | --- | --- |
| Q5.2 | Phase 2 / 3 软锚点细化 | 09 doc §7 inline | 低 |
| Q6.2 | 学术合作具体对象（清华 / 上海 AI Lab / 港大 / Stanford / CMU 等） | 09 doc §6.4 inline | 中 |
| Q6.3 | teleop 数据采集 location / 工位规模 / 操作员 | 09 doc §5.3 inline | 中 |
| Q6.4 | 国产工具链 partner 优先级（地平线 / 黑芝麻 / 阿里 Qwen / Cosmos 国内 team） | 09 doc §6.5 inline | 中 |

## 4. 候选 doc 设计（已落 spec）

最终 09 doc 章节大纲已落到 `2026-05-04-sweeper-embodied-roadmap-design.md` §5；本 checkpoint 不再重复。

### 4.1 命名与引用

- 路径：`projects/personal-ai-talk-2026-04-24/09-sweeper-embodied-roadmap.md`
- 现 doc（08-knowledge-doc.md）作为 reference，新 doc 用脚注 / inline 引用现 doc 的 §X.Y

### 4.2 §1 行业技术现状地图 raw material

08 doc 已经做了一次 grill 决定（详见 08 spec G10），把 "frontier 横扫 / 横向 reference table" 部分（不属于 narrative 主线）从 08 移到了 staging：

- **路径**：`projects/personal-ai-talk-2026-04-24/specs/08-drift-staging-for-09.md`
- **内容**：~4.3K 字，分 3 块——LLM frontier (GPT-5.5 / Gemini 3.1 / Claude 4.7 / Qwen / Kimi / GLM / DeepSeek + Mamba 架构线) / 多模态 LLM frontier (GPT-4o / Qwen Omni / Kimi K2 / GLM-4.6 等) / 几何重建 (3DGS / DUSt3R / VGGT)
- **用途**：09 doc §2 行业技术现状地图的初步 raw material；按 09 章节结构（成熟度 / 工业可用性 / 国内外厂商 cover）重新整理

## 5. 接续 instruction

下一阶段：

1. 写 09 doc 第一稿（§1 摘要 + §2 行业地图 + §3 Phase 路线图 骨架），与用户对齐
2. 起草中 inline 处理 Q5.2 / Q6.2 / Q6.3 / Q6.4 细化层
3. 进入 implementation（writing-plans 或直接写 doc）
