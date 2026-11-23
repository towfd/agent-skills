TOPIC: 對抗式審查

---
name: interrogate
description: 「用於『interrogate』、『adversarial review』、『multi-model review』、『challenge this』、『stress test this code』、『find blind spots』或『tear this apart』。由對手試著弄壞一個改動或設計，只有實際跑過證明的發現才留下來。」
disable-model-invocation: true（只有使用者打指令才啟動）
---

# 審問

由對手試著弄壞一個改動或一個設計。一個發現只有在實際跑過證明之後才留下來。回報這些發現。不要動手修。

## 界定框架

範圍是使用者指定的東西。沒指定的話，就是這個分支從它跟基準分支的 merge base 起算、一直到工作樹的 diff。用 **in-your-own-words** skill，根據使用者的訊息、commit 和 PR 說明，講出意圖。意圖不清楚時就問使用者。

## 分頭派出

跑 **arena** skill 階段 A 的第 3、4 步和階段 B，但有四個改變。讀 `interrogate reviewers` 那一行，取代 `arena runners`。把範圍內還沒 commit 的改動複製到每個 worktree。每個對手都用 `generalPurpose` 派出。不用 arena 的任務和理由，改給每個對手範圍、意圖和下面這份任務說明：

> 弄壞這個改動。每個發現都要拿真正的程式實際跑一次來證明，例如一個失敗的測試、一個重現腳本，或顯示錯誤行為的指令輸出。如果是設計或計畫，就跑一個原型，或去探測目前的程式樹。重現用的東西留在你自己的 worktree 裡。每個發現都要回報：標題、確切的指令、它印出的輸出，以及意圖要求的輸出。沒有實際跑過的東西都不要寫。這包括風格、命名、結構，以及要等將來某個改動才會出問題的風險。沒有發現也是合法的結果。

## 驗證

照 arena 的階段 F，重跑每個發現的指令來驗證它。輸出顯示出那個失敗、而且那個失敗違背了意圖，就留下這個發現。其餘的丟掉。根本原因相同的發現合併起來。

跳過 arena 的階段 C、D 和 E。不同的對手會找到不同的失敗，所以判定要保留每一個驗證過的發現，而不是只用某一個對手的清單。

## 產出

- **Intent**（意圖）：重新講過的那段話。
- **Findings**（發現）：每個驗證過的發現，寫出指令、它的輸出、它怎麼違背意圖，以及找到它的是哪些對手。一個都沒留下時，就寫「no verified findings」（沒有驗證過的發現）。
- **Dropped**（丟掉的）：每個對手被丟掉的發現有幾個、為什麼。
