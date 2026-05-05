# 09 doc 设计 spec — 扫地机具身新项目调研路线图

> **状态**：brainstorm phase 1 完成（12 项 root decision + 5 项 spec grill 修订 G1-G5 全部 closed-loop，2026-05-05）；剩 Q5.2 / Q6.2 / Q6.3 / Q6.4 细化层 open（09 doc 起草中 inline 处理）。
>
> **关联 doc**：
>
> - `2026-05-04-sweeper-embodied-roadmap-brainstorm-checkpoint.md`（流程 + 决策历史）
> - `08-drift-staging-for-09.md`（§1 行业地图 raw material）
> - `08-knowledge-doc.md`（演进笔记，Phase 1-3 reference 锚点）

## 1. Goal

`projects/personal-ai-talk-2026-04-24/09-sweeper-embodied-roadmap.md`（~10-15K 字）：

- **reader**：内部技术团队（定位 / 算法同事），平等技术语言，可有 hypothesis 但需标注
- **目的**：为公司具身新项目提供
  - 行业技术现状地图（mature 度 / 工业可用性 / 国内外 cover）
  - Phase 1 / 2 / 3 路线图 + 各 phase 候选方案
  - 计算资源选型 baseline（端侧 SoC + 云端 cluster + 数据策略）
  - 团队能力 gap + 获取策略
  - 可行性评估 + risk

不做 frontier 模型横扫（已 cover 在 §1 staging raw material）；narrative 服务于 decision support，非 reference。

## 2. 已锁决定（12 项）

| ID | Decision | Resolution | 影响章节 |
| --- | --- | --- | --- |
| Q1 | 产出形式 | 单独 09 doc，不动 08 | 整体 |
| Q2 | reader 视角 | 内部技术团队 | 整体语言基调 |
| Q3 | form factor north star | wheel-legged biped + 1 arm（可蹲扫地、站爬楼 / 抓物） | §2 / §5 |
| Q3.2 | Phase 拆分 | Phase 1 = 轮式 base + 1 arm（蹲伏模式）；Phase 2 = + lift 机构；Phase 3 = full wheel-legged biped | §5 |
| Q3.4 | Phase 1 task | language-grounded pickup-and-place with multi-target placement（N1+N2+N3 capability bundle） | §2 / §3 / §5 |
| Q4.1 | 推理分配 | 全端侧（行业 frontier 默认） | §3 |
| Q4.2 | SoC 选型 | dev/pilot Orin AGX 275 TOPS → 量产 Orin NX 100 TOPS → Phase 2 国产 SoC（地平线 J6P / 黑芝麻 A2000 Pro）。**M5-M6 trigger evaluation**：NX 量化 model 在 N1+N2+N3 task 成功率 ≥ AGX baseline -5pt 则 commit NX 量产；否则 fallback AGX 量产（高端定位 ¥9000-11000 整机），NX 推到 Phase 2 cost-down（见 G5）| §3 |
| Q4.3a | 数据策略 | D 三栈 combined：web video pretrain (EgoScale-style) + sim (Isaac Sim + Cosmos Transfer) + 公开数据集 (AgiBot World / Open X-Embodiment) + 真机 5-10 万 episode | §3 |
| Q4.3b | GPU cluster | Hybrid：dev 云租 + pretrain 自购 16×H100（约 ¥1500-2000 万） | §3 |
| Q4.4 | VLA model fork base | **GR00T N1.7** (NVIDIA Open Model License, 3B Cosmos-Reason2-2B + 32-layer DiT) 主线 + Mobile Aloha teleop pipeline reference + OpenVLA 作 fallback。**M0 parallel benchmark**（GR00T vs OpenVLA 同 dataset baseline，2-4 周）+ **M3 trigger evaluation**：若 GR00T transfer 成功率 ≤ OpenVLA baseline -10pt 则切 OpenVLA（见 G4）| §4 |
| Q5.1 | Phase 1 deadline | demo 锚 WAIC 2027-07 + 量产首发锚 IFA 2027-09 / 双 11 2027-11 | §5 |
| Q6.1 | 团队主路线 | **三层 model**（见 G2）：① **核心 ML/VLA + sim 5-8 人**（新招 + 转岗）② 公司既有 ME/EE / ML infra / product 5-8 人 ⅓ FTE 复用 ③ teleop 操作员 16-20 人外包 / 第三方数据公司合作 + fork 开源（GR00T N1.7 / OpenVLA / AgiBot World / Mobile Aloha）+ 学术合作 | §4 / §6 |

