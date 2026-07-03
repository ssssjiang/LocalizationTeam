# 实战案例：ThreadedSlam.cpp 重构评估与规划

> 对象：`okvis_multisensor_processing/src/ThreadedSlam.cpp`（类 `ThreadedSlam`，~4058 行）。
> 目的：把《重构》第 2~5 章的原则落到一个真实的多线程 SLAM 大文件上——先评估、再规划，**不在本文件里动代码**。
> 置信度约定：`[确认]`=代码/构建脚本可见；`[高置信]`=强证据未运行验证；`[待验证]`=需运行时/更多上下文确认。

---

## 0. 结论先行（TL;DR）

> - **现状**：单类 4058 行的 God Class，坏味道以「**重复代码**」和「**无测试网**」两项最致命。
> - **最大红线**：`ThreadedSlam` 目前**没有任何有效的自动化测试** `[确认]`——`test/` 下的用例引用的是已删除的旧类 `ThreadedKFVio.hpp`，且 CMake 测试目标只编译 `test_main.cpp`（`CMakeLists.txt` L92–94），那些用例未被 build。叠加 6+ 线程的并发复杂度，**当前任何重构都是"无保护高空作业"**。
> - **策略**：严格「测试先行 → 纯函数提炼消重复 → 提炼类 → 数据/状态收口 → 并发编排收尾」。**并发相关改动放到最后、且必须在测试网建立后再动**。
> - **不建议**：一次性大重写（rewrite）。风险不可控、无法小步验证、丢历史。

---

## 1. 现状评估

### 1.1 规模与职责（Large Class / God Class）`[确认]`
单个 `ThreadedSlam` 同时承担至少 8 类职责：
- 传感器接入（`addImages / addImuMeasurement / addWheelEncoderMeasurement`）
- 线程编排与生命周期（`startThreads / stopThreading / ~ThreadedSlam / reinit*`）
- 前端处理循环（`detectLoop / frontendLoop`）
- 后端优化循环（`backendLoop / optimisePublishMarginalise / doFinalBa`）
- 重定位（`relocalizeLoop / adjust*WithRelocalization`）
- 地图管理（`loadMap / saveMap / unloadMap / *VIMapBuilding / optimizeMap`）
- 发布与可视化（`publishingLoop / visualisationLoop / display`）
- 调试录制 + 命令文件轮询（`recordFrontendPackage / recordBackendState / checkAndProcessCommandFile`）

头文件成员 ~90 个（队列群、线程群、状态机、4 条平行 deque、byFrame map、算法对象……），是"改一处牵一片"的典型土壤。

### 1.2 坏味道分布（详见《补-C++并发与资源管理检查原则》§5 与本轮清单）
| 类别 | 代表 | 密度 |
|---|---|---|
| 重复代码 | 「构建 State/发布数据」抄 4 份（L1383/1760/1919/2916）；omega_S 片段 ≥7 处；trackingQuality→enum ×5 | **极高** |
| 过长函数 | frontendLoop(~510) / backendLoop(~444) / processFrame(~374) / optimisePublishMarginalise(~261) | 高 |
| 魔法数字 | `<15`、`0.01/0.3`、`dt=0.01`、`%100`、队列大小 `3` | 高 |
| 死代码/注释 | 成段注释（L1184/2532/2785-2805）、`// Renamed to avoid conflict` 大量 | 中 |
| 并发/资源 | `system("mkdir")`、手拼 JSON、`const_cast` mutex、裸 `reinitThread_` check-then-act、`static` 隐藏状态 | 中高 |
| 布尔沼泽 | ~12 个 bool/atomic 标志 与 `SystemState` 枚举并存 | 中 |

### 1.3 测试现状 —— 决定性 `[确认]`
- 测试可执行 `okvis_multisensor_processing_test` **仅编译 `test/test_main.cpp`**（`CMakeLists.txt` L92–94）。
- `testThreading.cpp / testDataFlow.cpp / testSynchronizer.cpp` 均 `#include <okvis/ThreadedKFVio.hpp>`，但该头文件在仓库中**已不存在**；用例针对旧类 `ThreadedKFVio` + Mock 接口，属**遗留死测试**，且带数据的用例还被 `/* */` 注释掉。
- **净结论**：`ThreadedSlam` 无回归保护网。→ 这是第 4 章原则的直接现实：**重构前必须先补测试**。

