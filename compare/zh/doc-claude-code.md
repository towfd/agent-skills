TOPIC: Cursor 名稱對照

# 在 Claude Code 裡用 pstack

pstack 的 skill 用的是 Cursor 的名稱。在 Claude Code 裡，每次對話讀這個檔一次，然後用下面的表格，把 skill 裡的每個 Cursor 名稱對應過來。`<pstack>` 指的是裝著 `skills/` 和 `docs/` 的那個資料夾。如果某個 Cursor 欄位在表裡沒有對應的列，就拿掉它，並說出來。絕不要傳工具 schema 不接受的欄位或值。

## 工具

| Cursor | Claude Code |
| --- | --- |
| `Task` | `Agent` |
| `AskQuestion` | `AskUserQuestion`。在 `-p` 模式下沒有這個工具，所以直接用文字問。 |
| 開一個待辦清單，或把步驟抄進待辦清單工具 | 如果這次對話有提供 `TodoWrite` 就用它。否則就把清單放在你的回覆裡，每個階段更新一次。 |
| 執行另一個 pstack skill（`/name` 或「**name** skill」） | 用 `Read` 讀 `<pstack>/skills/<name>/SKILL.md` 並照著做。`Skill` 工具會拒絕大部分的 pstack skill。當你要使用者自己打指令時，寫 `/pstack:<name>`。 |
| `Grep`、`Glob` | 對話裡沒有 `Grep` 或 `Glob` 時，用 `Bash` 跑 `rg`。 |

## Subagent 欄位

| Cursor | Claude Code |
| --- | --- |
| `subagent_type: generalPurpose` | `subagent_type: "general-purpose"` |
| `poteto-agent`、`comment-sicko` | `pstack:poteto-agent`、`pstack:comment-sicko` |
| `poteto-agent` 檔案裡的 `model:` 那一行 | 它寫的是 Cursor 的模型代號。每次用 `Agent` 派出 `pstack:poteto-agent` 時，都要傳 `model` 和 `effort`，用模型那張表對應過來，讓那個代號永遠不會送到 API。 |
| `readonly: true` | `subagent_type: "Explore"`。它還是有 `Bash`，所以交代任務時也要寫「do not edit files」（不要修改檔案），而且事後你要檢查 `git status`。 |
| `readonly: false` | `general-purpose`。它保有這次對話的 MCP 伺服器。 |
| `environment: "cloud"` | `isolation: "worktree"`。寫明工作者要切到哪個分支或 commit。 |
| `environment: "local"` | 省略。 |
| `cloud_base_branch: <b>` | 叫工作者先切到 `<b>`。 |
| `run_in_background: true` | 省略。Subagent 預設就在背景跑，跑完會通知你。 |
| `resume` | 派一個新的 agent，把之前的結果貼進給它的任務說明裡。 |
| `file_attachments` | 在任務說明裡列出路徑。 |

## 模型

| Cursor | Claude Code |
| --- | --- |
| `claude-<family>-<version>-<effort>[-fast]`，例如 `claude-opus-5-5-xhigh` | `model: "opus"` 和 `effort: "xhigh"`。`model` 只接受 `opus`、`sonnet`、`haiku`、`fable`。拿掉 `-fast`。 |
| `gemini-*` 或其他不是 Claude 的模型代號 | 省略 `model`，讓 agent 用這次對話的模型跑，並說出來。 |
| `auto` 或 `inherit-parent` | 省略 `model`。 |
| `pstack-models.mdc` 規則，`~/.cursor/rules/pstack-models.mdc` | `~/.claude/rules/pstack-models.md`。Claude Code 會把它載入每個新的對話，所以它的角色設定行已經在對話內容裡了。如果沒有，就讀那個檔。如果檔案或那個角色的那一行不存在，就用 skill 的預設模型代號。 |
| 角色的值 `<model> <effort>`，例如 `opus high` | `model: "opus"` 和 `effort: "high"`。 |

## setup-pstack