## 3. Phase 1 milestone（G1 修订：并行版 13-15 月）

> **G1 修订原因**（2026-05-05）：原 sequential 加总 14-21 月，对 WAIC 2027 (14 月) / IFA 2027 (16 月) deadline buffer 实际为负数。修订为 streaming + parallel 后 13-15 月，与 Q5.1 锚点真正 align。

| Milestone | 内容 | 月数 | 累计 | 关联节点 / parallel |
| --- | --- | --- | --- | --- |
| M0 团队 + 预研 | 招聘核心 4-6 人；Orin AGX dev kit + Isaac Sim setup；**parallel benchmark GR00T N1.7 vs OpenVLA**（G4 trigger 1） | 1-2 月 | 2 月 | 2026-Q3 |
| M1 真机 prototype | 扫地机 base + arm 组装；teleop 工位 setup（8-10 个） | 2 月 | 4 月 | M2 工位 setup ‖ M1 末期 |
| M2 数据 streaming 启动 | sim + web pretrain（fork GR00T 已 ready）+ 真机 episode 滚动采集（持续到 M5）| 持续（M2-M5）| — | ‖ M3-M5 |
| M3 fork GR00T + adaptation pretrain | streaming fine-tune on AgiBot World + Open X + 真机 incremental data；端侧 baseline (AGX)；**M3 末期 trigger evaluation**（GR00T vs OpenVLA on 自有 dataset，G4 trigger 2） | 2 月 | 6 月 | ‖ M2 数据滚动 |
| M4 N1 fine-tune（WAIC demo target）| N1 散落物清场 task 抓取成功率 ≥ 70% | 3-4 月 | 9-10 月 | ‖ M5 起步 |
| M5 multi-task + 语言 grounding | N1+N2+N3 三 task；VLM grounding 上线；**M5-M6 NX 部署 trigger evaluation**（G5）| 2-3 月 | 11-13 月 | ‖ M6 cost-down 起步 |
| M6 cost-down + pilot | 50-100 台 dev unit；AGX → NX 量化迁移 prototype（trigger 失败 fallback AGX 量产）| 2 月 | **13-15 月** | ‖ M5 末期 |

**Phase 1 总时长 ≈ 13-15 月**：

- WAIC 2027-07 demo (累计 14 月) 对 M4 完成时间 (9-10 月) → buffer 4-5 月 ✅
- IFA 2027-09 量产 (累计 16 月) 对 M6 完成 (13-15 月) → buffer 1-3 月 ✅
- 双 11 2027-11 量产 (累计 18 月) 对 M6 完成 → buffer 3-5 月 ✅

**关键 enabler**（不再 sequential）：

- M2 数据采集 streaming 与 M3 pretrain 并行（fork GR00T 自带 EgoScale + sim pretrain，公司只 incremental fine-tune）
- M0 期间 parallel benchmark GR00T vs OpenVLA，提前发现 fork base 风险
- M5-M6 cost-down 评估并行（不等 M5 完成才启动 NX 量化）

## 4. Phase 2 / Phase 3 indicative timeline

| Phase | 时长 | 累计 | 主要 milestone | 软锚点 |
| --- | --- | --- | --- | --- |
| Phase 2（lift 机构 + 桌面抓取）| 12-15 月 | 33-36 月 | M7 lift 机构集成 / M8 桌面 dataset retrain / M9 量产 SoC cost-down 国产替代 | 双 11 2028 / IFA 2028（2028-Q4 量产）|
| Phase 3（wheel-legged biped + 全 manipulation）| 30-48 月 | 63-84 月 | M11 biped 团队搭建 / M12 wheel-leg 平衡 RL / M13 transition policy + stair climb / M14 manipulation × biped coupling / M15 量产 + safety cert | WAIC 2030 demo / 量产 2031-2032 |

**注**：Phase 2 / 3 timeline 未硬锁，仅 indicative；Phase 1 量产 retrospective 后重估。

## 4.5 Phase 1 总投资 baseline（G3 新增）

公司预算 commit ≈ baseline ¥3000-5500 万（与下表 align）。breakdown：

