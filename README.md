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
| `principle-guard-the-context-window` | 對話內容接近上限時，將大量的閱讀與輸出交由 subagent 處理，主對話僅保留摘要 | 輸入 `/principle-guard-the-context-window` |
| `principle-laziness-protocol` | 優先考慮刪減，並以足以解決問題的最小幅度進行修改 | 輸入 `/principle-laziness-protocol` |
| `principle-subtract-before-you-add` | 新增內容之前，先移除不再需要的部分，再於較精簡的基礎上進行開發 | 輸入 `/principle-subtract-before-you-add` |

## 來源與授權

目前收錄的 skill 皆取自 [pstack](https://github.com/cursor/plugins/tree/main/pstack)（作者 Lauren Tan，採 MIT 授權），對應版本為 `7a58391`。授權條款全文請見 [`LICENSE-pstack`](LICENSE-pstack)。

| skill | 原始檔案 | 調整內容 |
|---|---|---|
| `sharpen`、`in-your-own-words`、三個 `principle-*` | `skills/<同名>/SKILL.md` | 未調整 |
| `pause-safely`、`session-pickup` | `skills/poteto-mode/playbooks/<同名>.md` | 原始檔案為劇本中的一頁，不含 skill 所需的檔頭。我們僅在檔案開頭補上名稱、說明與啟動方式，內文維持原樣 |

原始檔案是針對 Cursor 撰寫，在 Claude Code 上有兩處尚未對應，使用前請留意。其一，`session-pickup` 第 1 步所指的對話紀錄位置為 Cursor 的路徑。其二，兩份劇本會引用 `show-me-your-work` 與 `principle-prove-it-works`，這兩個 skill 目前尚未收錄。

## 倉庫內容

| 路徑 | 說明 |
|---|---|
| `skills/` | 各個 skill，每個 skill 一個資料夾 |
| `bin/cli.mjs` | 安裝程式 |
| `compare/` | 用來產生「原文與中文對照」網頁的程式，供挑選 skill 時閱讀原文 |
