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
| `poteto-mode` | 整套做法的入口：開工前先重述目標、依任務類型選用對應的原則與劇本、規定 subagent 的使用方式與回覆寫法。資料夾內另附 `worker.md`（交付給 subagent 的工作守則）、`playbooks/`（23 份劇本，各為一類工作的步驟，例如新功能、修 bug、重構、調查、原型、網頁設計）、`references/` 與 `scripts/`（劇本所用的判斷表與程式） | 輸入 `/poteto-mode` |
| `principle-guard-the-context-window` | 對話內容接近上限時，將大量的閱讀與輸出交由 subagent 處理，主對話僅保留摘要 | 輸入 `/principle-guard-the-context-window` |
| `principle-laziness-protocol` | 優先考慮刪減，並以足以解決問題的最小幅度進行修改 | 輸入 `/principle-laziness-protocol` |
| `principle-subtract-before-you-add` | 新增內容之前，先移除不再需要的部分，再於較精簡的基礎上進行開發 | 輸入 `/principle-subtract-before-you-add` |
| `unslop` | 清除文字中的 AI 腔，適用於回覆、文件與各類對外文字 | 輸入 `/unslop` |
| `technical-writing` | 撰寫技術文件、PR 說明與 commit 訊息的規範 | 輸入 `/technical-writing` |
| `no-comments` | 送審前清理程式中不必要的註解 | 輸入 `/no-comments` |
| `deslop` | 存檔前清除本次修改中帶有 AI 腔的程式碼 | 輸入 `/deslop` |
| `show-me-your-work` | 長時間或無人看管的工作中，逐筆記錄每個決定的內容、理由、證據與結果 | 輸入 `/show-me-your-work` |
| `figure-it-out` | 沒有合用的劇本時，為該項工作設計一份可供事後查核的做法 | 輸入 `/figure-it-out` |
| `architect` | 動手寫程式前，先定出型別、函式簽名與模組結構 | 輸入 `/architect` |
| `arena` | 讓多個 agent 就同一項任務各自產出一版，擇一為基礎，再併入其他版本的長處 | 輸入 `/arena` |
| `swarm` | 將工作分派給多個 agent 同時進行，彙整為一份報告 | 輸入 `/swarm` |
| `interrogate` | 由多個 agent 對一項修改或設計提出質疑，僅保留經實際執行證實的問題 | 輸入 `/interrogate` |
| `benchmark-checklist` | 回報或採用效能量測結果前的檢查清單 | 輸入 `/benchmark-checklist` |
| `create-verification-skill` | 為專案建立一份驗證用的 skill，以使用者的操作方式實際驅動應用程式 | 輸入 `/create-verification-skill` |
| `how`、`why`、`teach` | 說明某段程式如何運作、為何如此設計，或將一項工作完整講解清楚 | 輸入 `/how`、`/why`、`/teach` |
| `blast-radius` | 送出修改前，找出它可能在其他地方造成的影響 | 輸入 `/blast-radius` |
| `reflect`、`correct`、`recall` | 自對話中整理可長期保留的經驗、將反覆出現的錯誤轉為可攔截的檢查、重建近期的工作脈絡 | 輸入 `/reflect`、`/correct`、`/recall` |
| `ketchup`、`ketchup-video` | 彙整自上次查看以來的變動，以及等待使用者決定的事項 | 輸入 `/ketchup`、`/ketchup-video` |
| `poteto-help` | 說明整套做法的使用方式，並協助挑選合適的 skill、劇本或原則 | 輸入 `/poteto-help` |
| `website-brief` | 動手設計網站前，將需求寫成四節：目標與對象、頁面清單、各頁的區塊、文字草稿 | 輸入 `/website-brief` |
| `rwd-check` | 以瀏覽器在桌機、平板、手機三種寬度實際開啟網頁，截圖並量測內容是否超出畫面 | 輸入 `/rwd-check` |
| `frontend-design` | 設計畫面時的審美判斷：如何依主題做出有辨識度、不像套版的設計 | 設計畫面時自動載入，或輸入 `/frontend-design` |
| `speak-human-tw` | 去除繁體中文文字的 AI 腔，並校正中國用語與半形標點 | 提到去 AI 味時自動載入，或輸入 `/speak-human-tw` |
| 其餘 21 條 `principle-*` | 入口所引用的各項原則，分為核心、架構、驗證、委派、後設五類，例如 `principle-prove-it-works`、`principle-fix-root-causes`。完整清單請執行 `list` | 輸入 `/principle-<名稱>` |

## 來源與授權