| 项 | 估算 | 说明 |
| --- | --- | --- |
| **核心 ML/VLA + sim 团队**（Q6.1 第①层 5-8 人 × 1.3 年） | ¥650-1500 万 | 高 senior level，含五险一金 / option 摊销 |
| **既有团队复用**（Q6.1 第②层 5-8 人 × ⅓ FTE × 1.3 年） | ¥175-415 万 | ME/EE / ML infra / product 各 ⅓ 投入 |
| **teleop 操作员**（Q6.1 第③层 16-20 人 × 1 年外包） | ¥100-200 万 | 12 月活跃数据采集期 |
| **GPU cluster 自购**（Q4.3b 16×H100 一次性） | ¥1500-2000 万 | pretrain 进入 stable phase 后采购 |
| **GPU cluster 云租**（dev 阶段 8 卡 × 6 月） | ¥180-300 万 | M0-M2 dev 期 |
| **真机 hardware**（dev kit + arm × 10-20 套 + 工位 sensor） | ¥300-700 万 | arm ¥10-30 万 / 套 |
| **学术合作**（1-2 个高校 lab × 1.3 年） | ¥130-390 万 | sim / VLM grounding / sim2real 关键模块 |
| **数据采集运营**（episode 标注 / 物料 / 场景搭建） | ¥50-100 万 | ¥5-10 / episode × 5-10 万 episode |
| **dev tooling / SaaS / 杂项**（Isaac Sim license / Wandb / 云存储 etc） | ¥50-100 万 | — |
| **Phase 1 总投资** | **¥3135-5705 万** | 13-15 月修订时间表下 |

**预算 scenario**：

| 预算等级 | 区间 | spec 调整方向 |
| --- | --- | --- |
| baseline | ¥3000-5500 万 | 当前 spec 直接落（公司当前 commit）|
| 紧 | ¥1500-3000 万 | GPU 全云租 + 真机数据缩到 3-5 万 episode + 砍学术合作；push 量产到 双 11 2027 |
| 充裕 | ≥ ¥6000 万 | baseline + GR00T fallback 双线（M0 起 parallel run）+ Phase 2 lift 提前预研 |

## 5. 09 doc 章节大纲

```
# 扫地机具身新项目调研路线图

## 1. 摘要 / 战略结论
   - north star + Phase 1 hard target + 11 项 root decision 一句话总结

## 2. 行业技术现状地图
   ### 2.1 VLA frontier（基于 08 doc §7 + drift staging §3-§4）
   ### 2.2 World Models 工具链（08 §8 + drift §5）
   ### 2.3 几何重建大模型化（drift §5 / SLAM 与具身 SoC 选型直接相关）
   ### 2.4 国内外 cover 矩阵 + mature 度 / 工业可用性标签

## 3. Phase 路线图
   ### 3.1 north star: wheel-legged biped + 1 arm
   ### 3.2 Phase 1: 轮式 base + 1 arm + language-grounded pickup-and-place
   ### 3.3 Phase 2: + lift 机构 + 桌面 / 沙发抓取
   ### 3.4 Phase 3: wheel-legged biped + 全 manipulation + stair climb

## 4. Phase 1 候选技术方案（fork base × 数据 × 算力 trade-off 矩阵）
   ### 4.1 VLA model fork 选型 + fork chain
       #### 4.1.1 主线 GR00T N1.7（理由 + license + 架构）
       #### 4.1.2 fork chain + trigger criteria（M0 parallel benchmark + M3 transfer evaluation + OpenVLA fallback；G4）
   ### 4.2 数据 pipeline 设计（三栈 combined 落地 + streaming fine-tune）
   ### 4.3 端侧推理 stack（Orin AGX / NX + 量化 + 蒸馏 + M5-M6 trigger；G5）
   ### 4.4 风险与 fallback 矩阵

## 5. 计算资源选型
   ### 5.1 端侧 SoC 阶梯 + cost-down 决策树（AGX → NX → 国产；trigger fail fallback AGX 量产；G5）
   ### 5.2 云端 cluster 配置（hybrid dev 云租 + pretrain 自购 16×H100）
   ### 5.3 数据采集 setup（teleop 工位 cost / location / 外包操作员；Q6.3 inline）
   ### 5.4 推理 latency budget（control loop / perception / VLM grounding）
   ### 5.5 Phase 1 总投资 baseline + 预算 scenario（¥3000-5500 万 baseline；紧 / 充裕 scenario；G3）

## 6. 团队能力 gap + 可行性评估
   ### 6.1 现有能力盘点
   ### 6.2 Phase 1 capability gap 清单
   ### 6.3 三层团队 model 落地（核心 + 既有复用 + teleop 外包；G2）
   ### 6.4 学术合作候选（清华 / 上海 AI Lab / 港大 / Stanford / CMU；Q6.2 inline）
   ### 6.5 国产工具链 partner（地平线 / 黑芝麻 / 阿里 / Cosmos 国内 team；Q6.4 inline）

## 7. 路线图 + Risk
   ### 7.1 Phase 1 milestone（M0-M6 并行版 13-15 月；G1）
   ### 7.2 Phase 2 / 3 indicative timeline（Q5.2 inline）
   ### 7.3 Risk 清单 + mitigation
       #### 7.3.1 GR00T transfer fail（G4 fallback chain）
       #### 7.3.2 NX 量产部署 fail（G5 AGX fallback）
       #### 7.3.3 真机数据采集 throughput 不达 target
       #### 7.3.4 学术合作 deliverable delay
       #### 7.3.5 cost overrun（预算 scenario 切换）

## 8. 开放问题（不做判断）
   - sim2real 长尾覆盖率
   - VLA 端侧 inference cost vs 云端协同 trade-off 何时改变
   - Phase 3 wheel-legged biped 是否应考虑 acqui-hire / spin-off

## References
- 08-knowledge-doc.md §X.Y 引用
- 08-drift-staging-for-09.md raw material
- 行业 release 公开 link（GR00T / π₀ / GraspVLA / Cosmos / WAIC / IFA 等）
```

