<%*
// ============================================================
// Daily Bootstrap —— 一键初始化当天工作目录
// 功能：
//   1. 在 workspace/YYYY-MM-DD/ 下建好 daily.md / inbox/ / images/
//   2. 套用 workspace/TEMPLATE-daily.md 骨架
//   3. 自动顺延"跟进/派发"章节中的未勾选 - [ ] 项（往前找最近 14 天内最后一份 daily）
//   4. 把当天创建的新文件自动重命名+移动到正确位置
// ============================================================

const today = tp.date.now("YYYY-MM-DD");
const vault = app.vault;
const workspaceDir = "workspace";
const targetDir = `${workspaceDir}/${today}`;

// ---- 1. 建目录 ----
async function ensureFolder(path) {
  if (!(await vault.adapter.exists(path))) {
    await vault.createFolder(path);
  }
}
await ensureFolder(targetDir);
await ensureFolder(`${targetDir}/inbox`);
await ensureFolder(`${targetDir}/images`);

// ---- 2. 读取骨架模板 ----
const templatePath = `${workspaceDir}/TEMPLATE-daily.md`;
let skeleton = "";
if (await vault.adapter.exists(templatePath)) {
  skeleton = await vault.adapter.read(templatePath);
  skeleton = skeleton.replace(/^# YYYY-MM-DD/m, `# ${today}`);
} else {
  skeleton = `# ${today}\n\n## 待办\n\n### 跟进 / 派发\n\n- [ ] \n\n### 我的工作项\n\n- [ ] \n\n## 团队进展\n\n## 排期更新\n\n- \n\n## 知识 & 信息积累\n\n- \n\n## 原始材料\n\n- \n`;
}

// ---- 3. 找最近一份历史 daily.md，提取未勾选的「跟进/派发」项 ----
function listDailyDirs() {
  const folder = vault.getAbstractFileByPath(workspaceDir);
  if (!folder || !folder.children) return [];
  return folder.children
    .filter(f => f.children !== undefined && /^\d{4}-\d{2}-\d{2}$/.test(f.name) && f.name < today)
    .map(f => f.name)
    .sort()
    .reverse();
}

function extractFollowUpUnchecked(content) {
  // 匹配「### 跟进 / 派发」直到下一个「### 」或「## 」
  const m = content.match(/###\s*跟进\s*\/\s*派发\s*\n([\s\S]*?)(?=\n##\s|\n###\s|$)/);
  if (!m) return [];
  const section = m[1];
  const lines = section.split("\n");
  // 收集 - [ ] 行；同时保留紧跟在它之后的二级缩进子项（以两个空格或 tab 开头）
  const carry = [];
  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    if (/^\s*-\s*\[\s\]/.test(line)) {
      carry.push(line);
      // 把后面的子缩进行也带上
      let j = i + 1;
      while (j < lines.length && /^\s{2,}|\t/.test(lines[j]) && lines[j].trim() !== "") {
        carry.push(lines[j]);
        j++;
      }
    }
  }
  return carry;
}

let carriedLines = [];
let sourceDate = null;
for (const dir of listDailyDirs()) {
  const dailyPath = `${workspaceDir}/${dir}/daily.md`;
  if (await vault.adapter.exists(dailyPath)) {
    const content = await vault.adapter.read(dailyPath);
    const items = extractFollowUpUnchecked(content);
    if (items.length > 0) {
      carriedLines = items;
      sourceDate = dir;
    }
    break; // 只看最近一份；找到就停（无论有没有未完成项）
  }
}

// ---- 4. 注入顺延项到骨架的「跟进/派发」节 ----
if (carriedLines.length > 0) {
  const carryBlock = `\n> 以下条目从 ${sourceDate} 顺延而来，未完成项请继续跟进或明确标注完成。\n\n${carriedLines.join("\n")}\n`;
  skeleton = skeleton.replace(
    /(###\s*跟进\s*\/\s*派发\s*\n)([\s\S]*?)(?=\n###\s)/,
    `$1${carryBlock}\n`
  );
}

// ---- 5. 写入 daily.md（如已存在则不覆盖，仅打开） ----
const dailyPath = `${targetDir}/daily.md`;
if (!(await vault.adapter.exists(dailyPath))) {
  await vault.create(dailyPath, skeleton);
  new Notice(`✅ 已创建 ${dailyPath}` + (sourceDate ? `\n顺延 ${carriedLines.filter(l => /^-\s*\[\s\]/.test(l)).length} 条来自 ${sourceDate}` : ""));
} else {
  new Notice(`ℹ️ ${dailyPath} 已存在，直接打开`);
}

// ---- 6. 删除 Templater 自动新建的空文件，并打开真正的 daily.md ----
const createdFile = tp.file.find_tfile(tp.file.title);
if (createdFile && createdFile.path !== dailyPath) {
  await vault.delete(createdFile);
}
const dailyFile = vault.getAbstractFileByPath(dailyPath);
if (dailyFile) {
  await app.workspace.getLeaf(false).openFile(dailyFile);
}
-%>
