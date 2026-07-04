# 实战案例：Frontend.cpp 重构评估与规划

> 对象：`okvis_frontend/src/Frontend.cpp`（类 `Frontend`，3621 行 / 24 个成员函数实现）。
> 仓库：`/home/songshu/repo/mapping_ws/refactor`，分支 `private/songs/refactor`。
> 目的：把《重构》第 2~5 章原则落到 OKVIS 前端大文件上——先评估、再规划，**不在本文件里动代码**。
> 置信度约定：`[确认]`=代码/构建脚本可见；`[高置信]`=强证据未运行验证；`[待验证]`=需运行时/更多上下文确认。

---

## 0. 结论先行（TL;DR）

> - **现状**：`Frontend` 相对内聚（职责就是"视觉前端"），不是 God Class，但 **超长函数** 与 **重复的相机畸变 switch** 两项味道极重。
> - **头号味道**：同一套 4-way `switch(distortionType)` 分发到模板函数，**散在 8 处、共 29 个 case** `[确认]`——加一种相机模型要改 8 处，漏改即静默 `default throw`（典型「重复的 switch」3.12）。
> - **最大红线**：`Frontend` **零回归测试** `[确认]`——`okvis_frontend_test` 只测 `OfflineMapPipeline`，不碰 `Frontend`。但 test 目标结构完整、可编译（`build/okvis_frontend/okvis_frontend_test` 已生成），补表征测试门槛低。
> - **策略**：测试先行 → 无行为清理 → 消重复/消重复 switch → 提炼函数拆超长 → 提炼类。风险从低到高，一卡一手法一提交。
> - **本次范围**：**Phase 0 → Phase 4**（含拆类），**不做 Phase 5 并发/资源收口**。
> - **不建议**：一次性大重写。

---

## 1. 现状评估

### 1.1 过长函数（3.3）`[确认]`
| 函数 | 行数 | 位置 |
|---|---|---|
| `dataAssociationAndInitialization` | 524 | 722–1246（编排主入口，含 loop closure 大段） |
| `matchToMap` | 450 | 1459–1909 |
| `verifyRecognisedPlace` | 319 | 402–721 |
| `matchStereo` | 288 | 2578–2866 |
| `matchMotionStereo` | 212 | 2238–2450 |
| `vis_track_and_reproject` | 198 | 3423–EOF |
| `doWeNeedANewKeyframe` | 156 | 1302–1458 |
| `matchToMapByThreadUnitialised` | 143 | 2094–2237 |
| `matchMotionStereoByThread` | 126 | 2451–2577 |
| `runRansac2d2d` | 117 | 3140–3257 |
| `detectAndDescribe` | 114 | 287–401 |

### 1.2 重复的 switch（3.12）—— 头号味道 `[确认]`
- 8 处 `switch(distortionType)`（322 / 601 / 749 / 803 / 970 / 1110 / 3302 / 3532），同一 `RadialTangential / Equidistant / RadialTangential8 / DoubleSphere` 四分支分发到模板函数，共 **29 个 case**。
- 新增相机模型 = 改 8 处；漏改任一处即静默走 `default throw`。→ 收敛为**单一分发器**（模板 visitor / `dispatchByDistortion(type, functor)`）。

### 1.3 重复代码（3.2）`[高置信]`
- `matchToMapByThread`(2012) 与 `matchToMapByThreadUnitialised`(2094) 共享大段 setup（`T_SC/T_WC1/T_CW1`、`ddata`、landmark 遍历骨架）。
- `trackingQuality → TrackingQuality` enum 映射（787–791）活跃一处，注释里另留一份（3471–3476）。
- `detectAndDescribe` 里 additional detector 的 detect/describe 对 `cameraIndex==0 / ==1` 抄两遍（360–393）。

### 1.4 魔法数字（L2）`[确认]`
- `48`（BRISK 描述子字节数）出现 **19 次**；`kptrad=0.09`、`maxDistancePointToEpipolarLine=20`、reproj 阈值 `20.0/150.0`（2027）、trackingQuality 阈值 `0.01/0.3`、loop closure `p>0.4 / attempts<10 / 40`、`50`（1016 已 TODO 标注）。

