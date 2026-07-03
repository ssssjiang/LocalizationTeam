# 补充篇：C++ / 并发 / 资源管理 检查原则

> 定位：Fowler《重构》第 3 章的坏味道偏 **OO / 语言无关**，缺少 C++ 专属维度。
> 本篇补三块工程中最容易踩坑、也最值得在 code review / 重构前逐条 check 的内容：
> **① 资源管理与所有权（RAII）② 并发 / 线程安全 ③ C++ 语言层坏味道**。
> 用法：改动涉及裸指针 / new / 锁 / 线程 / 跨线程共享状态时，对照速查表逐条闻味道。
> 置信度约定：条目是通用原则；末尾「本项目实例」中 `[确认]`=代码可见，`[高置信]`=强证据未运行验证，`[待验证]`=需结合运行时/头文件。

---

## 1. 一页纸速查（Check 清单）

### 1.1 资源管理 / 所有权（RAII）

| # | 检查项 | 危险信号 | 修复方向 |
|---|---|---|---|
| R1 | 每个资源都有 RAII 持有者 | 裸 `new/delete`、手动 `close/free/unlock`、`system()` | 用智能指针 / 容器 / lock_guard / `std::filesystem` |
| R2 | 所有权语义明确 | 分不清「谁负责释放」；裸指针参与释放 | 独占用 `unique_ptr`、共享用 `shared_ptr`、观察用裸指针/引用（不拥有） |
| R3 | Rule of 0/3/5 | 定义了析构却没定义拷贝/移动 | 优先 Rule of 0（成员全 RAII）；否则五个特殊成员成套定义或 `=delete` |
| R4 | 标准库替代手写/系统调用 | `system("mkdir")`、`fopen`、手拼 JSON/XML 字符串 | `create_directories` / `fstream` / 序列化库 |
| R5 | 异常安全 | 获取资源→释放之间可能抛异常而泄漏 | RAII 保证；明确 basic / strong / nothrow 哪一档 |
| R6 | 复位/清理集中且不易漏 | 一个巨型 `reset()` 手动逐个清成员 | 用 RAII/值语义让「重建对象」替代「手动复位」 |

### 1.2 并发 / 线程安全

| # | 检查项 | 危险信号 | 修复方向 |
|---|---|---|---|
| C1 | 共享可变状态必须同步 | 普通 `bool`/POD 被多线程读写；部分成员 atomic 部分不 atomic | 每个共享成员：`atomic` / 锁保护 / 或设计成不可变 |
| C2 | 同步策略一致 | 同一数据有时加锁有时不加；`memory_order` 无依据地混用 | 同一数据同一把锁；拿不准用默认 `seq_cst` |
| C3 | 临界区短、不阻塞 | 持锁时做 IO / `join` / 调用外部回调 | 锁外做耗时操作；持锁只碰共享数据 |
| C4 | 多锁固定顺序 | 不同路径以不同顺序拿多把锁 | 全局固定加锁顺序；`std::scoped_lock` 一次锁多个 |
| C5 | 线程生命周期 RAII 化 | 裸 `std::thread` 手动 join；可能自 join / 漏 join / double join | `std::jthread`(C++20) 或封装类；明确 join/detach |
| C6 | 条件变量带谓词 | `wait` 无谓词（虚假唤醒）；notify 前未改共享状态 | `cv.wait(lock, pred)`；先改状态再 notify |
| C7 | 函数级 `static` = 隐藏共享状态 | `static` 局部做 warnOnce / 缓存 / 上一次值 | 提为成员或显式状态；多实例/多线程下隔离 |
| C8 | 复合操作的原子性 | `if(!t.joinable()) t=std::thread(...)`（check-then-act） | 用锁把「检查+动作」包成一个临界区 |
| C9 | 逻辑竞态（TOCTOU） | 「检查存在→再使用」中间状态可能变 | 缩小检查与使用的窗口；持锁跨越两步 |