## 6. spec grill 修订记录（G1-G5，2026-05-05）

| ID | 问题 | 修复 |
| --- | --- | --- |
| **G1** | milestone sequential 加总 14-21 月，对 deadline buffer = 0~-5 月 | 改并行版 13-15 月（streaming fine-tune + parallel benchmark + cost-down 评估并行）|
| **G2** | "5-8 核心团队"vs 实际 capability 10-15 人缺口未明确 | 三层 model：① 核心 ML/VLA 5-8 ② 既有团队 ⅓ FTE 复用 ③ teleop 外包 16-20 |
| **G3** | Phase 1 总 cost 估算缺失 | 加 §4.5 baseline ¥3000-5500 万 + 紧 / 充裕 scenario |
| **G4** | fork GR00T transfer risk + fallback 缺失 | 主线 GR00T + M0 parallel benchmark + M3 trigger evaluation + OpenVLA fallback；09 doc §4.1.2 |
| **G5** | 量产 NX 部署 viability 风险 + product 定位 ambiguity | 保 Q4.2 三阶段 + M5-M6 trigger evaluation + AGX fallback（高端定位 ¥9000-11000 整机）；09 doc §4.3 / §5.1 |

## 7. 剩余 open question（09 doc 起草中 inline 处理）

| ID | Topic | 处理 |
| --- | --- | --- |
| Q5.2 | Phase 2 / 3 软锚点细化 | 09 doc §7.2 inline |
| Q6.2 | 学术合作具体对象 | 09 doc §6.4 inline |
| Q6.3 | teleop 数据采集 location / 工位规模 / 外包公司 | 09 doc §5.3 inline |
| Q6.4 | 国产工具链 partner 优先级 | 09 doc §6.5 inline |

## 8. Next step

1. 写 09 doc 第一稿（§1 摘要 + §2 行业地图 + §3 Phase 路线图 骨架）
2. 与用户对齐 §1-§3 narrative，再扩展 §4-§8
3. 起草过程中 inline 处理 Q5.2 / Q6.2 / Q6.3 / Q6.4 细化层
4. §7.3 risk 章按 G4/G5 fallback chain + G1 buffer 评估展开

## 9. 风格约束

09 doc 沿用 `~/.cursor/rules/personal-doc-style.mdc`：

- 客观陈述 + 引用锚定（公司战略 hypothesis 标注 `<!-- REVIEW: -->`）
- 层级编号 + 同层 ≤ 3（演绎归纳）
- 中文自然语感，避免 AI 味
- 跨对象多维对照用表格
- 每个 ## 章节末配 References 子节
