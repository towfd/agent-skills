# agent-skills

本倉庫收錄我們選用的 agent skill，並附上一支安裝程式。在專案資料夾中執行一道指令，即可將所需的 skill 安裝至該專案的 `.claude/skills/`。

## 安裝

請在要使用的專案資料夾中執行：

```bash
npx github:towfd/agent-skills list                     # 列出可安裝的 skill
npx github:towfd/agent-skills add                      # 顯示清單供您挑選
npx github:towfd/agent-skills add sharpen pause-safely # 安裝指定的 skill
npx github:towfd/agent-skills add --all                # 安裝全部
```

| 選項 | 說明 |
|---|---|
| `--dir <專案資料夾>` | 安裝至指定的專案；未指定時，安裝至目前所在的資料夾 |
| `--global` | 安裝至 `~/.claude/skills/`，所有專案皆可使用 |
| `--force` | 若已有同名的 skill，以新的內容覆蓋；未指定時會略過 |
| `--link` | 以連結取代複製，僅適用於從本機倉庫執行的情況：`node bin/cli.mjs add --all --link --dir <專案>` |

安裝完成後，需開啟新的對話才會載入新的 skill。執行環境需要 Node 18 以上版本，不需另外安裝其他套件。

## 收錄的 skill

| skill | 用途 | 啟動方式 |
|---|---|---|
| `sharpen` | 協助將任務問得更深入：先釐清專業人士會多做哪些事、會從哪些原始材料著手、採用哪些方法，以及如何證明結果正確，再據此改寫提示詞 | 輸入 `/sharpen` |
| `in-your-own-words` | 請 agent 以自己的話重述您的目標與想解決的問題，方便在動手前確認雙方理解一致 | 輸入 `/in-your-own-words` |
| `pause-safely` | 在安全的段落暫停工作，保存進度並留下交接說明，讓新開的對話可以接續進行 | 輸入 `/pause-safely` |
| `session-pickup` | 依據前一段對話留下的紀錄接手工作，避免重複已完成的部分 | 輸入 `/session-pickup` |
| `poteto-mode` | 整套做法的入口：開工前先重述目標、依任務類型選用對應的原則與劇本、規定 subagent 的使用方式與回覆寫法。資料夾內另附 `worker.md`（交付給 subagent 的工作守則）與 `playbooks/`（21 份劇本，各為一類工作的步驟，例如新功能、修 bug、重構、調查、原型） | 輸入 `/poteto-mode` |
| `principle-guard-the-context-window` | 對話內容接近上限時，將大量的閱讀與輸出交由 subagent 處理，主對話僅保留摘要 | 輸入 `/principle-guard-the-context-window` |
| `principle-laziness-protocol` | 優先考慮刪減，並以足以解決問題的最小幅度進行修改 | 輸入 `/principle-laziness-protocol` |
| `principle-subtract-before-you-add` | 新增內容之前，先移除不再需要的部分，再於較精簡的基礎上進行開發 | 輸入 `/principle-subtract-before-you-add` |
| 其餘 21 條 `principle-*` | 入口所引用的各項原則，分為核心、架構、驗證、委派、後設五類，例如 `principle-prove-it-works`、`principle-fix-root-causes`。完整清單請執行 `list` | 輸入 `/principle-<名稱>` |

## 來源與授權

