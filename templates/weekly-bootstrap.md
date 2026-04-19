<%*
// ============================================================
// Weekly Bootstrap —— 周报自动生成器（自用复盘版）
// 触发：周五下班前 Cmd+P，或周一回顾时手动跑
// 输出：weekly/YYYY-Www.md
// 内容聚合：
//   1. 本周已完成项（从 daily 提取所有 - [x]）
//   2. 本周末仍未完成、将顺延到下周的项（从最后一份 daily 提取 - [ ]）
//   3. 本周新增决策（扫所有 modules/*/decisions.md 中本周新增 D-xxx）
//   4. 本周新增问题（扫所有 modules/*/problems.md 中本周新增 P-xxx）
//   5. 本周团队进展（合并各 daily 的「团队进展」表格行）
//   6. 本周排期变动（合并各 daily 的「排期更新」节）
//   7. 本周知识沉淀（合并各 daily 的「知识 & 信息积累」节）
// ============================================================

const vault = app.vault;
const today = tp.date.now("YYYY-MM-DD");
const todayMoment = tp.date.now("YYYY-MM-DD", 0, today, "YYYY-MM-DD");

// ---- 计算本周一 / 本周日（ISO 周，周一开始）----
function getWeekRange(dateStr) {
  const d = new Date(dateStr + "T00:00:00");
  const dow = d.getDay(); // 0=Sun..6=Sat
  const offsetToMon = dow === 0 ? -6 : 1 - dow;
  const monday = new Date(d);
  monday.setDate(d.getDate() + offsetToMon);
  const sunday = new Date(monday);
  sunday.setDate(monday.getDate() + 6);
  const fmt = (x) => x.toISOString().slice(0, 10);
  // ISO 周号
  const tmp = new Date(Date.UTC(monday.getFullYear(), monday.getMonth(), monday.getDate()));
  const dayNum = tmp.getUTCDay() || 7;
  tmp.setUTCDate(tmp.getUTCDate() + 4 - dayNum);
  const yearStart = new Date(Date.UTC(tmp.getUTCFullYear(), 0, 1));
  const weekNo = Math.ceil((((tmp - yearStart) / 86400000) + 1) / 7);
  return {
    monday: fmt(monday),
    sunday: fmt(sunday),
    year: tmp.getUTCFullYear(),
    week: String(weekNo).padStart(2, "0"),
  };
}

const range = getWeekRange(today);
const weeklyDir = "weekly";
const weeklyPath = `${weeklyDir}/${range.year}-W${range.week}.md`;

// ---- 建 weekly/ 目录 ----
if (!(await vault.adapter.exists(weeklyDir))) {
  await vault.createFolder(weeklyDir);
}

// ---- 收集本周内所有 daily 文件 ----
const workspaceDir = "workspace";
const folder = vault.getAbstractFileByPath(workspaceDir);
const dailyDirs = (folder && folder.children ? folder.children : [])
  .filter(f => f.children !== undefined && /^\d{4}-\d{2}-\d{2}$/.test(f.name))
  .map(f => f.name)
  .filter(n => n >= range.monday && n <= range.sunday)
  .sort();

const dailyContents = {};
for (const d of dailyDirs) {
  const p = `${workspaceDir}/${d}/daily.md`;
  if (await vault.adapter.exists(p)) {
    dailyContents[d] = await vault.adapter.read(p);
  }
}

// ---- 解析工具：按章节切片 ----
function extractSection(content, headingRegex, stopRegex = /^##\s/m) {
  const m = content.match(headingRegex);
  if (!m) return "";
  const startIdx = m.index + m[0].length;
  const rest = content.slice(startIdx);
  const stopMatch = rest.match(stopRegex);
  return stopMatch ? rest.slice(0, stopMatch.index).trim() : rest.trim();
}

// ---- ① 已完成项 ----
const completedByDay = {};
for (const [d, c] of Object.entries(dailyContents)) {
  const lines = c.split("\n").filter(l => /^\s*-\s*\[x\]/i.test(l));
  if (lines.length) completedByDay[d] = lines;
}

