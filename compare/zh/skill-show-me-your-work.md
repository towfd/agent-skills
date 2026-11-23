TOPIC: 留下決策紀錄

---
name: show-me-your-work
description: 「替長時間或無人看管的工作留一份可以審查的決策軌跡：一個 TSV 紀錄檔，每個決定一列（做了什麼、為什麼、證據、結果）。預設只放在本機；當審查者需要這份軌跡才能信任結果時，就把它 commit 進去。用於 /show-me-your-work、自主或多階段的執行，或人離開一陣子後才回來審查的工作。」
disable-model-invocation: true（只有使用者打指令才啟動）
---

# 把過程攤開給我看

只維持一份作為正本的紀錄檔。

## 格式

單一個 TSV 檔，每個決定一列。每一格都只有一行。證據是一個指標，不是一段敘述。

複製 `references/decision-log-template.tsv`（就是標題列）來開一份乾淨的紀錄檔。欄位：

- **ts.** ISO8601 時間戳記。
- **phase.** 階段或工作線。
- **decision.** 選了什麼或做了什麼，一行。
- **why.** 用白話講的理由。如果是某個原則促成的，就白話說出來，不要寫成術語標籤。
- **evidence.** 能證明它的連結或路徑：commit SHA、PR 編號、`file:line`，或某個成品、追蹤紀錄或截圖的路徑。絕不是一段文字。
- **result.** 結果或判斷條件的狀態：`tests green`、`reverted`、`pixel-diff 0`、`INCONCLUSIVE`、`open`。

一個例子，用白話寫，讓審查者一眼就看懂。

```
ts	phase	decision	why	evidence	result
2026-05-24T09:02:00Z	frame	counted the work first, about 100 components and roughly 75 hours	wanted to know the size before starting a long run	commit 3a9f1c2	found 5 things to sort out before starting
2026-05-24T09:40:00Z	harness	took screenshots of the old version before changing anything	so we can compare old against new and catch any visual change	scripts/snapshot.sh, baseline/	saved 120 reference screenshots
2026-05-24T11:15:00Z	widget	moved the widget styles over without changing how it looks	keep the change small and the result identical	commit 7c21e0a, pixel-diff 0	looks identical, tests pass
2026-05-24T12:30:00Z	widget	threw out a helper's work because its screenshots were blank	checked the real files instead of trusting its summary	worktree reset	reverted, tightened the instructions for next time
```

## 記一列

每一筆都照你跟隊友說你做了什麼的方式寫。白話、具體的動作，不要 AI 腔的說法或抽象的術語（**unslop** skill 也適用於紀錄檔裡的文字）。

用輔助腳本 `scripts/log.sh <logfile> <phase> <decision> <why> <evidence> <result>`。它會自動填上 `ts`、第一次用時寫入標題列、去掉零散的 tab 和換行，並在任何以 `=`、`+`、`-` 或 `@` 開頭的格子前面加一個單引號。直接用 `printf` 附加一列也可以，但如果格子的內容來自程式產生或使用者提供的文字，要留意同樣那些字元。

記決策點和檢查點，不是每個動作都記：選了哪條岔路、完成一個單元連同它的驗證結果、一次轉向或退回連同觸發它的原因、浮現出來的阻礙、修好的關卡。迴圈式的執行，每一輪一列。瑣碎和不言自明的就跳過。

一次執行就是一段 agent 對話，包括它後面的回合和它的任何摘要。接手、換一個 agent 來做，或開新的對話，都算開始一次新的執行。當一次執行要往一份已經有列的紀錄檔裡加東西時，它的第一列 phase 是 `start`，在另一次執行的 `start` 列之後它寫的第一列也是。所以一次執行在之後的回合回到一份紀錄檔時，要先讀紀錄檔的最後幾列，看看在那之後有沒有別的執行寫過。一個 `start` 列要寫出它前面那些不是這次執行寫的列的 `ts` 範圍，它的 evidence 要寫出這次執行是誰，例如它的 agent id。phase `start` 不能用在其他地方。

## 放在哪裡

預設這份紀錄檔是工作過程中的成品，不 commit。把它放在工作目錄的 `decisions.tsv`，或者在好幾件工作同時進行時放在 `.audit/<task-slug>.tsv`，並且不要放進 git。

只有在工作夠有野心，大到審查者需要這份軌跡才能信任結果時，才 commit 它。

## 規則

- 只能往後加。判斷錯了，就加一列新的取代它。絕不編輯或刪除歷史。
- 證據優先用已經 commit 的腳本產生的，不要用手做的一次性東西（**encode-lessons-in-structure** 原則 skill）。

## 拿對話紀錄稽核紀錄檔

在執行結束、交回之前，檢查紀錄檔有沒有講真話。讀這次執行在目前工作區 `agent-transcripts/` 目錄下的對話紀錄（系統提示會寫出路徑）。不要跨 `~/.cursor/projects/*/` 去比對檔名。那會讀到不相干的私人對話。拿這次執行的列，逐一對照實際發生的事。這些列的每一段，從這次執行的某個 `start` 列開始，如果紀錄檔是這次執行建立的就從第一列開始，到另一次執行的下一個 `start` 列結束：

- 檢查每一列都對應到一個真實的決定或動作。
- 檢查每一列的證據找得到，而且顯示的正是那一列所說的。
- 影響了工作、卻沒有記下來的岔路、轉向或放棄的做法，就是缺口。把它加上去。

改正的是紀錄檔，不是說法。稽核絕不編輯或移除任何一列，就算是捏造的那一列也一樣。當一列記的既不是真實的決定、也不是真實的動作，或它的說法或證據是錯的，就加一列取代它，寫上實際發生的事和一個找得到的指標。這次稽核不檢查這次執行那幾段以外的列。如果這次執行自己的工作顯示其中某一列是錯的，就像處理任何判斷錯誤一樣，加一列取代它。

## 用別家的模型審查軌跡

交回之前，派一個 subagent，用的模型要來自跟做這份工作的模型不同的廠商。自己審自己不能取代它。這個 subagent 讀稽核軌跡和這次執行的對話紀錄，然後標出使用者該注意的地方。不是把工作重做一遍，而是掃一遍，找出不夠好或有風險的地方。依工作挑每個 subagent 的推理等級，照 **poteto-mode** skill 的 Subagents 那一節。

- 證據薄弱或沒有證據就記下的決定。
- 被跳過的驗證步驟，或在對話紀錄裡沒有證明就宣稱做過的驗證步驟。
- 事後看起來有風險的選擇（太早做、範圍蔓延、只是把症狀蓋住）。
- 使用者隨便掃過時會漏掉的缺口。

每一次有產生軌跡的執行，回覆都以一個「Attention」（注意）段落結尾。開頭單獨一行寫審查者的模型（`reviewed by <model>`），然後列出每一個標記，各自指向特定的列或時刻。「No flags」（沒有標記）是合法的值。模型名稱不是。

## 審查軌跡

從上讀到下，順著證據的指標去看，抽查。GitHub 會把 commit 進去的 TSV 顯示成表格。`column -s$'\t' -t decisions.tsv` 可以在終端機裡把它排出來。

## 跟其他 skill 組合

其他 skill 把它們的稽核軌跡導到這裡，不要自己發明一套。用名字引用它，讓它負責格式。不要重述欄位。
