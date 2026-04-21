## Learned User Preferences

- Always communicate with the user in Chinese (simplified); code and comments in English.
- When running `raw-materials-curation`, always present 「线索摘要」 (phase 1 summary) and wait for explicit user confirmation before proceeding to phase 2 extraction.
- User confirms phase transitions with minimal input ("ok", simple one-liners); no need to re-summarize the full plan after confirmation.
- User manually attaches the `raw-materials-curation` skill to messages when initiating inbox processing sessions.
- After curation, user may ask follow-up queries about specific documents; search within structured module docs (`decisions.md`, `gaps.md`) first before scanning raw inbox files.
- When analyzing weekly meeting reports: summarize 已完成 items briefly (归纳概括); record 待办 items with full details including sub-tasks.
- Treat recurring station maintenance (e.g. CQIQC / CIIQC line maintenance) as long-running upkeep, not as weekly Action items; keep those in a separate long-term section when tracking meetings.
- For Feishu updates to SPM or product when they are in the same chat, prefer a gentle, question-led tone that invites alignment rather than a hard directive tone.
- User (宋姝) is the localization team lead and does not personally take on specific execution work items in weekly tracking.
- Daily workspace (`workspace/YYYY-MM-DD/daily.md`) todo section has two subsections: 「跟进/派发」and 「我的工作项」; both are the user's own work. Uncompleted 「跟进/派发」items (unchecked) carry over to the next day's daily.md verbatim until explicitly marked done.
- MR review ownership: vision team MRs → 宋姝 reviews (goes into 跟进 list); fusion team MRs → 林子越 reviews; laser team MRs → 明坤 reviews. Non-vision MRs are recorded in 团队进展 table only, not in 跟进 list.

## Learned Workspace Facts

- Project root: `/home/songshu/repo/LocalizationTeam`
- Raw materials ("inbox") live under `teams/<team>/inbox/` subdirectories, organized by date-stamped subfolders (e.g., `inbox/0413新增/`).
- Structured knowledge docs live under `teams/<team>/modules/<module>/` and `overview/modules/<module>/`: each module contains `decisions.md`, `timeline.md`, `gaps.md`, `problems.md`, and `images/`.
- Key modules: `overview/modules/common/`, `teams/vision/modules/vslam/`, `teams/fusion/modules/fastlivo/`, `teams/fusion/modules/fusion/`, `teams/laser/modules/mslam/`.
- Numbering convention: decisions use `D-001…N`; gaps use `G-xxx` (observations), `Q-xxx` (open questions), `R-xxx` (risks); numbers are per-module and increment strictly.
- Project conventions are documented in `docs/process/raw-materials-conventions.md`.
- Images from inbox documents are copied to the corresponding module's `images/` directory with descriptive names; whiteboard/design figures are kept, raw test screenshots are skipped.
- `raw-materials-curation` is the primary skill used in this workspace for converting inbox documents into structured team knowledge.
- Vision team weekly meeting records live under `teams/vision/weekly/YYYY-WXX.md` (one file per ISO week); filename should annotate the covered date range; each file is organized per-person with 「本周完成」 + 「待办」 sections.
- Team uses 飞书多维表格 to manage two parallel tracking tables: (1) bug 跟踪表 — bug id / 责任人 / 分配时间 / 当前状态（用于组内进度与工作量跟踪）; (2) 代码合入与发版表 — bug id / 功能 / 涉及代码库 / 合入人 / 合入 dev 时间 / 发版版本（用于对外输出给 SPM 指导 cherry-pick，以及内部按版本追踪 bug 关联代码）。Local HF rollup markdown: `docs/hf-tracking/融合定位组HF跟踪.md` (regenerate with `scripts/build_hf_tracking.py`).
- Channel mapping (corridor visual mapping) canonical summaries live under `teams/vision/modules/vslam/通道建图/` as `01-产品需求.md` … `04-测试需求.md`; raw intake stays in `teams/vision/inbox/通道建图/`. Prefer embedding or linking original images and Feishu artifacts in consolidated docs instead of vague “screenshot-only” citations. Cross-team special topic reports still go under `overview/modules/common/` as standalone `.md` files.
- Temperature test documents for the stereo camera are located at `teams/vision/inbox/005_视觉slam/005_测试文档/006_温补测试情况更新/温补测试情况更新.md`.