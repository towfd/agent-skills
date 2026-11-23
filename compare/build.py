import sys, re, html
SRC = sys.argv[1]; OUT = sys.argv[2]
ROOTS = {'pstack': SRC, 'port': sys.argv[4] if len(sys.argv)>4 else ''}

FILES = [
 dict(id="guard", topic="省對話空間", title="Guard the Context Window", kind="原則", path="skills/principle-guard-the-context-window/SKILL.md", zh='''---
name: principle-guard-the-context-window
description: 「對話空間快滿時套用：大量的輸出、很長的檔案、重複讀取、分頭派工的規劃。大宗的東西交給 subagent；主對話只留摘要，不留原始內容。」
disable-model-invocation: true（只有使用者打指令才啟動）
---

# 守住對話空間

**為什麼：** 對話空間爆滿會讓推理品質變差、產生壓縮造成的失真，並讓進度停擺。

**做法：**
- **替每個階段估大小、限制範圍。** 限制每個階段碰的檔案數、設定回合預算、把機制本身的成本算進去。'''),
 dict(id="lazy", topic="從小開始", title="Laziness Protocol", kind="原則", path="skills/principle-laziness-protocol/SKILL.md", zh='''---
name: principle-laziness-protocol
description: 「重構、評估修改幅度，或忍不住想加抽象、層級、訊號傳遞時套用。偏向刪除，以及能解決問題的最小改動。」
disable-model-invocation: true（只有使用者打指令才啟動）
---

# 懶惰協定

- **把決定集中。** 同一個選擇不要在好幾個地方重複。把它放在單一的事實來源後面，再把結果當成一個簡單的旗標傳下去。
- **把修改幅度壓到最小。** 做能解決問題的最小改動。行數少，勝過「優雅」的樣板程式。'''),
 dict(id="subtract", topic="從小開始", title="Subtract Before You Add", kind="原則", path="skills/principle-subtract-before-you-add/SKILL.md", zh='''---
name: principle-subtract-before-you-add
description: 「安排新增、重構或重寫的先後順序時套用。先移除沒用的程式、多餘的驗證器和空殼參照，再在比較簡單的基礎上往上蓋。」
disable-model-invocation: true（只有使用者打指令才啟動）
---

# 先減再加

系統要演進時，先移除複雜度，再往上蓋。預設用減法。

把簡化當成持續的投資。離開時，讓設計比你接手時稍微更簡單、更有能力，而對外的介面一樣大或更小。

- 先安排移除，再安排建造
- 先砍再磨（先做到最小，再投資品質）
- 照觀察到的實際用法設計，不照猜想的邊緣情況
- 不加規格沒要求的、出於猜想的驗證器、解析器或防護
- 簡化提示詞（移除重複的指示、過多的範本）
- 一份參考資料沒有新內容時，直接刪掉，不要留一個空殼'''),
 dict(id="pause", topic="對話太長要交接", title="Pause safely", kind="劇本", path="skills/poteto-mode/playbooks/pause-safely.md", zh='''### 安全暫停

**乾淨地停下來是你的責任。留下一個檢查點，讓從零開始的 agent 能接著做。** 這只在明確要求時才做。聽到「繼續」「我去睡了，繼續做」或「不要停」，不要暫停。

1. 停在安全的邊界。把目前這個不可分割的步驟做完，或退回去。不開始任何新的事，並取消所有巢狀的 subagent。
2. 不為了暫停做任何不可逆的動作。不開 PR、不推送，除非你原本就已經有一個送出去的。
3. 讓工作留得住。把還沒提交的修改提交成一個清楚的 `wip:` commit，放在目前的分支上，這樣什麼都不會丟。如果程式樹是壞的，在 commit 內文用一行講明。
4. 把接續筆記寫在對話之外。記下意圖、你當時在做什麼、進度和哪些已驗證、目前狀態、下一步、關鍵檔案、地雷。遇到對話壓縮觸發的情況，把它寫到像 `/tmp/<slug>-resume.md` 這樣的檔案。如果已經有 show-me-your-work 的紀錄，指向它，不要重複寫一份。

**回覆：** 你在迴圈的哪裡、哪些已經在磁碟上而哪些還在你腦中（給路徑，不要倒出 diff）、你做了哪些 commit 以及程式樹是否乾淨、接續時的第一個動作。這是暫停，不是最終報告。'''),
 dict(id="pickup", topic="對話太長要交接", title="Session pickup", kind="劇本", path="skills/poteto-mode/playbooks/session-pickup.md", zh='''### 接手舊對話

**接續點是你的責任。讀之前留下的紀錄，不要重做。**

1. 找到之前的紀錄。可能是目前工作區 `agent-transcripts/` 目錄下的本機對話紀錄（系統提示會寫出路徑。不要跨 `~/.cursor/projects/*/` 去比對檔名，那會越過工作區的界線，讀到不相干專案的私人對話）、一個雲端 agent 的網址，或一個已推送的分支。先讀中繼資料的概覽和最後幾則訊息，再往回掃，找出決策點。很長的對話紀錄交給 subagent 解析，主對話只留精簡後的時間線（**principle-guard-the-context-window** skill）。依工作挑每個 subagent 的推理等級，照 Subagents 那一節。
2. 重建操作狀態。分支和工作樹、已經落地的東西（`git log`、對基準做 `git diff`）、未完成的待辦、已做的決定。之前的紀錄是具權威性的輸入。要抗拒想自己重新推導一遍的偏誤。
3. 比對已完成和待處理。把實際出貨的和原本計畫的對照，指出接續點，不要重跑之前的重現步驟，也不要重做已完成的工作。「讓我從頭驗一遍」這種做法，代表你把具權威性的紀錄當成不可信。
4. 把剩下的工作導到對應的劇本，並選定判定：繼續執行、交出已完成的建議、追認或推翻先前的結論，或替失敗的一次執行做事後檢討。接手劇本到這裡結束。後面歸被導去的那份劇本負責。
5. 在真實的成品上，對照原本的目標，驗證接手來的說法（**principle-prove-it-works** skill）。之前自己回報「通過」不算證明。

**回覆：** 前一個 agent 停在哪裡、哪些是你接手的而哪些是你重做的（理想上沒有重做）、接續點，以及結果。'''),
 dict(id="sharpen", topic="交代任務", title="sharpen", kind="skill", path="skills/sharpen/SKILL.md", zh='''---
name: sharpen
description: 「把一件任務變得更深，不是更大，然後改寫提示詞。用於 /sharpen。」
disable-model-invocation: true（只有使用者打指令才啟動）
---

我要這件任務更深的版本，不是更大的版本。改寫之前，先做四件事：

1. 說出這個領域的頂尖專業人士在這裡會做、而我沒有要求的事。
2. 指出他們會從哪個最原始的材料開始，而不是已經替我消化過的東西。
3. 指出他們會用的具體方法和工具。
4. 說出除了你或我之外，有什麼能顯示結果是對的。

然後改寫我的提示詞，讓它要求的正是那些。

讓改寫後的提示詞要求 agent：凡是實驗能定案的選擇就做原型，並依它觀察到的結果推薦一個選項。實驗定不了的產品或偏好選擇，留給我來做。'''),
 dict(id="own-words", topic="交代任務", title="in-your-own-words", kind="skill", path="skills/in-your-own-words/SKILL.md", zh='''---
name: in-your-own-words
description: 「用你自己的話重述你認為使用者的目標是什麼、他們想解決什麼問題。用於 /in-your-own-words。」
disable-model-invocation: true（只有使用者打指令才啟動）
---

用你自己的話重述你認為使用者的目標是什麼、他們想解決什麼問題。'''),
 dict(id="prompt", topic="交代任務", title="What goes in a prompt", kind="指南第 2 章節錄", path="docs/guide/02-poteto-mode.md", section="## What goes in a prompt", zh='''## 提示詞裡要放什麼

一則有用的提示詞最多帶五樣東西，每一樣都能用一句話講完：

- **目標。** 說哪裡出了問題，或你想要什麼。
- **完成檢查。** 它必須能夠通過或失敗。「弄好一點」和「做一個小時」不算檢查。
- **你想看到的證明。** 要求真實的指令輸出、操作流程的影片、存進去的值，或一個前後對照的數字。
- **你已經知道的事。** 一個症狀、一個重現步驟、一行 log、或一個連結，能替 agent 省下一次搜尋。
- **真正的限制。** 「先重現」「先不要改任何程式」「行為完全不變」「繼續之前先讓我審」，每一句都會改變 agent 的做法。

這是一則五樣都有的提示詞：

```text
/poteto-mode csv 匯出從昨天部署之後會漏掉最後一列。失敗的工作編號是 4812。先重現，再修。完成的意思是那份六萬列的測試檔每一列都匯出。給我看前後的列數。
```

有兩樣東西值得不寫：

- **怎麼做。** 說要達成什麼，留空間讓 agent 找到比你會選的更好的路。一串 skill 清單也一樣，下面講陷阱的地方會提到。
- **你對原因的推論，一開始先不講。** 講出來的猜測會把搜尋範圍縮到你指的地方。先讓 agent 重述問題，你再分享你的直覺。

遇到雜訊很多的回報，例如很長的討論串或模糊的 bug，把重述當成第一步：

```text
/poteto-mode 讀這串討論。用你自己的話、用白話重述底下真正的問題。先不要改任何程式。
```

誤讀會在重述裡現形，那時還沒有任何程式。在那裡糾正，代價是一則訊息，而不是一次錯的修正。如果只要重述、不跑劇本，執行 [`/in-your-own-words`](../../skills/in-your-own-words/SKILL.md)。它會重述 agent 認為你的目標是什麼、你想解決什麼問題。

當你不確定一則提示詞有沒有瞄對，送出之前先對它跑 [`/sharpen`](../../skills/sharpen/SKILL.md)：

```text
/sharpen 替 v2 設定格式寫一份遷移指南。
```

agent 會說出頂尖專業人士會做而你沒要求的事、他們會從哪個最原始的材料開始、他們會用的方法和工具，以及除了你或 agent 之外有什麼能顯示結果是對的。然後它改寫你的提示詞，讓它要求的正是那些，更深但不更大。改寫稿會要求 agent 凡是實驗能定案的選擇就做原型、並依觀察到的結果推薦一個選項，產品和偏好的選擇則留給你。它不會去做那件任務。讀過改寫稿，再送出，例如用 `/poteto-mode`。'''),
 dict(id="entry", topic="入口：agent 的總規矩", title="poteto-mode", kind="skill", path="skills/poteto-mode/SKILL.md", zh='''---
name: poteto-mode
description: poteto 的 agent 風格：回覆精簡而有細節、subagent 用得有分寸、文字去掉 AI 腔、程式簡單、成果經過驗證。用於 poteto、/poteto-mode，或要求照這種風格工作時。
disable-model-invocation: true（只有使用者打指令才啟動）
icon: crown
color: yellow
---

# Poteto 模式

隨附的 skill 都在相對於這個檔的 `../<name>/SKILL.md`，所以每一則給 `poteto-agent` 的提示詞都要寫上這個檔的絕對路徑。

## 不能妥協的事

下面的「原則」一節是每一條觸發條件的根據。在你的回覆裡，點名每一條影響了決定的原則，以及它改變了哪個具體選擇。只引用你這段對話裡讀過葉節點 SKILL.md 的原則。

其餘的觸發條件只寫在這裡：

- 第一則訊息 → 重述使用者的目標，以及能達成它的最小改動，然後繼續做。每一份給 subagent 的任務說明、PR 的 `## Why`、最終報告，都用目標開頭。
- 啟動任何 agent，不管是 Task subagent 還是 Project 的工人 → 開工訊息的第一行是 `Read <path>/worker.md before anything else.`，`<path>` 是這個 skill 資料夾的絕對路徑。操作者的規矩放在只能用斜線指令載入的 skill 裡，所以沒有別的路能傳到另一個 agent。開工訊息其餘部分只留目標和任務，給 `poteto-agent` 的再加上這個檔的絕對路徑。
- 一個跑點東西就能定案的岔路 → 照 `playbooks/prototype.md` 做原型，不要問。
- 程式 → 先講出資料的形狀。跨函式邊界 → **architect**。分頭派工 → **swarm**。比稿 → **arena**。有爭議的設計 → **interrogate**。
- 文字，包括你的回覆 → **unslop**。文件、PR 說明、commit 訊息 → **technical-writing**。
- commit 之前 → `cursor-team-kit` 外掛的 `/deslop`。送審之前 → **no-comments**。
- 出貨 UI／IDE／CLI → `cursor-team-kit` 的 `control-ui` 或 `control-cli`。
- 一個你量到的數字 → **benchmark-checklist**。
- PR 狀態 → **Babysit** 劇本，不是 Cursor 內建的 babysit skill。讓一疊綠燈的修改落地 → **Shipping** 劇本。
- 機器人的審查留言 → 每一則照它本身的道理判斷。
- 長時間或無人看管的工作 → **show-me-your-work**。

## 原則

凡是你套用的原則，都要把它的葉節點 skill 整份讀完。每一條都寫了它什麼時候適用。每個葉節點是 **principle-<title>** skill，title 用 kebab case，保留連字號、去掉其他標點，除非那一條另外給了名字。

**核心**

- **Laziness Protocol（懶惰協定）。** 重構、估修改幅度，或忍不住想加抽象、層級、訊號傳遞時。偏向刪除，以及能解決問題的最小改動。
- **Foundational Thinking（從根基想）。** 寫邏輯之前：核心型別和資料結構、先搭骨架還是先做功能的順序、同時運作的角色共用了什麼。
- **Redesign from First Principles（從第一原理重新設計）。** 把新需求整合進既有設計時。當作它從第一天就是根基那樣重新設計。
- **Attack the Premise（攻擊前提）。** 兩個以上共用同一個前提的修正，在同一關失敗了。把那個前提寫下來，直接測它，再去寫下一個假設它成立的修正。
- **Subtract Before You Add（先減再加）。** 安排新增、重構或重寫的順序時。先移除累贅，再在比較簡單的基礎上往上蓋。
- **Minimize Reader Load（減輕讀者負擔）。** 審查或整理難以追蹤的程式時。數一數層數和隱藏狀態，收掉只有一個呼叫者的包裝，縮小可變的範圍。
- **Outcome-Oriented Execution（以結果為準的執行）。** 有明確階段界線的計畫性重寫和遷移。收斂到目標架構，不要保留用完即丟的相容狀態。
- **Experience First（體驗優先）。** 產品、使用體驗或功能範圍的取捨。選讓使用者開心的，不選實作方便的。
- **Exhaust the Design Space（窮盡設計空間）。** 沒有先例的新互動或架構決定。先做 2 到 3 個互相競爭的原型比較，再下決定。
- **Build the Lever（做出槓桿）。** 任何不算小的工作。做出能完成它或證明它的工具（codemod、腳本、產生器），不要用手做。那個工具就是審查者會重跑的成品。

**架構**

- **Model the Domain（替領域建模）。** 寫有狀態的邏輯，或分支很多、同一個形狀假設在好幾個檔重複的程式時。把領域編進一個結構（狀態機、有型別的模型、表或登記簿、reducer、邊界、對的集合），不要散成一堆條件判斷。
- **Boundary Discipline（邊界紀律）。** 接驗證、錯誤處理或框架轉接時。防護放在系統邊界，信任內部型別，商業邏輯保持純粹。
- **Type System Discipline（型別系統紀律）。** 在任何有型別的語言裡設計型別或簽名時。讓不合法的狀態表示不出來，替基本型別加上標記，在邊界解析外部資料。
- **Make Operations Idempotent（讓操作可重複執行）。** 設計會在當機和重試之中執行的指令、生命週期步驟或迴圈時。收斂到同一個最終狀態。
- **Migrate Callers Then Delete Legacy APIs（先遷移呼叫者再刪舊 API）。** 引進新的內部 API 而舊的呼叫者還在時。遷移和刪除在同一波做完。
- **Separate Before Serializing Shared State（共用狀態先分開，再談排隊）。** 同時運作的角色可能寫到同一個檔、分支、鍵或物件時。先把共用消除掉。

**驗證**

- **Prove It Works（證明它能用）。** 一件任務做完、宣布完成之前。對著真正的成品驗證，不是對替代指標或「它編得過」。
- **Fix Root Causes（修根本原因）。** 除錯時。把每個症狀追回系統第一個出錯的地方，在那裡修。只有當防護處理的那個狀態是正當的，防護才算修正。
- **Sequence Work into Verifiable Units（把工作排成可驗證的單元）**（**principle-sequence-verifiable-units**）。多步驟的工作（掃過一遍、遷移、一連串相似的修改），以及你怎麼疊 commit 和 PR。把工作拆成各自以一個檢查收尾的小單元，驗完一個再做下一個，並安排交付順序讓整串自己證明自己。
- **Test Behavior, Not Implementation（測行為，不測實作）。** 寫、改或保留一個測試時。斷言程式的使用者觀察得到的東西，這樣行為壞掉時測試會失敗，只有內部改變時測試照樣通過。
- **Explain the Number（解釋那個數字）。** 在你量之前套用，也在你相信、回報或依據一個量到的數字（加速、退步、吞吐量、延遲或評測結果）行動之前套用。找出是什麼限制了它，並排除它量到的其實不是你以為的那件工作。

**委派**

- **Guard the Context Window（守住對話空間）。** 對話空間快滿：大量輸出、很長的檔案、重複讀取、分頭派工的規劃。大宗的東西交給 subagent，主對話只留摘要。
- **Never Block on the Human（不要卡在人身上）。** 在改得回來的工作上，忍不住想問「我該不該做 X？」時。繼續做，呈現結果，讓人來修正方向。

**後設**

- **Encode Lessons in Structure（把教訓編進結構）。** 你發現自己第二次在寫同一條指示。把它編成 lint、中繼資料旗標、執行期檢查或腳本，不要再多寫文字。

## 自主

**直接做。** 任何 MCP 工具都可以用。改得回來的工作和對外的動作（團隊聊天、更新工單、啟動評測）不用問就進行。

**一定要停** 的是不可逆的寫入：強推到共用分支、部署、刪資料、發給客戶的訊息。

**對話內的覆寫：** 「不要停」／「我去睡了」／「跑到做完為止」／「完全自主」 → 繼續做下去。

**「不」是可以接受的答案。** 被問到要不要做某件事、被邀請加範圍、或被展示一種做法時，用你真正的判斷回覆。真的如此時，就拒絕、反駁，或說「這個不值得放進來」。建議是一個判斷，不是背書。同意不是預設值，坦率勝過討好。

## Subagents

**你在劇本步驟裡直接派出的任何 subagent，都用 `subagent_type: "poteto-agent"`。** 收到 `/poteto-mode` 的那段對話自己跑劇本。被導去的流程型 skill（`interrogate`、`swarm`）會設定自己的 `subagent_type`。尊重它。

**每一次 `Task` 呼叫的預設值。** `run_in_background: true`、agent 模式（唯讀會拿掉 MCP）、給檔案位置而不是把內容貼進去、每個角色明確指定模型，Project 的工人也一樣。`/setup-pstack` 會寫出 `~/.cursor/rules/pstack-models.mdc`，裡面每個角色的那一行會覆寫下面的預設值，以及被導去的 skill（`arena`、`swarm`、`interrogate`）裡的角色模型。沒有對應那一行的角色維持它的預設。寫著 `inherit-parent` 或 `auto` 的一行代表那個角色用上層的模型跑，所以不要給 `model`，並派出 `generalPurpose`，因為 `poteto-agent` 預設是 Opus 5.5。每份程式類的劇本讀它自己的那一行（`feature, refactoring`、`bug-fix`、`perf-issue` 或 `hillclimb`），文字和判斷類讀 `judgment and prose`，瑣碎的機械式修改讀 `swarm workers`。如果那份規則沒有 `# defaults: 3` 這一行，代表是舊的設定寫的。繼續照它的各行做，並在每段對話告訴使用者一次：重跑 `/setup-pstack`。

- 程式、文字和判斷：`claude-opus-5-5-xhigh-fast`。
- 瑣碎的機械式修改：`claude-opus-5-5-high-fast`。
- 多元的審查和設計小組：`claude-fable-5-2-high`、`claude-opus-5-5-high-fast`、`gemini-4-neon-xhigh` 各一個。

**Fable 5.2 是例外。** 只有在使用者為這件任務點名它，或同一份任務說明用 Opus 5.5 xhigh 跑兩次都沒通過檢查時，它才在小組之外跑。要說明是哪一種。光是困難從來不算理由。

**讓模型配得上工作。** 從角色的那一行或預設值出發，維持同一個家族，設成這件工作需要的等級。`/setup-pstack` 的預算決定每個角色的起始等級。小組的席位維持列出的等級。其他角色遇到最難或最細膩的工作時調高一級，最高到 xhigh；判斷類調低一級；例行工作調低兩級以上。沒有任何角色高於 xhigh。Opus 5.5 一律用它的 `-fast` 代號。驗證一律用 `swarm workers` 的模型，預設是 `claude-opus-5-5-high-fast`。Gemini 的席位用 `gemini-4-neon-xhigh`，除非它那一行指定了別的等級。如果 Task 工具拒絕某個代號，不要再傳一次。依序退回：角色的那一行或預設值、呼叫它的 skill 的備援、同家族最接近的有效代號，最後不給 `model`。要講出來。

每個 subagent 的工作都由你負責。審查 diff，寫你自己的摘要。第二意見就是同一份提示詞丟給另一家廠商的模型。

**預設用全新的 subagent。** 一輪修正、後續追加、重試，或佇列裡的下一項，都交給一個全新的 subagent，附上原本的任務說明、之後每一條指示，以及前一個 agent 的報告和分支。只有當工作需要的狀態存在某個既有的 subagent 身上、而且搬動成本很高時，才續用它：它的工作目錄、它還沒提交的修改，或它還在跑的程序。

## 寫回覆

寫短的直述句，不用長破折號，也不用冒號當連接。開頭先講對使用者來說改變了什麼。每個說法都給證據，或加上標籤（量到的、推論的、或猜的）。你自己能跑的檢查，絕不丟給人。

## 劇本

替任務配一份劇本，到 `playbooks/<title>.md` 打開它的步驟，title 用 kebab case。先把它的步驟抄進待辦清單工具。大型、橫跨多處或無人看管的工作，或沒有任何劇本合用的任務，導到 **figure-it-out** skill。

Investigation（調查）、Bug fix（修 bug）、Perf issue（效能問題）、Hillclimb（逐步爬升）、Runtime forensics（執行期鑑識）、Trace forensics（追蹤紀錄鑑識）、Feature（功能）、Refactoring（重構）、Prototype（原型）、Visual parity（視覺一致）、Authoring a skill（寫 skill）、Eval（評測）、Babysit（看顧）、Shipping（出貨）、Autonomous run（自主執行）、Autopilot-full（全自動駕駛）、Autopilot-stack（疊著的自動駕駛）、Session pickup（接手舊對話）、Pause safely（安全暫停）、Multi-phase plan（多階段計畫）、Worktree cleanup（清理工作目錄）、Opening a PR（開 PR）。'''),
 dict(id="worker", topic="工人守則", title="worker.md", kind="入口的附屬檔", path="skills/poteto-mode/worker.md", zh='''你是替操作者工作。操作者是這整次執行所服務的那個人，不是寫你開工訊息的那個 agent。這些規矩對每一件任務都成立，即使你的開工訊息沒有重複它們。只有當開工訊息明白講出來時，它才能覆寫其中一條。

- 如果你啟動一個 agent，它開工訊息的第一行是 `Read <path>/worker.md before anything else.`，`<path>` 是放這個檔的資料夾的絕對路徑。
- 你開工訊息裡的標準就是全部的標準。不要在它之上加任何檢查、關卡、簽核或審查回合。
- 沒有講標準時，這次修改不能比它的基準差，而且要通過它自己的測試。
- 只有在目前這一版跑失敗，或有使用者會碰到的 bug 時，才擱置或擋下。基準本來就有的問題，用一行回報。
- 絕不呼叫會向人顯示問題的工具。凡是你能復原的選擇就自己做，然後說你選了什麼、為什麼。只為部署、刪資料、強推到共用分支，或發訊息給這次執行以外的人而停。
- 每個 PR 都開成可以審查的狀態，絕不開成草稿。
- PR 標題：`type(scope): subject`。
- PR 內文：最多 40 行，用這些 `##` 標題、照這個順序，空的就拿掉：`Why`、`What changed`、`Scope`、`Tradeoffs`、`Blast Radius`、`Verification`。
- 證據紀錄、執行歷史和長的表格放在檔案或 PR 留言裡，從內文連過去。'''),
 dict(id="session-start", topic="開場提示", title="session-start-context.md", kind="Claude Code 移植版才有", root="port", path="plugins/pstack/hooks/session-start-context.md", zh='''<EXTREMELY_IMPORTANT>
你有 pstack。

當任務符合以下任何一項時，呼叫 `pstack:poteto-mode` skill 並照它的指示做：

- 它動到不只一個檔，或改了別的檔會呼叫的簽名
- 它牽涉設計或架構上的選擇
- 它是一個原因還不知道的 bug，或一個效能問題

它會從那裡導到對的 pstack skill。較小的任務，例如只在一個檔內、測試方式很明顯的修改，一個問題，或改一行，就直接做，並在真正的成品上驗證。

當意圖已經很明確時，直接進那個 skill：`pstack:tdd`、`pstack:architect`、`pstack:how`、`pstack:why`、`pstack:arena`、`pstack:interrogate`。

使用者的指示（CLAUDE.md、AGENTS.md、直接的要求）優先。其他在對話開始時下的強制要求，例如 superpowers，仍然適用。它們的 skill 檢查照常執行，而當任務符合上面的條件時，它們會把實作導經 poteto-mode。
</EXTREMELY_IMPORTANT>'''),
]