收錄的 skill 多數取自 [pstack](https://github.com/cursor/plugins/tree/main/pstack)（作者 Lauren Tan，採 MIT 授權），對應版本為 `7a58391`。授權條款全文請見 [`LICENSE-pstack`](LICENSE-pstack)。其餘項目的來源列於下表。

pstack 原本是針對 Cursor 撰寫。原作者另外提供了 Claude Code 版（原倉庫的 `harness/pstack/claude-code/`），做法是不更動 skill 的內文，改以一份對照表說明 Cursor 的各個名稱在 Claude Code 中對應什麼，並在內文含有 Cursor 名稱的 skill 開頭加上一句，請 agent 每段對話先讀一次該對照表。本倉庫採用的即是這個版本，未自行改寫內文。

| 項目 | 原始檔案（未另外註明者，皆位於 pstack 原倉庫的 `harness/pstack/claude-code/`） | 調整內容 |
|---|---|---|
| `sharpen`、`in-your-own-words`、`unslop`、`technical-writing`、`no-comments`、`show-me-your-work`、`figure-it-out`、`architect`、`arena`、`swarm`、`interrogate`、`benchmark-checklist`、`create-verification-skill`、`how`、`why`、`teach`、`blast-radius`、`reflect`、`correct`、`recall`、`ketchup`、`ketchup-video`、`poteto-help`、24 個 `principle-*` | `skills/<同名>/`（含附屬的腳本與範本） | 未調整 |
| `deslop` | Cursor 另一個外掛 [`cursor-team-kit`](https://github.com/cursor/plugins/tree/main/cursor-team-kit) 的 `skills/deslop/SKILL.md`（Cursor，MIT 授權，條款見 [`LICENSE-cursor-team-kit`](LICENSE-cursor-team-kit)） | 未調整 |
| `poteto-mode` | `skills/poteto-mode/` 整個資料夾 | 入口的劇本名單增加 `Web design` 一項，並新增劇本 `playbooks/web-design.md`（本倉庫自行撰寫）。其餘未調整 |
| agent 設定 `poteto-agent`、`comment-sicko` | `agents/<同名>.md` | 未調整。位於本倉庫的 `agents/`，安裝時會一併放到 `.claude/agents/` |
| Claude Code 對照表 | `docs/harness/claude-code.md` | 未調整。位於本倉庫的 `docs/harness/`，安裝時會一併放到 `.claude/docs/harness/` |
| 使用指南 | `docs/guide/`（共十章） | 未調整。位於本倉庫的 `docs/guide/`，安裝時會一併放到 `.claude/docs/guide/` |
| `pause-safely` | `skills/poteto-mode/playbooks/pause-safely.md` | 原始檔案為劇本中的一頁，不含 skill 所需的檔頭。我們僅在檔案開頭補上名稱、說明與啟動方式，內文維持原樣 |
| `session-pickup` | `skills/poteto-mode/playbooks/session-pickup.md` | 同上補上檔頭。因內文含有 Cursor 的路徑，另在檔頭後加上「先讀對照表」那一句，用字與原作者版本相同 |
| `frontend-design` | Anthropic 的 [`anthropics/skills`](https://github.com/anthropics/skills/tree/main/skills/frontend-design)，版本 `41bbe19`（Apache 2.0 授權，條款見 [`skills/frontend-design/LICENSE.txt`](skills/frontend-design/LICENSE.txt)） | 未調整 |
| `speak-human-tw` | [`Raymondhou0917/speak-human-tw`](https://github.com/Raymondhou0917/speak-human-tw)，版本 `7fc6724`（作者 Raymond Hou，MIT 授權，條款見 [`skills/speak-human-tw/LICENSE`](skills/speak-human-tw/LICENSE)） | 未調整。僅收錄 `SKILL.md`、`references/`、`evals/` 與授權條款 |
| `website-brief`、`rwd-check`、劇本 `web-design` | 本倉庫自行撰寫 | 不適用 |

### 使用前請留意

- 對照表以 `/pstack:<name>` 稱呼各 skill、以 `pstack:poteto-agent` 稱呼 agent，並以 `<pstack>` 指稱同時含有 `skills/` 與 `docs/` 的資料夾。原作者是以外掛的形式發佈；本倉庫是將 skill 個別安裝至 `.claude/skills/`，因此實際的指令為 `/<name>`，agent 的名稱為 `poteto-agent`、`comment-sicko`，`<pstack>` 對應的則是專案的 `.claude/`。
- 劇本 `web-design` 會依序引用 `website-brief`、`frontend-design`、`speak-human-tw`、`rwd-check` 四個 skill，以及原有的「原型」與「功能」兩份劇本，請一併安裝。`rwd-check` 需要可操作瀏覽器的工具，例如 Playwright MCP。
- 尚未收錄的項目如下。入口或劇本引用到這些項目時，該步驟無法照原文執行。
  - 未收錄的 skill：`setup-pstack`、`tdd`、`typescript-best-practices`、`maintain-verification-skill`、`create-formal-verification-skill`、`maintain-formal-verification-skill`、`statechart`、`automate-me`、`make-bot-ui`、`bro`。`control-ui`、`control-cli` 屬於 Cursor 的另一個外掛 `cursor-team-kit`，同樣未收錄。
- `poteto-mode/scripts/` 內的程式（監看 PR、盤點 worktree）需要另行安裝 [Bun](https://bun.sh) 才能執行，其中盤點 worktree 的腳本是針對 Cursor 與 macOS 撰寫。

## 倉庫內容

| 路徑 | 說明 |
|---|---|
| `skills/` | 各個 skill，每個 skill 一個資料夾 |
| `bin/cli.mjs` | 安裝程式 |
| `agents/` | 入口與 `no-comments` 派工時使用的 agent 設定 |
| `docs/harness/claude-code.md` | 原作者撰寫的 Claude Code 對照表 |
| `docs/guide/` | 原作者撰寫的使用指南 |
| `compare/` | 用來產生「原文與中文對照」網頁的程式，供挑選 skill 時閱讀原文。`compare/zh/` 為各原則與劇本的逐段中文對照 |