### 1.4 并发复杂度 `[高置信]`
- 6+ 工作线程：`detect / frontend / backend / publishing / visualisation / reloc / fullGraphOpt / mapOpt / reinit`。
- 跨线程协作：`snapshotMutex_ + snapshotCv_ + snapshotVersion_` 的版本协议、`frontendDataCv_`、`lastOptimisedStateCv_`。
- 高风险点：`reinitThread_` 无锁的 check-then-act（7 处）；`reinit` 在工作线程内触发全量停线程（潜在自 join / 死锁，`[待验证]`）。

### 1.5 双流水线并存 `[高置信]`
同步 `processFrame()`（L900）在 `useAsyncProcessing_` 时开头即 `return false`，但仍被 `stopThreading()` L1656 调用。生产走异步 `frontend/backendLoop`。同步路径疑似死路径，是 1.2「重复代码」的重要来源。**是否可删需先确认调用方**（见 §7）。

---

## 2. 重构目标（可度量的完成标准）

- 单函数 ≤ ~60 行、圈复杂度显著下降（frontendLoop/backendLoop 拆开）。
- 消除 4 份「构建 State/发布」重复 → 收敛到 1 处。
- `ThreadedSlam` 职责数从 8 降到「编排 + 少量胶水」，其余拆出独立类。
- 关键路径建立表征测试（characterization tests），CI 可跑、绿色。
- 并发共享状态同步模型统一（无裸普通成员跨线程写、线程 RAII 化）。

---

## 3. 重构策略与原则

- **测试先行**（第 4 章）：没有测试的地方，先补表征测试再动手。
- **小步 + 常绿**：每个提交只做**一个**手法（第 5 章名录里的一个），改完能 build、测试通过、可回滚。
- **行为保持**：重构不改可观察行为；性能/实时性相关（绑核、线程优先级、队列大小）视为"行为"，不在重构中顺手改。
- **并发最后动**：语言层/结构层清理先行；触及锁、线程、内存序的改动排到最后，且必须有测试网。
- **范围控制**：一次一层，超范围就停下来记录再决定（scope expansion rule）。

---

## 4. 分阶段规划

> 顺序即风险从低到高。每阶段可独立停下并交付。

### Phase 0 · 测试脚手架（前置，**不可跳过**）`风险:低 价值:极高`
- 动作：
  1. 清理/隔离 `test/` 下引用 `ThreadedKFVio` 的死测试（移出 build 或删除，先确认无人依赖）。
  2. 为 `ThreadedSlam` 建**表征测试**：构造/析构、`addImages/addImu/addWheel` 的入队与丢帧行为、pause/resume、shutdown 幂等。**优先做不依赖 DI 的 public API 黑盒行为测试**（真实对象 + 极小相机系统），Mock 注入按 §8 渐进引入。
  3. 对「可纯函数化」的逻辑（trackingQuality→enum、omega_S 提取、wheel wrapDiff 判定）先写**单元测试**（此时它们还在大函数里，测试可先针对抽出后的自由函数）。
- 手法：第 4 章「自测试代码」；characterization test。
- 验证：`ctest` 绿；覆盖到后续要改的路径。
- 数据不足项：见 §7（测试要不要真实跑 estimator）。

### Phase 1 · 无行为清理（热身）`风险:极低`
- 动作：删死代码/注释块（L1184/2532/2785-2805）、去重复 include（L40/56 等）、修正文件头 `ThreadedSlam3` 注释、魔法数字提为 `constexpr`（L1060/1240/2567/队列大小）。
- 手法：移除死代码；符号常量化。
- 验证：编译通过 + 表征测试绿。属 Fast-path 级别单点改动。

### Phase 2 · 提炼纯函数 / 消重复（收益最高的一步）`风险:低-中`
- 动作：
  - 提炼 `trackingQualityToEnum(double)`（消 5 处）。
  - 提炼 `computeOmegaS(imuDeque, timestamp, b_g)`（消 ≥7 处）。
  - 提炼 `buildPublishedState(StateId, ...)` / `PublicationBuilder`：把 L1383/1760/1919/2916 四份「遍历 id→取值→构 State」收敛为一处。
  - 提炼 measurement 收集与 deque 剪枝的公共 helper。
- 手法：提炼函数(106)、以查询取代临时变量(178)、引入参数对象(140)。
- 验证：每提炼一处即跑测试；逐个提交。

### Phase 3 · 提炼类（拆 God Class）`风险:中`
- 候选（按独立性从高到低）：
  1. `DebugRecorder`（`initDebugRecording/recordFrontendPackage/recordBackendState`）—— 独立、无并发耦合，最先拆；顺带把手拼 JSON 换库、`system("mkdir")` 换 `std::filesystem`。
  2. `CommandFileWatcher`（`checkAndProcessCommandFile`）—— IO + 命令解析，边界清晰。
  3. `PublicationBuilder`（承接 Phase 2 的 buildPublishedState + landmarks 打包）。
  4. `MapController`（`load/save/unload/optimizeMap/*VIMapBuilding` 转发）。