### 1.3 C++ 语言层坏味道

| # | 检查项 | 危险信号 | 修复方向 |
|---|---|---|---|
| L1 | const 正确性 | `const_cast` 去掉 const 后改成员 | 需在 const 方法中改的同步/缓存成员声明为 `mutable` |
| L2 | 具名常量替魔法数字 | 函数体内散落 `15 / 0.01 / 3` 等裸字面量 | `constexpr` 具名常量，命名表达含义 |
| L3 | 用类型表达状态，而非布尔沼泽 | 十几个 `bool_/atomic_bool` 共同表达系统状态 | `enum class` 状态机；单一真相来源 |
| L4 | 封装边界 | 直接读写他类 `public` 数据成员容器 | 通过接口访问；把逻辑搬到数据所在类 |
| L5 | include / 头文件卫生 | 重复 include、包含过宽 | 去重、最小包含、前置声明 |
| L6 | 聚合初始化安全 | 长位置参数 `T{a,b,c,...,n}` 无字段名 | 具名构造 / 指定初始化(C++20) / 参数对象 |
| L7 | 注释与死代码 | 成段被注释的代码；注释与代码不符 | 删死代码（交给版本控制）；注释只写「为什么」 |

---

## 2. 资源管理 / 所有权（RAII）

### R1 每个资源都有 RAII 持有者
原则：资源（内存、文件、锁、线程、句柄）的获取即绑定到一个对象的生命周期，析构时自动释放。手动 `delete/free/close/unlock` 是坏味道，因为任何提前 return / 抛异常都会漏释放。

```cpp
// 坏：手动管理，异常/提前 return 即泄漏
void f() {
  std::mutex m; m.lock();
  if (cond) return;        // 忘了 unlock -> 死锁
  m.unlock();
}
// 好：RAII
void f() {
  std::lock_guard<std::mutex> lk(m);   // 作用域结束自动 unlock
  if (cond) return;                    // 安全
}
```

### R2 所有权语义明确
- 独占所有权 → `std::unique_ptr`
- 共享所有权 → `std::shared_ptr`（真的需要共享才用）
- 仅观察、不拥有 → 裸指针 / 引用 / `string_view` / `span`（绝不 `delete`）

「一个裸指针，读者能一眼看出它拥不拥有资源吗？」答不上来就是坏味道。

### R3 Rule of 0 / 3 / 5
- **Rule of 0**：类不直接管理资源（成员都是 RAII 类型）→ 五个特殊成员都别写，编译器默认即正确。**首选**。
- 一旦你需要自定义析构/拷贝构造/拷贝赋值/移动构造/移动赋值中的**任意一个**，通常五个都要考虑（Rule of 5），否则会得到危险的默认实现（如浅拷贝导致 double free）。

```cpp
// 坏：定义了析构，却用默认拷贝 -> 两个对象持同一指针 -> double free
struct Buf { char* p; ~Buf(){ delete[] p; } };
// 好：Rule of 0
struct Buf { std::unique_ptr<char[]> p; };   // 拷贝自动禁用、移动自动可用
```

### R4 用标准库替代手写 / 系统调用
`system("mkdir -p ...")` 有命令注入面、不可移植、错误处理弱；手拼 JSON 极易产出非法格式。已有标准设施就别手写。

```cpp
// 坏
system(("mkdir -p " + dir).c_str());
// 好
std::error_code ec;
std::filesystem::create_directories(dir, ec);
```

### R5 异常安全
获取资源到释放之间若抛异常，是否泄漏？给每个函数定一档保证：nothrow（不抛）/ strong（要么成功要么回到原状）/ basic（不泄漏、状态有效但可能改变）。RAII 是达成 basic/strong 的基础工具。

### R6 复位逻辑集中且不易漏
一个几十行的手动 `reset()`/`deactivate()` 逐个清成员，是**霰弹式修改**的温床——新增成员就得记得来补一行。优先用「析构旧对象 + 构造新对象」（值语义 / 重建）替代「原地手动复位」。

