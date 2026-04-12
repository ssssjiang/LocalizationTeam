# 设计文档：参数标定独立为顶层 team 目录

**日期**：2026-04-12
**状态**：已批准，待实施

---

## 背景与动机

原始结构将「标定」和「视觉SLAM」合并在 `teams/vision/` 下。但实际上：

- 标定有专属负责人（邱冰冰），与 VSLAM 人员分开
- 标定原始材料量大（新补充的 `006_参数标定/` 有 22+ 子目录）
- 混放导致 vision 目录语义不清，视觉 SLAM 未来难以干净入驻

目标：将标定拆分为独立顶层 team 目录，与 `laser/fusion/vision` 平级。

---

## 目标结构

```
teams/
  laser/         ← 不变
  fusion/        ← 不变
  vision/        ← 仅保留 VSLAM（当前均为占位符）
  calibration/   ← 新建
    people.md
    tech.md
    inbox/
      003_标定相关/
      006_参数标定/
    modules/
      calibration/
        timeline.md
        decisions.md
        problems.md
        gaps.md
        images/
```

---

## 操作清单

### 1. 目录移动


| 操作    | 源路径                                 | 目标路径                                     |
| ----- | ----------------------------------- | ---------------------------------------- |
| mkdir | —                                   | `teams/calibration/`                     |
| mv    | `teams/vision/modules/calibration/` | `teams/calibration/modules/calibration/` |
| mv    | `teams/vision/inbox/003_标定相关/`      | `teams/calibration/inbox/003_标定相关/`      |
| mv    | `teams/vision/inbox/006_参数标定/`      | `teams/calibration/inbox/006_参数标定/`      |


### 2. 新建文件


| 文件                            | 内容来源                                                     |
| ----------------------------- | -------------------------------------------------------- |
| `teams/calibration/people.md` | 从 `teams/vision/people.md` 提取邱冰冰相关内容，标题改为「参数标定组」         |
| `teams/calibration/tech.md`   | 从 `teams/vision/tech.md` 提取「方向一：标定」全节，标题改为「参数标定组 — 技术地图」 |


### 3. 编辑现有文件


| 文件                       | 变更                                                                                                                                          |
| ------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `teams/vision/people.md` | 移除邱冰冰行；标题更新为「视觉定位组（VSLAM）」；顶部加注「标定方向已独立至 teams/calibration/」                                                                                |
| `teams/vision/tech.md`   | 移除「方向一：标定」整节；顶部加注同上；保留「方向二：VSLAM」                                                                                                           |
| `README.md`              | 更新顶部描述（三个→四个方向）；快速导航新增 calibration 条目；更新所有指向 `teams/vision/modules/calibration/` 的链接为 `teams/calibration/modules/calibration/`；inbox 表格更新路径 |


### 4. 保留空目录（为未来 VSLAM 材料留位）

- `teams/vision/inbox/`（保留，将来放 VSLAM 原始资料）
- `teams/vision/modules/`（保留，将来放 VSLAM 模块）

---

## 范围边界

- **本次不做**：`006_参数标定/` 内部材料的结构化提取（那是独立的后续梳理任务）
- **本次不做**：`teams/vision/tech.md` 的 VSLAM 部分内容填充（仍为占位符）

---

## 验证标准

- `teams/calibration/` 目录存在，包含 people/tech/inbox/modules
- `teams/vision/modules/` 和 `teams/vision/inbox/` 下不再有标定相关内容
- `README.md` 所有链接可达（无断链）
- `teams/vision/tech.md` 不再包含标定内容