- 手法：提炼类(182)、搬移函数(198)、搬移字段(207)。
- 验证：每拆一个类一个提交；表征测试 + 针对新类的单测。

### Phase 4 · 数据与状态收口 `风险:中`
- 动作：
  - `State{...}` 长位置参数 → 具名构造/参数对象（消错位风险）。
  - 布尔沼泽 → 以 `SystemState` 为单一真相的状态机；`const_cast` mutex → `mutable`。
  - 4 条平行 deque 的所有权/剪枝集中到一个小组件。
- 手法：引入参数对象(140)、封装变量(132)、以对象取代基本类型(174)。
- 验证：测试绿；重点回归 pause/resume/reinit 路径。

### Phase 5 · 并发与线程编排（**最后、最危险**）`风险:高`
- 前置门槛：Phase 0 测试网必须已覆盖构造/析构/shutdown/reinit。
- 动作：
  - `reinitThread_` 的 check-then-act 用锁封装成 `RestartController`（消 7 处竞态）。
  - 裸 `std::thread` → **C++17 自封装 RAII wrapper**（析构自动 join；C++17 无 `std::jthread`）；统一 join/detach 语义。**不触碰绑核/优先级逻辑（约束 3）**。
  - 梳理 `reinit → stopThreading` 的自 join / 死锁风险（先用测试复现，再改）。
  - 统一 snapshot 版本协议为一个 `SnapshotBus` 组件。
- 手法：提炼类(182) + 并发专项（见《补-C++并发与资源管理检查原则》C1/C5/C8）。
- 验证：ThreadSanitizer（TSan）+ 压力测试；反复跑构造/析构/reinit。

---

## 5. 优先级矩阵

| 阶段 | 价值 | 风险 | 成本 | 何时做 |
|---|---|---|---|---|
| P0 测试 | ★★★★★ | 低 | 中 | **立刻，先于一切** |
| P1 清理 | ★★ | 极低 | 低 | 与 P0 并行热身 |
| P2 消重复 | ★★★★★ | 低-中 | 中 | P0 后立即 |
| P3 拆类 | ★★★★ | 中 | 中-高 | P2 后 |
| P4 数据/状态 | ★★★ | 中 | 中 | P3 后 |
| P5 并发 | ★★★★ | 高 | 高 | **最后，须有测试网** |

---

## 6. 风险与红线

- **红线 1**：无测试不碰并发（P5 前必须 P0）。
- **红线 2**：一次提交只做一个手法，随时可回滚。
- **红线 3**：不在重构中改数值/绑核/优先级/队列大小等"行为"参数。
- **红线 4**：删双路径（同步 processFrame）前必须确认无外部调用方（§7）。

---

## 7. 已确认约束（决策，2026-07-03）

> 以下为 songshu 拍板，作为后续所有重构的硬约束/红线。

1. **同步 `processFrame()` 路径必须保留** —— 它用于与异步路径做效果对照，**不得删除**。
   影响：不能靠"删同步路径"消重复；改为让同步/异步**共用提炼出的 helper**（行为保持，两边都调用同一实现）。
2. **C++17** —— 不使用 `std::jthread`、指定初始化等 C++20 特性。线程 RAII 化用 **C++17 自封装 wrapper**（析构自动 join）。
3. **绑核 / 线程优先级不动** —— `BackendMainThreadCPUID`、`lockCPUID`、`set_current_thread_high_priority()`、`pthread_setaffinity_np` 相关全部**尊重现有实现**，重构中不调整、不"顺手优化"（视为行为的一部分）。
4. **测试走 Mock 接口** —— 需给 `ThreadedSlam` 引入可注入的依赖边界。
   ⚠️ **代价（确认事实）**：`estimator_.` 调用 183 处、`frontend_./frontendOptimizer_.` 44 处，其中直接访问对方 `public` 数据成员 29 处。**全量接口化风险极高、且是无测试网下的大手术**。故采用**渐进 seam**（见 §8）：先拆低耦合独立类做单测 + public API 表征测试，Mock/接口化按需、局部、最后引入。

---

## 8. 执行流水线：子代理实现 + 主会话校验