### 1.5 死代码 / 注释（L7 / 3.24）`[确认]`
- 约 48 行"被注释掉的代码"；`vis_track_and_reproject` 尾部大段注释（3468–3476）；17 处 `TODO/FIXME/HACK`。

### 1.6 并发 / 资源（C/R）`[高置信]`（本次范围外，仅记录）
- 裸 `std::thread*` 存于 `cnnThreads_` map，手动 `delete`（1045、1270）+ 手动 join → R1/C5。
- `threadPool_.reset(new ThreadPool(...))` 运行时重建扩容（1081），check-then-act（C8）。
- **`threadPoolSize_` 在 `Frontend.hpp:593` 被注释，但 `Frontend.cpp:1078–1082`（`#ifdef OKVIS_USE_NN`）在用它** → 开 NN 编译疑似编译不过 `[待验证：取决于 OKVIS_USE_NN]`。
- 同步模型不一致（C1）：`trackingLost_` 为 `atomic_bool`，`isInitialized_/isSlip_` 为普通 `bool`，`isInitialized()` 无锁读、`dataAssociationAndInitialization` 里写（830）。
- 绑核：`Detector1ThreadCPUID=4` + `pthread_setaffinity_np`（293–308，`ENABLE_X5_CPU_SECH_OPTIMIZE`）——**行为参数，红线不动**。

### 1.7 条件编译分散 `[确认]`
- `OKVIS_USE_NN / USE_RERUN / USEOPENCLWRAPPER / ENABLE_X5_CPU_SECH_OPTIMIZE / CMAKE_CROSSCOMPILING / OKVIS_USE_LOOP_CLOSURES` 多宏交织；`initialiseBriskFeatureDetectors` 两份定义（3354 `USEOPENCLWRAPPER` / 3399 `#else`）。

### 1.8 测试现状 —— 决定性 `[确认]`
- `okvis_frontend_test` 仅编译 `test/runTests.cpp` + `test/TestOfflineMapPipeline.cpp`，只测 `OfflineMapPipeline`，**`Frontend` 零覆盖**。
- test 目标结构完整、可编译（`build/okvis_frontend/okvis_frontend_test` 已存在），补 Frontend 表征测试门槛低。

---

## 2. 重构目标（可度量）
- 8 处 distortionType switch → 收敛到 1 处分发器。
- 超长函数拆到单函数 ≤ ~80 行；`dataAssociationAndInitialization` 变"编排 + 少量胶水"。
- `48`/阈值等魔法数字 → 具名 `constexpr`。
- `Frontend` public API（`detectAndDescribe/propagation/dataAssociationAndInitialization`）建表征测试，`ctest` 绿。
- 拆出 `BriskDetectorFactory / CnnRunner / PlaceRecognizer` 三个内聚组件。

---

## 3. 重构策略与原则
- **测试先行**（第 4 章）：没测试的地方先补表征测试再动手。
- **小步 + 常绿**：每提交只做一个手法，改完能 build、测试通过、可回滚。
- **行为保持**：性能/实时性相关（绑核、线程优先级、线程池扩容策略、数值阈值）视为"行为"，不在重构中顺手改。
- **范围控制**：一次一层，超范围就停下记录再决定。

---

## 4. 已确认约束（决策，2026-07-04，songshu 拍板）

1. **范围到 Phase 4**：做测试先行 + 清理 + 消重复/消 switch + 拆超长函数 + 拆类；**不做 Phase 5 并发/资源收口**（并发味道仅记录于 §1.6，留待后续单独立项）。
2. **红线完全沿用 ThreadedSlam 那套**：
   - 不动数值阈值 / 绑核 / 线程优先级 / 线程池扩容策略等"行为"参数。
   - public 虚接口（`detectAndDescribe / propagation / dataAssociationAndInitialization`）签名与可观察行为保持不变。
   - 一卡一手法、一卡一提交、随时可回滚。