// ---- ② 本周末仍未完成项（取最后一份 daily 的「跟进/派发」未勾选）----
const lastDailyDate = dailyDirs[dailyDirs.length - 1];
let openItems = [];
if (lastDailyDate && dailyContents[lastDailyDate]) {
  const followSection = extractSection(
    dailyContents[lastDailyDate],
    /###\s*跟进\s*\/\s*派发\s*\n/,
    /^###\s/m
  );
  openItems = followSection.split("\n").filter(l => /^\s*-\s*\[\s\]/.test(l));
}

// ---- ③ ④ 扫所有 modules/*/decisions.md 和 problems.md，找本周新增 ----
async function findFilesByName(rootPath, fileName) {
  const results = [];
  async function walk(dir) {
    const node = vault.getAbstractFileByPath(dir);
    if (!node || !node.children) return;
    for (const child of node.children) {
      if (child.children !== undefined) {
        await walk(child.path);
      } else if (child.name === fileName) {
        results.push(child.path);
      }
    }
  }
  await walk(rootPath);
  return results;
}

// 简单策略：扫所有 decisions.md / problems.md，提取条目；用本周日期范围过滤"本周新增"
// 由于 decisions.md/problems.md 不一定带日期，这里只能粗略提取，标记为「本周可能新增（请人工核对）」
async function scanModuleEntries(fileName, prefix) {
  const found = [];
  const candidatePaths = [];
  for (const root of ["overview", "laser", "fusion", "vision", "calibration", "teams"]) {
    if (await vault.adapter.exists(root)) {
      const paths = await findFilesByName(root, fileName);
      candidatePaths.push(...paths);
    }
  }
  for (const p of candidatePaths) {
    const content = await vault.adapter.read(p);
    // 提取 ## D-xxx 或 ## P-xxx 标题，附本周日期范围内的"决策日期/首次发现"
    const itemRegex = new RegExp(`^##\\s+(${prefix}-[A-Z0-9]+\\s+.+)$`, "gm");
    let m;
    while ((m = itemRegex.exec(content)) !== null) {
      const headerLine = m[1];
      // 在标题后 30 行内找日期字段（决策日期 | / 首次发现：）
      const tailIdx = m.index + m[0].length;
      const slice = content.slice(tailIdx, tailIdx + 1500);
      const dateMatch = slice.match(/(\d{4}-\d{2}-\d{2})/);
      if (dateMatch) {
        const dateStr = dateMatch[1];
        if (dateStr >= range.monday && dateStr <= range.sunday) {
          found.push({ source: p, header: headerLine, date: dateStr });
        }
      }
    }
  }
  return found;
}

const newDecisions = await scanModuleEntries("decisions.md", "D");
const newProblems = await scanModuleEntries("problems.md", "P");

// ---- ⑤ ⑥ ⑦ 各 daily 的「团队进展」「排期更新」「知识 & 信息积累」聚合 ----
function collectSection(headingRegex) {
  const out = [];
  for (const d of dailyDirs) {
    const c = dailyContents[d];
    if (!c) continue;
    const sec = extractSection(c, headingRegex);
    // 去掉空骨架（只有 - 或表头）
    const meaningful = sec.split("\n").some(l => l.trim() && !/^[|\-\s]*$/.test(l) && !/^\|\s*\|/.test(l));
    if (sec && meaningful) {
      out.push({ date: d, content: sec });
    }
  }
  return out;
}