---

## 3. 并发 / 线程安全

### C1 共享可变状态必须同步
跨线程访问的每个可变成员，必须满足三者之一：`std::atomic`、锁保护、或不可变（构造后只读）。**最隐蔽的坏味道是「不一致」**：一部分标志用了 atomic，另一部分同样跨线程的标志却是普通 `bool`——说明作者没有统一的同步模型。

### C2 同步策略一致
同一份数据始终用同一把锁保护。`memory_order` 的放宽（relaxed/acquire/release）必须有明确理由；拿不准就用默认 `seq_cst`，正确性优先于微优化。

### C3 临界区短、不在锁内阻塞
持锁期间做文件 IO、`thread.join()`、或回调用户代码 = 死锁 / 优先级反转的高发区（回调里可能反向拿锁）。

```cpp
// 坏：持锁调用外部回调
{ std::lock_guard lk(m); if (cb_) cb_(data_); }
// 好：锁内取数据，锁外回调
Data snapshot; { std::lock_guard lk(m); snapshot = data_; }
if (cb_) cb_(snapshot);
```

### C4 多锁固定顺序
需要同时持有多把锁时，全程序按固定顺序获取，或用 `std::scoped_lock(m1, m2)`（内部死锁避免算法）。

### C5 线程生命周期 RAII 化
裸 `std::thread` 到处 `joinable()/join()` 是脆弱设计：容易自 join（在线程自身里 join 自己）、漏 join（析构未 join → `std::terminate`）、double join。C++20 用 `std::jthread`（析构自动 join、支持 `stop_token`），或自己封一层 RAII。

### C6 条件变量必须带谓词
```cpp
// 坏：虚假唤醒后误以为条件成立
cv.wait(lock);
// 好：谓词 + shutdown 兜底
cv.wait(lock, [&]{ return ready_ || shutdown_; });
```
notify 前先修改共享状态，再 `notify_*`。

### C7 函数级 static 是隐藏的共享状态
`static` 局部变量的初始化在 C++11 起是线程安全的，但**后续读写不是**。用它做 `warnOnce`、缓存「上一次的值」、去重，在多线程/多实例下就是共享可变状态。

```cpp
// 坏：多线程竞争、多实例互相污染
bool f(double x){ static double prev = 0; bool jump = std::abs(x-prev) > TH; prev = x; return jump; }
// 好：状态成为对象成员，随实例隔离，需要时再加锁
```

### C8 复合操作的原子性（check-then-act）
`if (!t.joinable()) t = std::thread(...)` 不是原子的：两个线程可能同时判为 `!joinable()` 并各自建线程。把「检查 + 动作」用同一把锁包住。

### C9 逻辑竞态（TOCTOU）
即便每步都加了锁，「先检查再使用」之间状态仍可能被改（Time-Of-Check-To-Time-Of-Use）。缩小窗口或让检查与使用共处一个临界区。

---

## 4. C++ 语言层坏味道

### L1 const 正确性 → 用 mutable 而非 const_cast
`const` 成员函数里需要加锁 / 更新缓存时，把该 `mutex`/缓存成员声明为 `mutable`；`const_cast<T&>(...)` 去 const 后写入是设计缺陷的信号（且对真正 const 对象是 UB）。

```cpp
// 坏
double get() const { const_cast<std::mutex&>(m_).lock(); ... }
// 好
mutable std::mutex m_;
double get() const { std::lock_guard lk(m_); ... }
```

### L2 具名常量替魔法数字
函数体内的裸 `15 / 0.01 / 0.3 / 3` 无法自解释、改一处漏一处。提为 `constexpr` 具名常量，名字表达含义与单位。

### L3 用类型表达状态，而非布尔沼泽
十几个 `bool_ / atomic_bool` 共同描述系统状态 → 组合爆炸、易自相矛盾。用 `enum class` 建单一状态机；已有枚举就别再和散落布尔并存。