Claude Code 會把 `~/.claude/rules/` 裡的每個 `.md` 檔載入每個新的對話，所以 `setup-pstack` 把它的規則寫在那裡。照它的步驟做，但有這些改變：

- 偵測（Detect）。偵測到的模型，就是 `Agent` 工具 schema 列出的那些 `model` 值，每個都配上 schema 的 `effort` 值裡的一個 effort。實際的模型寫成 `<model> <effort>`，例如 `opus xhigh`。effort 是最後一個 token，所以預算那一步照原本寫的就能用。
- 預設值（Defaults）。用上面的列對應每個預設的模型代號：`claude-opus-5-5-xhigh-fast` 是 `opus xhigh`，`claude-opus-5-5-high-fast` 是 `opus high`，`claude-fable-5-2-high` 是 `fable high`，`gemini-4-neon-xhigh` 是 `inherit-parent`。
- 寫入（Write）。寫 `~/.claude/rules/pstack-models.md`，開頭不放檔頭，接著是註解行、`# budget` 那一行，以及第 5 步的每個角色各一行。整個檔案覆寫。絕不要把角色那幾行放進 `CLAUDE.md` 或 `AGENTS.md`。

## 路徑

| Cursor | Claude Code |
| --- | --- |
| `.cursor/skills/`、`~/.cursor/skills/` | `.claude/skills/`、`~/.claude/skills/` |
| `~/.cursor/plugins/`、`.cursor-plugin/plugin.json` | `~/.claude/plugins/`、`.claude-plugin/plugin.json` |
| `.cursor/rules/*.mdc`、一律套用的規則 | `CLAUDE.md`，沒有 `CLAUDE.md` 時用 `AGENTS.md`。Claude Code 從不讀 `.mdc` 檔。模型規則是例外。見模型那一節。 |
| `https://github.com/cursor/plugins/blob/main/pstack/<path>` | 那個檔存在時用 `<pstack>/<path>`。外掛裡附了這些 skill、`docs/guide/` 和 `README.md`。讀本機那份，絕不要上網抓。使用者需要連結時，給他們網址。 |
| `~/.cursor/projects/<slug>/agent-transcripts/` 裡的對話紀錄 | `~/.claude/projects/<slug>/<session>.jsonl`。slug 是把工作區路徑裡的每個 `/` 和 `.` 都換成 `-`，所以 `/Users/you/proj` 會變成 `-Users-you-proj`。直接放在那個資料夾裡、最新的那個 `.jsonl` 就是目前的對話。它的 `<session>/subagents/` 資料夾放著 subagent 的對話紀錄。只讀這個工作區的資料夾。 |

## Cursor 專有的功能

Claude Code 沒有 Cursor Automations、Bugbot、Cursor 雲端 agent，也沒有內建的 PR 工具。當某一步需要其中一個時，在你的回覆裡放一行 `Skipped in Claude Code: <step>. <reason>.`，然後繼續下一步。不要停下來、不要問、也不要重試。當後面的步驟需要被跳過的那一步產出的東西，例如一個網址或一把金鑰，就留一個佔位符，並在那一行裡寫出它的名字。

| Cursor | Claude Code |
| --- | --- |
| Cursor Automations：例行任務、`update_state` 的例行任務呼叫、`api2.cursor.sh/automations` 的 webhook、例行任務的喚醒，以及 `SendToUser` 的密鑰請求 | 跳過，並寫那一行。 |
| Bugbot | Bugbot 在 GitHub PR 上的留言就是一般的審查討論串，所以用那一步給的程式碼託管平台指令來分類處理。當 PR 沒有 Bugbot 的檢查或留言時，跳過啟動、等待或設定 Bugbot 的步驟。 |
| Cursor 雲端 agent | `environment: "cloud"` 對應到一個 worktree，就像 Subagent 欄位那一節。跳過需要雲端 agent 本身的步驟，例如它在儀表板上的狀態或它自己的機器。 |
| 內建的 PR 工具 | 用那一步給的程式碼託管平台指令，例如 `gh pr create`。這不算跳過，所以不用寫那一行。 |