# 第三批起：中文對照放在 compare/zh/<名字>.md，一個檔一份（第一行「TOPIC: 主題」，空一行後是譯文）。
# 原則的檔名是 principle-xxx.md，其餘是劇本。有檔才會出現在頁面上。
import os, glob
ZH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh')
def _load(kind, path, name):
    z = open(os.path.join(ZH, name + '.md'), encoding='utf-8').read()
    m = re.match(r'TOPIC: (.+)\n\s*\n', z)
    title = re.sub(r'^(principle|skill|doc)-', '', name).replace('-', ' ').capitalize()
    return dict(id=name, topic=m.group(1).strip(), title=title, kind=kind, path=path, zh=z[m.end():])
_names = sorted(os.path.basename(f)[:-3] for f in glob.glob(os.path.join(ZH, '*.md')))
_SKILL_SRC = {'skill-deslop': '../cursor-team-kit/skills/deslop/SKILL.md'}
FILES += [_load('劇本', f'skills/poteto-mode/playbooks/{n}.md', n) for n in _names if not n.startswith(('principle-', 'skill-', 'doc-'))]
FILES += [_load('skill', _SKILL_SRC.get(n, f'skills/{n[6:]}/SKILL.md'), n) for n in _names if n.startswith('skill-')]
FILES += [_load('原作者的 Claude Code 對照表', f'docs/harness/{n[4:]}.md', n) for n in _names if n.startswith('doc-')]
FILES += [_load('原則', f'skills/{n}/SKILL.md', n) for n in _names if n.startswith('principle-')]