3. **C++17**：不使用 `std::jthread`、指定初始化等 C++20 特性。
4. **拆类走渐进 seam**：先拆低耦合独立类（`BriskDetectorFactory` 最先）+ public API 表征测试，接口化按需、局部引入。

---

## 5. 分阶段规划（顺序即风险从低到高）

### Phase 0 · 表征测试脚手架（前置，不可跳过）`风险:低 价值:极高`
- 动作：
  1. `propagation`（1247，`const` 纯计算）最先补单测——最易测、无副作用。
  2. `detectAndDescribe` 的关键点产出 + 线程安全（多相机并行）黑盒测试。
  3. `dataAssociationAndInitialization` 端到端表征测试：极小相机系统 + 空/单帧 snapshot（首帧路径、tracking 弱路径）。
- 手法：第 4 章「自测试代码」；characterization test。
- 验证：见 §8。

### Phase 1 · 无行为清理（热身）`风险:极低`
- 动作：删死代码/注释块（3468–3476 等）、去重复 include、魔法数字提 `constexpr`（`48→kBriskDescriptorBytes`、`0.01/0.3`、`kptrad`、reproj 阈值 `20.0/150.0`）。
- 手法：移除死代码(237)；符号常量化。属 Fast-path 级单点改动。

### Phase 2 · 消重复 + 消重复 switch（收益最高）`风险:低-中`
- 动作：
  - 提炼 `trackingQualityToEnum(double)`（消 787–791 + 注释处）。
  - **引入相机畸变分发器**：把 8 处 `switch(distortionType)` 收敛为一个模板 visitor / `dispatchByDistortion(type, functor)`。以多态/模板取代重复条件表达式(272)。
  - 提炼 `matchToMapByThread` / `Unitialised` 公共 setup；提炼 `detectAndDescribe` additional-detector 重复块。
- 手法：提炼函数(106)、引入参数对象(140)、以多态取代条件表达式(272)。
- 验证：每提炼一处即跑测试；逐个提交。

### Phase 3 · 提炼函数拆超长函数 `风险:中`
- 动作：`dataAssociationAndInitialization` 拆为 `runMatchToMap / runMotionStereo / decideKeyframe / runLoopClosure`；同法拆 `matchToMap / verifyRecognisedPlace / matchStereo`。
- 手法：提炼函数(106)、分解条件表达式(260)。
- 验证：每拆一处一提交；表征测试绿。

### Phase 4 · 提炼类（渐进 seam）`风险:中`
- 候选（独立性从高到低）：
  1. `BriskDetectorFactory`（合并两份 `initialiseBriskFeatureDetectors`）—— 边界最清晰，最先拆。
  2. `CnnRunner`（`cnnThreads_ / cnnFutures_ / threadPool_ / endCnnThreads`）—— 注意仅搬移、不改并发语义（约束 1/2）。
  3. `PlaceRecognizer`（`dBow_ + verifyRecognisedPlace + loop closure` 段）。
- 手法：提炼类(182)、搬移函数(198)、搬移字段(207)。
- 验证：每拆一个类一个提交；表征测试 + 新类单测。

---

## 6. 优先级矩阵
| 阶段 | 价值 | 风险 | 成本 | 何时做 |
|---|---|---|---|---|
| P0 测试 | ★★★★★ | 低 | 中 | 立刻，先于一切 |
| P1 清理 | ★★ | 极低 | 低 | 与 P0 并行热身 |
| P2 消重复/消 switch | ★★★★★ | 低-中 | 中 | P0 后立即（本文件最大收益）|
| P3 拆超长函数 | ★★★★ | 中 | 中-高 | P2 后 |
| P4 拆类 | ★★★ | 中 | 中-高 | P3 后 |

---