目前收錄的 skill 皆取自 [pstack](https://github.com/cursor/plugins/tree/main/pstack)（作者 Lauren Tan，採 MIT 授權），對應版本為 `7a58391`。授權條款全文請見 [`LICENSE-pstack`](LICENSE-pstack)。

| skill | 原始檔案 | 調整內容 |
|---|---|---|
| `sharpen`、`in-your-own-words`、24 個 `principle-*` | `skills/<同名>/SKILL.md` | 未調整 |
| `pause-safely` | `skills/poteto-mode/playbooks/pause-safely.md` | 原始檔案為劇本中的一頁，不含 skill 所需的檔頭。我們僅在檔案開頭補上名稱、說明與啟動方式，內文維持原樣 |
| `session-pickup` | `skills/poteto-mode/playbooks/session-pickup.md` | 同上補上檔頭。另將第 1 步的對話紀錄位置由 Cursor 的路徑改為 Claude Code 的路徑 |
| `poteto-mode` | `skills/poteto-mode/SKILL.md`、`worker.md`、`playbooks/*.md` | `worker.md` 未調整。`SKILL.md` 與部分劇本將 Cursor 專有的寫法改為 Claude Code 的寫法，詳見下表。`autopilot-stack`、`babysit`、`investigation`、`multi-phase-plan`、`pause-safely`、`trace-forensics` 六份劇本未調整 |

### 由 Cursor 改為 Claude Code 的內容

原始檔案是針對 Cursor 撰寫。下列各處已改為 Claude Code 的對應寫法，用字盡量沿用 [pstack 的 Claude Code 移植版](https://github.com/michael-denyer/pstack-claude)；其餘內容維持原文。

| 檔案 | 原文 | 改為 |
|---|---|---|
| `session-pickup` 第 1 步 | 對話紀錄位於 `agent-transcripts/`，不得跨 `~/.cursor/projects/*/` 搜尋 | 對話紀錄位於 `~/.claude/projects/<encoded-cwd>/*.jsonl`，不得跨 `~/.claude/projects/` 下的其他資料夾搜尋 |
| `poteto-mode` 檔頭 | `icon`、`color` 兩個欄位 | 移除（Claude Code 不使用） |
| `poteto-mode` | `Task` subagent、Project worker、`Task` call、Task tool | `Agent` subagent、background worker、`Agent` call、`Agent` tool |
| `poteto-mode` | `/deslop` from the `cursor-team-kit` plugin | `/deslop` |
| `poteto-mode` | `control-ui` or `control-cli` from `cursor-team-kit` | Claude Code 內建的 `run`，以及專案的 `verify` skill |
| `poteto-mode` | Cursor's built-in babysit skill | the bundled **babysit** skill |
| `poteto-mode` | agent mode (readonly strips MCP) | full tool access (do not pick a subagent_type that strips MCP) |
| `poteto-mode` | `/setup-pstack` 寫入 `~/.cursor/rules/pstack-models.mdc`；舊版設定檔的相容說明 | `/setup-pstack` 寫入 `pstack-models.md`；相容說明移除 |
| `poteto-mode` | 未指定模型時改用 `generalPurpose` | 未指定模型時省略 `model` |
| `poteto-mode` | 模型代號 `claude-opus-5-5-xhigh-fast`、`claude-opus-5-5-high-fast`、`claude-fable-5-2-high`、`gemini-4-neon-xhigh`，以及 `-fast` 與 Gemini 的規定 | `opus`、`fable`、`sonnet` 搭配 effort `xhigh` 或 `high`。Claude Code 無法使用 Gemini，審查小組的第三席改為 `sonnet` |
| `poteto-mode` | another vendor's model | a model from another family |
| 劇本 `feature`、`bug-fix`、`refactoring`、`perf-issue`、`hillclimb` | 模型代號 `claude-opus-5-5-xhigh-fast` | `opus` at effort `xhigh` |
| 劇本 `eval` | 模型代號 `claude-opus-5-5-medium-fast`；對話紀錄位於 `agent-transcripts/` | `opus` at effort `medium`；對話紀錄位置同 `session-pickup` |
| 劇本 `session-pickup` | 對話紀錄位於 `agent-transcripts/` | 同獨立的 `session-pickup` skill |
| 劇本 `autonomous-run` | `AskQuestion`；Cursor's `/loop` command | `AskUserQuestion`；Claude Code's `/loop` command |
| 劇本 `bug-fix` | Cursor's `/loop` command | Claude Code's `/loop` command |
| 劇本 `autopilot-full`、`shipping` | 負責人與驗證者為 Cursor cloud agent；`cursor-team-kit` 的 `control-ui`、`control-cli`、`deslop` | 各自在獨立 worktree 中的 subagent；the driver skill；`/deslop` |
| 劇本 `bug-fix`、`perf-issue`、`prototype`、`refactoring`、`runtime-forensics`、`visual-parity` | the control skill | the driver skill |
| 劇本 `opening-a-pr` | `/deslop` from `cursor-team-kit` | `/deslop` |
| 劇本 `authoring-a-skill` | Cursor 內建的 **create-skill** | **skill-creator** |

尚未收錄的項目如下。入口或劇本引用到這些項目時，該步驟無法照原文執行，使用前請留意。

- 入口與劇本點名的其他 skill：`architect`、`swarm`、`arena`、`interrogate`、`unslop`、`technical-writing`、`no-comments`、`benchmark-checklist`、`show-me-your-work`、`figure-it-out`、`deslop`、`setup-pstack`，以及 agent 設定 `poteto-agent`。
- 劇本 `worktree-cleanup`：內容依賴為 Cursor 與 macOS 撰寫的盤點腳本，無法僅以替換用字對應，故未收錄。
- 劇本所用的附屬檔：`scripts/watch-pr/`（`babysit`、`shipping` 用於監看 PR）與 `references/bugbot-triage.md`（`babysit` 用於判斷機器人的審查留言）。
- 劇本中的 `origin` 指令為 Cursor 的程式碼託管服務。原文已載明預設使用 GitHub CLI（`gh`），僅在 `origin` 可用時才改用，因此未作調整。

## 倉庫內容

| 路徑 | 說明 |
|---|---|
| `skills/` | 各個 skill，每個 skill 一個資料夾 |
| `bin/cli.mjs` | 安裝程式 |
| `compare/` | 用來產生「原文與中文對照」網頁的程式，供挑選 skill 時閱讀原文。`compare/zh/` 為各原則與劇本的逐段中文對照 |
