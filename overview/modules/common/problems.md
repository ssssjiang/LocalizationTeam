# 通用（全组共用）— Problems

> 模块：`overview/modules/common/`
> 来源 inbox：`inbox/`（全组通用文档）

---

## P-001 内存踩踏系列问题（ASAN 分析）

- **症状**：通过 ASAN 工具发现多个 Bug，覆盖多个驱动版本（285/287/291/292）

  | Bug ID | 问题类型 | 日志文件 |
  |--------|---------|---------|
  | 285 | stack-use-after-scope | — |
  | 287 | detected memory leaks + heap-buffer-overflow | — |
  | 291 | detected memory leaks（14357）/ heap-buffer-overflow（14364）/ stack-use-after-scope（14364×2）/ memory leaks（14479）/ heap-buffer-overflow on address（14807） | drivers_mem.log.* |
  | 292 | heap-use-after-free（2073）/ heap-buffer-overflow（2135）/ memory leaks（14129/14128）| drivers_mem.log.* |

- **根因**：具体根因分散在多个 drivers 版本日志中（详见源文档截图）
- **修复**：进行中（各 Bug 状态见源文档）
- **来源**：inbox/007_通用文档/002_测试文档/001_内存踩踏分析

---

## P-002 联合双目存在批量盲区不良风险

- **症状**：联合双目在新项目中面临更严格的盲区要求；文档报告联合两批次 `OC` 分布左右目不一致，随机搭配后更容易出现大盲区，存在批量不良风险
- **根因**：文档归因于左右目结构约束不同、无法共用治具和机台，叠加厂内制程管控能力偏弱，使左右目 `Cy` 分布不居中且一致性不足；在架构盲区较去年更大的背景下，该波动更容易放大为整机盲区超限
- **修复**：进行中。文档记录联合 `2026-04-09` 批次已重新挑选 `golden` 模组点检 `OC`，并计划于 `4.14/4.15` 上整机 `monet` 继续验证整机数据；项目评估层面暂不建议采用联合非 `AA` 工艺
- **来源**：`inbox/0413新增/联合OC及盲区管控_2026-04-13-14-34-49/联合OC及盲区管控.md`；`inbox/0413新增/FLORA,LUMOS,GAIA联合双目评估_2026-04-13-14-36-45/FLORA,LUMOS,GAIA联合双目评估.md`