### 8.1 角色与回路
- **子代理（composer-2.5）**：领**一张任务卡**，只做卡内一个手法，产出 diff + 自检说明。
- **主会话（本会话）**：校验每张卡 —— ①范围是否越界 ②行为是否保持 ③编译/测试是否通过 ④是否可回滚。不通过则打回。
- **回路**：定义卡 → 派子代理 → 收 diff → 主会话校验（build+test+review）→ 绿则合入、红则打回 → 下一张卡。
- **原则**：一卡一手法、一卡一提交、随时可回滚；卡之间尽量无依赖或依赖显式声明。

### 8.2 前置门槛（P-1，未过不派实现类子代理）
- **G1 验证手段**：主会话必须能对每张卡给出「通过/不通过」的**可执行证据**（编译 + 测试）。构建方式见 §8.4（待定）。
- **G2 死测试隔离**：`test/` 下引用 `ThreadedKFVio.hpp` 的用例移出 build（否则 test target 编不过，无法建基线）。
- **G3 基线绿**：在动任何生产代码前，先让"空测试 target + 新增表征测试"跑通一次，作为回归基线。

### 8.3 子步骤 backlog（每卡：目标 / 手法 / 范围红线 / 验收 / 回滚）

> 顺序执行；`[seam]` 标记为渐进依赖注入的接缝点。验证命令待 §8.4 敲定后填入每卡。

| 卡 | Phase | 目标 | 手法 | 范围红线 | 验收 |
|---|---|---|---|---|---|
| C0.1 | P0 | 隔离 `ThreadedKFVio` 死测试、建基线 | 移除死代码(237) | 只动 `test/` 与 test CMake | test target 可编译、可运行 |
| C0.2 | P0 | public API 表征测试：构造/析构/shutdown 幂等 | 自测试代码 | 不改生产代码 | 新测试绿 |
| C0.3 | P0 | 表征测试：addImu/addWheel 入队与过滤、addImages 丢帧 | 自测试代码 | 不改生产代码 | 新测试绿、覆盖 §4 P0 路径 |
| C1.1 | P1 | 删死代码块 + 去重复 include + 修文件头注释 | 移除死代码(237) | 单文件、无行为变更 | 编译 + 表征测试绿 |
| C1.2 | P1 | 魔法数字提 `constexpr` 具名常量 | 符号常量化 | 不改数值本身 | 同上 |
| C2.1 | P2 | 提炼 `trackingQualityToEnum` / `computeOmegaS` | 提炼函数(106) | 纯函数、无副作用 | 单测 + 全量测试绿 |
| C2.2 | P2 | 提炼 `PublicationBuilder::build*`，同步/异步四处共用 | 提炼函数/类 | **保留同步路径（约束1）** | 四处行为一致、测试绿 |
| C2.3 | P2 | 提炼 measurement 收集 / deque 剪枝 helper | 提炼函数(106) | 同步异步共用 | 测试绿 |
| C3.1 | P3 | 拆 `DebugRecorder`（含 `system→filesystem`、JSON 换库） | 提炼类(182) | 仅调试路径 | 独立单测绿 |
| C3.2 | P3 | 拆 `CommandFileWatcher` | 提炼类(182) | 仅命令文件路径 | 独立单测绿 |
| C3.3 | P3 `[seam]` | 拆 `MapController`（转发 mapManager_） | 搬移函数(198) | 转发语义不变 | 测试绿 |
| C4.1 | P4 | `State{...}` → 具名构造/参数对象 | 引入参数对象(140) | 字段语义不变 | 测试绿 |
| C4.2 | P4 | `const_cast` mutex → `mutable` | — | 单点 | 编译 + 测试绿 |
| C4.3 | P4 | 布尔沼泽 → 以 `SystemState` 收口 | 封装变量(132) | 行为保持 | 回归 pause/resume/reinit |
| C5.1 | P5 | 线程 C++17 RAII wrapper | 提炼类(182) | **不动绑核/优先级（约束3）** | 构造/析构/shutdown 反复跑绿 |
| C5.2 | P5 | `reinitThread_` check-then-act 收口为 `RestartController` | 提炼类(182) | 行为保持 | TSan + 压力测试 |
| C5.3 | P5 `[seam]` | 按需对 estimator_/frontend_ 局部引入可注入接缝 + Mock | 以委托取代继承/接口抽取 | 仅隔离所需最小面 | Mock 单测绿 |

### 8.4 构建 / 验证方式（**待定，阻塞 G1**）
> 这是 §8.2 G1 的落地方式，决定主会话能否给"通过/不通过"的证据。选定前不派会改生产代码的卡。

---

## 沉淀区（回填用）

- **我的复述**：
- **我拍板的决策（§7 的 4 个问题）**：
- **想先做哪个 Phase / 哪个手法**：