## 7. 风险与红线
- **红线 1**：无表征测试不动生产代码（P1 起须 P0 基线绿）。
- **红线 2**：一次提交只做一个手法，随时可回滚。
- **红线 3**：不改数值阈值 / 绑核 / 优先级 / 线程池扩容策略等"行为"参数。
- **红线 4**：public 虚接口签名与行为保持不变。
- **红线 5**：并发/资源味道（§1.6）本次不碰；`threadPoolSize_` hpp/cpp 不一致等留待后续立项。

---

## 8. 构建 / 验证方式（G1）

> 主会话对每张卡的固定校验命令（`build/` 已配置，test 目标已生成）：

```bash
# 编译测试目标（增量快）
cmake --build build --target okvis_frontend_test -j$(nproc)

# 运行测试
./build/okvis_frontend/okvis_frontend_test
```
- 前置门槛：G1 验证手段（上）已就位；G2 无死测试需隔离（现有测试与 Frontend 无关，可直接用）；G3 需先补首批 Frontend 表征测试并跑绿作为基线。

---

## 9. 任务卡 backlog（每卡：目标 / 手法 / 范围红线 / 验收 / 回滚）

> 顺序执行；`[seam]` 标记渐进依赖注入接缝。验收命令统一见 §8。一卡一手法一提交。

| 卡 | Phase | 目标 | 手法 | 范围红线 | 验收 |
|---|---|---|---|---|---|
| C0.1 | P0 | `propagation` 纯计算单测 | 自测试代码 | 不改生产代码 | 新测试绿 |
| C0.2 | P0 | `detectAndDescribe` 产出 + 多相机线程安全黑盒测试 | 自测试代码 | 不改生产代码 | 新测试绿 |
| C0.3 | P0 | `dataAssociationAndInitialization` 首帧/弱跟踪表征测试 | 自测试代码 | 不改生产代码 | 新测试绿、覆盖 §5 P0 路径 |
| C1.1 | P1 | 删死代码/注释块 + 去重复 include | 移除死代码(237) | 单文件、无行为变更 | 编译 + 表征测试绿 |
| C1.2 | P1 | 魔法数字提 `constexpr`（`48`/阈值/reproj） | 符号常量化 | 不改数值本身 | 同上 |
| C2.1 | P2 | 提炼 `trackingQualityToEnum(double)` | 提炼函数(106) | 纯函数、无副作用 | 单测 + 全量测试绿 |
| C2.2 | P2 | 引入 `dispatchByDistortion` 分发器，收敛 8 处 switch | 以多态取代条件表达式(272) | 分发语义/行为不变、保留 default throw | 8 处行为一致、测试绿 |
| C2.3 | P2 | 提炼 `matchToMapByThread`/`Unitialised` 公共 setup | 提炼函数(106) | 两路共用、行为保持 | 测试绿 |
| C2.4 | P2 | 提炼 `detectAndDescribe` additional-detector 重复块 | 提炼函数(106) | 仅 USEOPENCLWRAPPER 路径 | 测试绿 |
| C3.1 | P3 | 拆 `dataAssociationAndInitialization` 为若干阶段函数 | 提炼函数(106) | 编排语义不变 | 测试绿 |
| C3.2 | P3 | 拆 `matchToMap` / `verifyRecognisedPlace` / `matchStereo` | 提炼函数(106) | 行为保持 | 测试绿 |
| C4.1 | P4 | 拆 `BriskDetectorFactory`（合并两份 `initialiseBriskFeatureDetectors`） | 提炼类(182) | 检测器构造行为不变 | 独立单测绿 |
| C4.2 | P4 `[seam]` | 拆 `CnnRunner`（搬移 CNN 线程管理） | 搬移函数(198) | **不改并发语义（约束1）** | 测试绿 |
| C4.3 | P4 `[seam]` | 拆 `PlaceRecognizer`（dBow + verify + loop closure） | 提炼类(182) | 仅回环路径 | 独立单测绿 |

---

## 沉淀区（回填用）
- **首批表征测试实际覆盖到哪些路径**：
- **`dispatchByDistortion` 最终形态（模板 visitor / 宏 / 其他）**：
- **拆类过程中发现的新味道 / 范围扩张记录**：