const teamProgress = collectSection(/##\s*团队进展\s*\n/);
const scheduleChanges = collectSection(/##\s*排期更新\s*\n/);
const knowledge = collectSection(/##\s*知识\s*&\s*信息积累\s*\n/);

// ---- 组装周报内容 ----
let body = `# ${range.year}-W${range.week} 周报（${range.monday} ~ ${range.sunday}）\n\n`;
body += `> **生成时间**：${today}\n`;
body += `> **覆盖 daily**：${dailyDirs.length} 份（${dailyDirs.join(", ") || "无"}）\n\n`;
body += `---\n\n`;

body += `## 一、本周已完成\n\n`;
if (Object.keys(completedByDay).length === 0) {
  body += `_本周 daily 中未提取到 \`- [x]\` 完成项。_\n\n`;
} else {
  for (const [d, lines] of Object.entries(completedByDay)) {
    body += `### ${d}\n\n${lines.join("\n")}\n\n`;
  }
}

body += `## 二、未完成 / 顺延到下周\n\n`;
if (openItems.length === 0) {
  body += `_无未完成项（或本周末 daily 不存在）。_\n\n`;
} else {
  body += `> 来自 ${lastDailyDate} 「跟进/派发」节\n\n`;
  body += openItems.join("\n") + "\n\n";
}

body += `## 三、本周新增决策\n\n`;
if (newDecisions.length === 0) {
  body += `_本周未在 modules/*/decisions.md 中发现日期落在本周的 D-xxx 条目。_\n_提示：如有手工补录的决策（无日期标注），请补充到此处。_\n\n`;
} else {
  for (const d of newDecisions) {
    body += `- **${d.header}** （${d.date}） · \`${d.source}\`\n`;
  }
  body += "\n";
}

body += `## 四、本周新增问题\n\n`;
if (newProblems.length === 0) {
  body += `_本周未在 modules/*/problems.md 中发现日期落在本周的 P-xxx 条目。_\n\n`;
} else {
  for (const p of newProblems) {
    body += `- **${p.header}** （${p.date}） · \`${p.source}\`\n`;
  }
  body += "\n";
}

body += `## 五、团队进展（聚合）\n\n`;
if (teamProgress.length === 0) {
  body += `_各 daily 的「团队进展」节为空骨架，无可聚合内容。_\n\n`;
} else {
  for (const t of teamProgress) {
    body += `### ${t.date}\n\n${t.content}\n\n`;
  }
}

body += `## 六、排期变动\n\n`;
if (scheduleChanges.length === 0) {
  body += `_各 daily 的「排期更新」节为空。_\n\n`;
} else {
  for (const s of scheduleChanges) {
    body += `### ${s.date}\n\n${s.content}\n\n`;
  }
}

body += `## 七、知识 & 信息沉淀\n\n`;
if (knowledge.length === 0) {
  body += `_各 daily 的「知识 & 信息积累」节为空。_\n\n`;
} else {
  for (const k of knowledge) {
    body += `### ${k.date}\n\n${k.content}\n\n`;
  }
}

body += `---\n\n`;
body += `## 八、本周复盘（手写）\n\n`;
body += `### 做得好的\n\n- \n\n`;
body += `### 做得不好的 / 需要改进\n\n- \n\n`;
body += `### 下周重点\n\n- \n\n`;
body += `### 给团队的话\n\n- \n\n`;

// ---- 写入 weekly 文件 ----
if (!(await vault.adapter.exists(weeklyPath))) {
  await vault.create(weeklyPath, body);
  new Notice(`✅ 周报已生成：${weeklyPath}\n聚合 ${dailyDirs.length} 份 daily / ${newDecisions.length} 决策 / ${newProblems.length} 问题`);
} else {
  // 如已存在，追加一条更新提示，不覆盖（保留你已写的复盘）
  new Notice(`ℹ️ ${weeklyPath} 已存在，直接打开（如需重新聚合，请先删除现有文件）`);
}

// ---- 清理 Templater 中间产物，打开周报 ----
const createdFile = tp.file.find_tfile(tp.file.title);
if (createdFile && createdFile.path !== weeklyPath) {
  await vault.delete(createdFile);
}
const weeklyFile = vault.getAbstractFileByPath(weeklyPath);
if (weeklyFile) {
  await app.workspace.getLeaf(false).openFile(weeklyFile);
}
-%>
