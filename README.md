# agent-skills

挑選過的 agent skill，加上一支安裝程式。在專案裡下一道指令，就能把要用的 skill 裝進那個專案的 `.claude/skills/`。

## 安裝

在要用的專案資料夾裡：

```bash
npx github:towfd/agent-skills list                     # 看有哪些
npx github:towfd/agent-skills add                      # 列出來讓你挑
npx github:towfd/agent-skills add sharpen pause-safely # 裝指定的幾個
npx github:towfd/agent-skills add --all                # 全部裝
```

| 選項 | 作用 |
|---|---|
| `--dir <專案資料夾>` | 裝到別的專案，預設是目前所在的資料夾 |
| `--global` | 裝到 `~/.claude/skills/`，所有專案都看得到 |
| `--force` | 已經有同名的就蓋掉，預設是跳過 |
| `--link` | 不複製，改做連結。只適合從本機的倉庫執行：`node bin/cli.mjs add --all --link --dir <專案>` |

新開的對話才看得到新裝的 skill。需要 Node 18 以上，沒有其他相依套件。

## 有哪些 skill

| skill | 做什麼 | 啟動方式 |
|---|---|---|
| `sharpen` | 把一件任務變得更深而不是更大，然後改寫提示詞 | 打 `/sharpen` |
| `in-your-own-words` | 讓 agent 用自己的話重述你的目標和你想解決的問題 | 打 `/in-your-own-words` |
| `pause-safely` | 乾淨地停下來，留下一個讓全新的 agent 能接著做的檢查點 | 打 `/pause-safely` |
| `session-pickup` | 從前一段對話留下的紀錄接手，不重做 | 打 `/session-pickup` |
| `principle-guard-the-context-window` | 對話空間快滿時：大宗的東西交給 subagent，主對話只留摘要 | 打指令 |
| `principle-laziness-protocol` | 偏向刪除，以及能解決問題的最小改動 | 打指令 |
| `principle-subtract-before-you-add` | 先移除沒用的東西，再在比較簡單的基礎上往上蓋 | 打指令 |

## 來源與授權

目前的 skill 都來自 [pstack](https://github.com/cursor/plugins/tree/main/pstack)（作者 Lauren Tan，MIT 授權），取自版本 `7a58391`。授權全文在 [`LICENSE-pstack`](LICENSE-pstack)。

| skill | 原檔 | 改動 |
|---|---|---|
| `sharpen`、`in-your-own-words`、三個 `principle-*` | `skills/<同名>/SKILL.md` | 無 |
| `pause-safely`、`session-pickup` | `skills/poteto-mode/playbooks/<同名>.md` | 原檔是一頁劇本，沒有 skill 的開頭。只在最上面加了名字、說明和啟動方式，內文未改 |

原檔是為 Cursor 寫的。`session-pickup` 第 1 步提到的對話紀錄位置是 Cursor 的；兩份劇本提到的 `show-me-your-work`、`principle-prove-it-works` 這裡還沒有收。

## 倉庫裡有什麼

| 路徑 | 內容 |
|---|---|
| `skills/` | 每個 skill 一個資料夾 |
| `bin/cli.mjs` | 安裝程式 |
| `compare/` | 產生「原文和中文對照」網頁的程式，挑 skill 時用來讀原文 |
