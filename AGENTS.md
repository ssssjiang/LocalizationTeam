## Learned User Preferences

- Always communicate with the user in Chinese (simplified); code and comments in English.
- When running `raw-materials-curation`, always present 「线索摘要」 (phase 1 summary) and wait for explicit user confirmation (often a minimal one-liner like "ok") before proceeding to phase 2 extraction.
- After curation, user may ask follow-up queries about specific documents; search within structured module docs (`decisions.md`, `gaps.md`) first before scanning raw inbox files.
- When analyzing weekly meeting reports: summarize 已完成 items briefly (归纳概括); record 待办 items with full details including sub-tasks.
- Treat recurring station maintenance (e.g. CQIQC / CIIQC line maintenance) as long-running upkeep, not as weekly Action items; keep those in a separate long-term section when tracking meetings.
- For Feishu updates to SPM or product when they are in the same chat, prefer a gentle, question-led tone that invites alignment rather than a hard directive tone.
- User (宋姝) is the localization team lead and does not personally take on specific execution work items in weekly tracking.
- Daily workspace (`workspace/YYYY-MM-DD/daily.md`) todo section has two subsections: 「跟进/派发」and 「我的工作项」; both are the user's own work. Uncompleted 「跟进/派发」items (unchecked) carry over to the next day's daily.md verbatim until explicitly marked done. All task list items must use markdown to-do syntax `- [ ]` (including nested children), not plain `-`; descriptive notes/group headings remain as plain bullets.
- MR review ownership: vision team MRs → 宋姝 reviews (goes into 跟进 list); fusion team MRs → 林子越 reviews; laser team MRs → 明坤 reviews. Non-vision MRs are recorded in 团队进展 table only, not in 跟进 list.
- Upward summaries to leadership or PM on technical programs (e.g. radar dropout): prefer one ultra-short sentence—business outcome first, key numbers and a clear failure fallback (e.g. the user’s preferred 断流口径：「减少断流时停机重定位；6s 内无感恢复定位；失败才执行重定位」); avoid MULLS/setpose-style implementation jargon unless asked.
- For single-document curation (one file from `~/下载/`, not a full inbox batch): first output a 「梳理稿」 with 结论先行 + 金字塔结构(论点/论据)，并嵌入相关图片预览；只有用户回复「归档」后才真正落盘（复制 inbox、改写 decisions/timeline/gaps/problems、按命名规范 copy 图到 `images/`）。
- After archiving, the user frequently asks reviewer-style follow-ups (concept clarifications, edge-case challenges)；preserve enough context from the just-archived doc to answer in line.

## Learned Workspace Facts

- Project root: `/home/songshu/repo/LocalizationTeam`
- Raw materials ("inbox") live under `teams/<team>/inbox/` subdirectories, organized by date-stamped subfolders (e.g., `inbox/0413新增/`); single-document archive uses the same path with `<原文档名>/` containing 原文 + 全部原图。
- Structured knowledge docs live under `teams/<team>/modules/<module>/` and `overview/modules/<module>/`: each module contains `decisions.md`, `timeline.md`, `gaps.md`, `problems.md`, and `images/`.
- Key modules: `overview/modules/common/`, `teams/vision/modules/vslam/`, `teams/fusion/modules/fastlivo/`, `teams/fusion/modules/fusion/`, `teams/laser/modules/mslam/`.
- Numbering convention: decisions use `D-001…N`; gaps use `G-xxx` (observations), `Q-xxx` (open questions), `R-xxx` (risks); numbers are per-module and increment strictly.
- Project conventions are documented in `docs/process/raw-materials-conventions.md`; the `raw-materials-curation` skill is the primary tool for converting inbox docs into structured team knowledge.
- Images from inbox documents are copied to the corresponding module's `images/` directory with descriptive names (whiteboard/design figures kept, raw test screenshots skipped); fastlivo 模块图片按 `fastlivo_<topic>_<variant>.{png,gif}` 命名。
- Vision team weekly meeting records live under `teams/vision/weekly/YYYY-WXX.md` (one file per ISO week); filename should annotate the covered date range; each file is organized per-person with 「本周完成」 + 「待办」 sections.
- Team uses 飞书多维表格 to manage two parallel tracking tables: (1) bug 跟踪表 — bug id / 责任人 / 分配时间 / 当前状态（用于组内进度与工作量跟踪）; (2) 代码合入与发版表 — bug id / 功能 / 涉及代码库 / 合入人 / 合入 dev 时间 / 发版版本（用于对外输出给 SPM 指导 cherry-pick，以及内部按版本追踪 bug 关联代码）。Local HF rollup markdown: `docs/hf-tracking/融合定位组HF跟踪.md` (regenerate with `scripts/build_hf_tracking.py`).
- Channel mapping (corridor visual mapping) canonical summaries live under `teams/vision/modules/vslam/通道建图/` as `01-产品需求.md` … `04-测试需求.md`，二期工作项集中在 `05-二期工作项.md`（编号 `W-01…N` 严格递增，只纳入与二期直接相关的项）；raw intake stays in `teams/vision/inbox/通道建图/`. Prefer embedding or linking original images and Feishu artifacts in consolidated docs instead of vague “screenshot-only” citations. Cross-team special topic reports go under `overview/modules/common/` as standalone `.md` files; competitor digests and curated test plans often live under `overview/modules/common/specials/竞品测试/`. Radar dropout (断流) cross-doc summaries live under `overview/modules/common/specials/radar-pause/`.
- Vision team meeting/project tracking 原始记录归档到 `teams/vision/inbox/005_视觉slam/009_视觉定位组项目会议跟踪记录/YYYY-MM-DD_<主题>.md`；跨项目/跨团队的项目周例会不放 `teams/<team>/周报/`，也不留在个人 `workspace/`。Temperature test docs for the stereo camera: `teams/vision/inbox/005_视觉slam/005_测试文档/006_温补测试情况更新/温补测试情况更新.md`。
- Laser team weekly reports and meeting minutes live under `teams/laser/周报/`：周报文件 `laser-weekly-YYYY-WXX.md` 直接放在该目录下，组会纪要放在子目录 `teams/laser/周报/组会纪要/YYYY-MM-DD.md`（目录有 README 说明结构）。
- 三维彩色建图相关主题（FAST-LIVO2 彩色建图、地面空洞补全、实景三维地图拼接、多次割草拼接）统一归到 `teams/fusion/modules/fastlivo/`。