#!/usr/bin/env node
// 把這個倉庫 skills/ 裡的 skill 裝進一個專案的 .claude/skills/（或全域的 ~/.claude/skills/）。
// 沒有任何外部套件。用法見 help()。
import { readdirSync, readFileSync, existsSync, mkdirSync, cpSync, symlinkSync, rmSync, lstatSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { homedir } from 'node:os';
import { createInterface } from 'node:readline/promises';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const SRC = join(ROOT, 'skills');

function all() {
  return readdirSync(SRC, { withFileTypes: true })
    .filter(d => d.isDirectory() && existsSync(join(SRC, d.name, 'SKILL.md')))
    .map(d => {
      const text = readFileSync(join(SRC, d.name, 'SKILL.md'), 'utf8');
      const m = text.match(/^description:\s*"?(.*?)"?\s*$/m);
      return { name: d.name, description: m ? m[1] : '' };
    })
    .sort((a, b) => a.name.localeCompare(b.name));
}

function help() {
  console.log(`用法：
  agent-skills list                     列出有哪些 skill
  agent-skills add                      互動式：列出來讓你選
  agent-skills add <名字> [<名字>...]    裝指定的幾個
  agent-skills add --all                全部裝

選項：
  --dir <專案資料夾>   裝到那個專案的 .claude/skills/（預設是目前所在的資料夾）
  --global            裝到全域的 ~/.claude/skills/
  --link              不複製，改做連結（只適合從本機的倉庫執行，倉庫更新就跟著更新）
  --force             已經有同名的就蓋掉（預設是跳過）`);
}

function printList(skills) {
  skills.forEach((s, i) => console.log(`${String(i + 1).padStart(2)}. ${s.name}\n    ${s.description}`));
}

async function choose(skills) {
  printList(skills);
  const rl = createInterface({ input: process.stdin, output: process.stdout });
  const answer = (await rl.question('\n要裝哪幾個？輸入編號或名字，用空白隔開；全部就打 all；不裝就直接按 Enter：')).trim();
  rl.close();
  if (!answer) return [];
  if (answer === 'all') return skills.map(s => s.name);
  return answer.split(/[\s,]+/).map(t => (/^\d+$/.test(t) ? skills[Number(t) - 1]?.name : t)).filter(Boolean);
}

async function main() {
  const argv = process.argv.slice(2);
  const cmd = argv.shift();
  const skills = all();
  if (!cmd || cmd === 'help' || cmd === '--help' || cmd === '-h') return help();
  if (cmd === 'list') return printList(skills);
  if (cmd !== 'add') { console.error(`不認得的指令：${cmd}\n`); help(); process.exit(2); }

  const opt = { all: false, global: false, link: false, force: false, dir: process.cwd() };
  const names = [];
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--all') opt.all = true;
    else if (a === '--global') opt.global = true;
    else if (a === '--link') opt.link = true;
    else if (a === '--force') opt.force = true;
    else if (a === '--dir') opt.dir = resolve(argv[++i] ?? '');
    else if (a.startsWith('--')) { console.error(`不認得的選項：${a}`); process.exit(2); }
    else names.push(a);
  }

  let picked = opt.all ? skills.map(s => s.name) : names;
  if (!picked.length) {
    if (!process.stdin.isTTY) { console.error('沒有指定要裝哪些。請加上名字或 --all。現有的：\n'); printList(skills); process.exit(2); }
    picked = await choose(skills);
    if (!picked.length) return console.log('沒有選，什麼都沒裝。');
  }
  const known = new Set(skills.map(s => s.name));
  const unknown = picked.filter(n => !known.has(n));
  if (unknown.length) { console.error(`倉庫裡沒有這些 skill：${unknown.join('、')}`); process.exit(2); }

  const dest = opt.global ? join(homedir(), '.claude', 'skills') : join(opt.dir, '.claude', 'skills');
  mkdirSync(dest, { recursive: true });
  console.log(`裝到：${dest}`);
  for (const name of picked) {
    const to = join(dest, name);
    let exists = false;
    try { lstatSync(to); exists = true; } catch {}
    if (exists && !opt.force) { console.log(`  跳過 ${name}（已經有了，要蓋掉請加 --force）`); continue; }
    if (exists) rmSync(to, { recursive: true, force: true });
    if (opt.link) symlinkSync(join(SRC, name), to, 'dir'); else cpSync(join(SRC, name), to, { recursive: true });
    console.log(`  ${opt.link ? '連結' : '複製'} ${name}`);
  }
  // 對照表：skill 裡寫的是 ../../docs/harness/claude-code.md，所以放在 skills 資料夾的隔壁。
  const docFrom = join(ROOT, 'docs', 'harness', 'claude-code.md');
  const docTo = join(dest, '..', 'docs', 'harness', 'claude-code.md');
  mkdirSync(dirname(docTo), { recursive: true });
  rmSync(docTo, { force: true });
  if (opt.link) symlinkSync(docFrom, docTo, 'file'); else cpSync(docFrom, docTo);
  console.log(`  ${opt.link ? '連結' : '複製'} Claude Code 對照表 → ${docTo}`);
  console.log('好了。新開的對話才看得到新裝的 skill。');
}

main().catch(e => { console.error(e.message); process.exit(1); });
