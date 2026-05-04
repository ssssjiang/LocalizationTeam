# 扫地机具身新项目调研 doc — Brainstorming Checkpoint

> **状态**：brainstorming 进行中，本次会话因 form factor 未定中断。下次讨论时直接读本 doc 接续。
>
> **trigger 原话**（2026-05-04）：
> > 我们调研的目的，其实是给我们扫地机公司的，具身新项目一些启发 & 方向上的指导，以及希望了解行业技术的现状，以及我们可以考虑什么样的方案，用什么样的计算资源；当然从 CNN 说起，是为了掌握发展的脉络，不会悬浮。

## 1. 真实需求识别

现有产出 `projects/personal-ai-talk-2026-04-24/08-knowledge-doc.md` 是 **AI 演进笔记**（2012-2026 客观 record），但 user 真实需要的是 **扫地机具身新项目调研结论**——两类产出目的不同：

| 维度 | 现 doc（08-knowledge-doc.md）| 待写新 doc |
| --- | --- | --- |
| 目的 | 技术演进客观 record | 给具身新项目的 启发 / 方向 / 资源选型 |
| reader 视角 | 任意技术读者 | 内部技术团队 |
| 输出形式 | 演进时间线 + 客观陈述 | 现状地图 + 候选方案 + decision support |
| 风格 | 不下判断 | 必须有 implication / 推荐 / trade-off（基于客观证据 derive）|
| 计算资源 | 不涉及 | 端侧 SoC / 云端训练 / 推理 latency 必须明确 |

现 doc 不动（保持 self-contained 演进 reference 价值），新 doc 引用 §4.X 而不重复演进细节。

## 2. 已确认决定

| ID | 决定 | 选择 | 备注 |
| --- | --- | --- | --- |
| Q1 | scope / 产出形式 | **B：单独新 doc** | `09-sweeper-embodied-roadmap.md`（~8-12K 字）；现 doc 不改 |
| Q2 | reader 视角 | **B：内部技术团队** | 定位 / 算法同事；平等技术语言；可有 hypothesis 但要标注 |

## 3. 待决问题

### 3.1 Q3：具身新项目的目标形态（核心 — 决定整个方案空间）

| 选项 | 描述 | 影响 |
| --- | --- | --- |
| A | 现有扫地 / 割草机 + VLM 增强（语言交互 / 物体识别 / 用户指令理解，不动机械臂）| VLM 端侧推理 + 现有 SLAM stack；改动最小，落地最快 |
| B | 轮式 + 单臂 / 抓取（拾取地面玩具 / 衣物 / 垃圾，半具身）| 引入抓取 RL / VLA-pick-and-place；硬件改动大 |
| C | 轮式 / 足式 + 双臂 / 上半身（家居整理 / 厨房任务）| 全 VLA；与 GR00T / Helix 对标 |
| D | 全仿人（与 Figure / GR00T 对标）| 远超公司现有能力；需大幅扩团队 |
| E | SLAM + Foundation model 平台（多 form factor 共享底层：扫地 / 割草 / 仿人）| 平台型路线；研发周期长但复用度高 |
| F | 还在德尔菲中 / 多条都可能 | 可能并行 |

**user 当前态度**：还没想好，待下次讨论决定。

### 3.2 Q4：算力 / 硬件平台预算（未问）

候选方向：
- 端侧 SoC：高通 RB5 / RB6、地平线 J5/J6、瑞芯微 RK3588 / RK3576、NVIDIA Jetson Orin（NX / AGX）、海思
- TOPS 预算：≤8 TOPS（轻量 CV）/ 8-30 TOPS（小型 VLM）/ 30-275 TOPS（VLA / 大模型推理）
- 功耗 / 散热 / BOM cost 约束
- 是否允许云端协同（mobile robot + cloud inference）

### 3.3 Q5：时间节点（未问）

- 短期 demo（3-6 月）
- 中期 product（1-2 年）
- 长期 platform（3+ 年）
- 是否对标某个具体的展会 / 发布节点

### 3.4 Q6：团队能力 gap（未问）

已知：user 是 SLAM / 定位建图算法工程师；公司有扫地 / 割草机量产 SLAM 能力。

待确认：
- 是否已有 VLM / 多模态团队
- 是否已有 RL / 模仿学习 / VLA 团队
- 是否已有抓取 / 操作 / dexterous manipulation 团队
- 数据采集能力（家居场景遥操作 / 仿真 sim2real）

## 4. 候选 doc 设计（待 Q3-Q6 决定后填充）

### 4.1 章节大纲

`09-sweeper-embodied-roadmap.md` 草拟章节（~8-12K 字）：

1. **§1 行业技术现状地图**（基于 08-knowledge-doc.md 抽象，加"成熟度 / 工业可用性"标签）
   - VLM / VLA / World Models / 重建侧 当前 state-of-the-art
   - 哪些已工业化（量产）/ demo / 仅实验室
   - 国内外厂商 cover 矩阵
2. **§2 候选技术方案**（针对 Q3 选定的 form factor）
   - 3-4 条候选路线 × trade-off 矩阵
   - 每条路线：所需模型 / 数据 / 算法 / 硬件 / 风险
3. **§3 计算资源选型**
   - 端侧 SoC 候选 + TOPS / 功耗 / BOM 矩阵
   - 云端训练资源（GPU 数 / 时长 / cost）
   - 推理 latency budget（real-time control loop / 长 horizon planning）
4. **§4 团队能力 gap + 可行性评估**
   - 现有能力 vs 需要能力 → 缺口清单
   - 招聘 / 外包 / 合作 / 学术 三选一
5. **§5 路线图建议**
   - 短期 / 中期 / 长期 milestone
   - 优先级 + risk

### 4.2 命名与引用

- 路径：`projects/personal-ai-talk-2026-04-24/09-sweeper-embodied-roadmap.md`
- 现 doc（08-knowledge-doc.md）作为 reference，新 doc 用脚注 / inline 引用现 doc 的 §X.Y

## 5. 接续 instruction

下次 session 开场直接：

1. 读本 doc（你现在看的这份）
2. 用户回答 Q3（form factor 选项 A-F + 可补充 hypothesis）
3. 顺序问 Q4 / Q5 / Q6
4. 进入 doc 大纲 fill-in 阶段
5. 落盘 final spec 至 `projects/personal-ai-talk-2026-04-24/specs/2026-05-04-sweeper-embodied-roadmap-design.md`
6. 进入 implementation（writing-plans 或直接写 doc）
