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