### L4 封装边界
直接读写别的类的 `public` 数据容器（`other.someMap_[...]`）= 内幕交易 / 依恋情结的 C++ 具体形态。通过接口访问，或把操作数据的逻辑搬到数据所属的类。

### L5 include / 头文件卫生
重复 include、包含过宽拖慢编译且掩盖依赖。去重、最小包含、能前置声明就不 include。

### L6 聚合初始化安全
`T{a, b, c, ..., n}` 十几个位置参数无字段名，错位极难发现。用具名构造函数、C++20 指定初始化 `T{.x=..,.y=..}`、或引入参数对象。

### L7 注释与死代码
成段被注释掉的代码交给版本控制删除即可；注释只写「为什么这么做」，不写「代码在做什么」。`// Renamed to avoid conflict` 这类注释往往是复制粘贴的痕迹，是重复代码的信号。

---

## 5. 本项目实例（`okvis_multisensor_processing/src/ThreadedSlam.cpp`）

> 把上面的 check 项映射到实际发现，便于对照学习。行号基于当前版本。

| Check | 位置 | 说明 | 置信度 |
|---|---|---|---|
| R4 | L3305–3322 `initDebugRecording` | `system("mkdir -p "+debugOutputDir_)`，且文件已 include `<filesystem>` 却不用 | [确认] |
| R4 | L3327–3615 `recordFrontendPackage/recordBackendState` | 200+ 行手拼 JSON，靠 `needs_comma`/`firstXxx` 手工维护，注释里有修 bug 痕迹 | [确认] |
| R6 | L3617–3702 `reinit_deactivate` | ~40 个成员手动逐个 reset，新增成员极易漏 | [确认] |
| C1 | 头文件 L500–501 | `firstFrontendFrame_/firstDetectFrame_` 为普通 `bool`，与大量 `atomic_bool` 并存（同步模型不一致；注：`shutdown_/blocking_` 实为 atomic，无问题） | [高置信] |
| C5/C8 | L666,794,2121,2482,2495,2750,3113 | 裸 `reinitThread_` 在多线程里 `if(!joinable()) reinitThread_=std::thread(...)`，无锁保护的 check-then-act | [高置信] |
| C5 | `reinit`→`reinit_deactivate`→`stopThreading`→`join(各loop线程)` | 工作线程内触发全量停线程，存在自 join / 死锁风险 | [待验证] |
| C7 | L734,766,803,2085 | `static warnOnce/warnOnce2/prevL,prevR/lastCmdCheck` 承载跨调用隐藏状态 | [确认] |
| L1 | L327 `calculatePoseEstimate` | `const` 方法内 `const_cast<std::mutex&>(lastOptimisedStateMutex_)`，应改 `mutable` | [确认] |
| L2 | L1060,3139,1240,2567 及多处队列大小 3 | `numKeypoints()<15`、`dt=0.01`、`%100`、`...IfFull(...,3)` 等魔法数字 | [确认] |
| L3 | 全类 | `firstFrontendFrame_/is_pausing_/imu_converged_/hasStarted_/...` 布尔沼泽，与 `SystemState` 枚举并存 | [确认] |
| L4 | L1207,1340,2202,3202,3212 | 直接访问 `estimator_.imuMeasurementsByFrame_`、`estimator_.T_AiS_`、`frontendOptimizer_.states_/problem_` | [高置信] |
| L5 | L40/56,42/57,48/53 | `<chrono>/<cstdlib>/<sys/resource.h>` 各重复 include | [确认] |
| L6 | L1399 等多处 | `State{...}` ~14 个位置参数无字段名 | [确认] |
| L7 | L1184-1188,2532-2536,2785-2805 | 成段注释代码；大量 `// Renamed to avoid conflict` | [确认] |

---

## 沉淀区（回填用）

- **我的复述**：
- **我的疑问**：
- **我想补的 C++ 实战例子 / 本项目更多实例**：