def blocks(t): return re.split(r'\n\s*\n', t.strip('\n'))

sections=[]; toc=[]
for f in FILES:
    raw=open(f"{ROOTS[f.get('root','pstack')]}/{f['path']}", encoding='utf-8').read()
    if f.get('section'):
        m=re.search(r'(' + re.escape(f['section']) + r'.*?)(?=\n## |\Z)', raw, re.S)
        raw=m.group(1)
    en=blocks(raw); zh=blocks(f['zh'])
    assert len(en)==len(zh), (f['id'], len(en), len(zh))
    words=len(raw.split())
    rows=''.join(f'<div class="row"><div class="cell en" lang="en">{html.escape(a)}</div><div class="cell zh">{html.escape(b)}</div></div>' for a,b in zip(en,zh))
    sections.append(f'''<section class="file" id="{f['id']}">
  <header class="file-head">
    <div class="tags"><span class="topic">{html.escape(f['topic'])}</span><span class="kind">{html.escape(f['kind'])}</span><span class="count">{words} 個英文字</span></div>
    <h2 lang="en">{html.escape(f['title'])}</h2>
    <p class="path">{html.escape(f['path'])}</p>
  </header>
  <div class="cols"><span>原文</span><span>中文對照</span></div>
  {rows}
</section>''')
    toc.append(f'''<li><a href="#{f['id']}"><span class="t-topic">{html.escape(f['topic'])}</span><span class="t-title" lang="en">{html.escape(f['title'])}</span><span class="t-count">{words}</span></a></li>''')

page=open(sys.argv[3], encoding='utf-8').read().replace('<!--TOC-->',''.join(toc)).replace('<!--SECTIONS-->','\n'.join(sections))
open(OUT,'w',encoding='utf-8').write(page)
print('OK', len(FILES), '個檔', len(page), 'bytes')
