# 重定位逻辑梳理

> 整理日期：2026-04-14  
> 整理人：宋姝

---

## 整体框架：三个场景，两类发起方


| 场景         | 发起方               | 导航动作           | 结束判定                |
| ---------- | ----------------- | -------------- | ------------------- |
| 割草中定位变差    | **SLAM** 判断并通知导航  | 速度减半，只做 odo 递推 | SLAM 判断 RTK 固定解比例恢复 |
| 机器被搬动      | **导航** 判断并通知 SLAM | 走 2m×2m 方格     | SLAM pose.init 0→1  |
| 其他（基站外重启等） | **导航** 判断并通知 SLAM | 复用现有 reset 流程  | —                   |


---

## 场景一：割草中定位差

### 触发条件（AND 关系）

- RTK 当前非固定解
- 过去 1s 内 RTK 非固定解比例 > 80%，**或** 1s 内收不到 RTK 数据
- 视觉 tracking lost

### 状态机流程

割草中定位差状态机

```
normal
  ↓ [触发条件满足]
relocate_start  → 发 RelocateCmd(relocate_cmd=1)
  ↓ next sensor
relocating  → 只做 odo 递推，不做视觉更新
  ↓ 检查：过去 3s RTK 固定解比例 > 95%？
  N → 回 relocating 继续等
  Y ↓
relocate_end  → 发 RelocateCmd(relocate_cmd=0)
  ↓ next sensor
normal
```

**超时**：定位长时间无法找回，导航可直接报错；产品定义 5min 停机报错。

### 接口

```protobuf
// common_protobuf/proto/common/SlamMsg.proto
message SlamToNavMsg {
    enum Type {
        RELOCATE_BAD_LOCATION = 2;
    }
    bool relocate_cmd = 3; // 1=开始重定位, 0=结束重定位
}
```

与状态机交互：

- 建图模式 → 报错
- 割草模式 → 忽略（机器进入主动重定位状态）

```protobuf
message SlamMsg {
    enum Type {
        RELOCATE_BAD_LOCATION = 4;
    }
    bool relocate_cmd = 7;
}
```

---

## 场景二：搬动重定位

### 触发

导航检测到机器被人为搬动。

### 流程

```
导航检测到搬动
  → 发 RELOCATE_MOVED 给 SLAM
  → 导航执行 2m×2m 方格行走
  → SLAM 持续发布不可用 pose（init=0）
  → SLAM 找回 RTK 固定解 + 初始对准成功 → init: 0→1
  → 重定位成功，app 更新机器位置到当前实际位置 B
```

### 接口

```protobuf
// common_protobuf/proto/common/SlamMsg.proto
message NavToSlamMsg {
    enum Type {
        RELOCATE_MOVED = 10;
    }
}
```

**重定位成功条件**：SLAM 能够找到 RTK 固定解 + 重新初始对准成功。

### UX 细节

机器从 A 被搬到 B：

- 搬动期间 app 持续显示位置 A，状态显示"重定位中"
- 重定位成功后，app 位置跳至 B，恢复工作

---

## 场景三：其他情况

基站外重启等其他触发场景，复用已有 `NavToSlamMsg::reset_cmd`，导航主动发 reset，无新接口。

---

## 关键差异点


|           | 场景一                | 场景二                  |
| --------- | ------------------ | -------------------- |
| 谁先感知异常    | SLAM（RTK + 视觉都差）   | 导航（IMU/里程计检测搬动）      |
| SLAM → 导航 | RelocateCmd（开始/结束） | 无主动消息，靠 pose.init 反馈 |
| 导航 → SLAM | 无                  | RELOCATE_MOVED       |
| 导航行为      | 减速 + 纯 odo 推算      | 走 2×2 方格             |


---

## 待确认项

1. **流程图缺失超时分支**：`relocating` 状态未画出超时/失败→报错路径，与产品文档"5min 停机"存在 gap，需确认状态机是否有该分支
2. **场景一"主动重定位状态"触发来源**：割草模式下状态机忽略 SLAM 消息，但"机器进入主动重定位状态"在哪里触发，接口文档未说明

---

## 引用原始材料

1. **产品策略文档**
  `teams/fusion/inbox/0413新增/RTK定位&重定位_2026-04-13-11-03-36/RTK定位&重定位.md`  
   内容：重定位产品定义、触发时机、成功/失败处理、UX 交互、出桩定位逻辑
2. **技术接口文档**
  `teams/fusion/inbox/004_融合定位/002_算法文档/008_重定位/001_导航-slam重定位接口/导航-slam重定位接口.md`  
   内容：三场景 protobuf 接口定义、导航/SLAM 交互逻辑、状态机交互（2025-11-11 新增）
3. **状态机流程图**（场景一：割草中定位差）
  原图 Image Token: `IUP6bdbSxo3TR6xumKNcBjnInFg`，本地副本：`images/reloc-state-machine-bad-location.png`

