TOPIC: 清 worktree 和模擬器

### 清理 worktree 和模擬器

1. 拍快照、做盤點。記下 `df -h /`，然後跑 `scripts/worktree-audit.sh [-b <pr-base-ref>] [repo-path]`（principle-build-the-lever）。不加 `-b` 時，它拿 `origin/HEAD` 來檢查 `MERGED`，所以 PR 的目標是別的分支時，要傳 `-b origin/<branch>`。它從 `git worktree list` 讀路徑，絕不用手打的，因為手打的 `myrepo-worktrees/x` 會漏掉放在 `.cursor/worktrees/myrepo/x` 的那一個（principle-encode-lessons-in-structure）。它依大小、放了多久、合併狀態、未提交的工作、PR 狀態，以及最近碰過它的對話，替每個 worktree 分類，然後建議該放哪一類。掃對話紀錄很慢，所以放到背景跑。
2. 分類是建議，不是許可。釘選的和進行中的對話才是真正的成品（principle-prove-it-works）。從使用者或側邊欄拿到這份清單，逐一交叉比對每個候選。這個槓桿曾經把使用者釘選的 worktree 標成 `safe`，所以以釘選清單為準。
3. 刪之前先確認有沒有在用。每一列 `verify-recent-chat`，或任何你有疑慮的，分派多個 subagent 去讀對話紀錄，回報那段對話是否被釘選或還在進行，以及它碰了哪些 worktree（principle-guard-the-context-window，對話紀錄屬於大宗資料）。一段釘選的對話會透過背景 subagent，把 arena 和重現用的程式樹開在同層的其他 worktree 裡，就算它們的名字從沒出現在側邊欄，也是在用中。依工作挑每個 subagent 的推理等級，照 Subagents 那一節。
4. 遇到不可逆的損失就暫停。`wip:N` 是 N 個有追蹤、但還沒提交的修改。先把 diff 拿出來看、取得決定，因為移除乾淨的 worktree 可以從它的分支救回來，但沒提交的工作就沒了。`scratch:N` 是沒追蹤的拋棄式檔案，可以丟，但要列出檔名。照「自主」那一節，乾淨、已合併、沒在用的就直接進行。`wip` 和在用中的要暫停。
5. 清掉確認過的那一批。每個路徑跑 `git worktree remove --force <path>`。如果資料夾因為被忽略的建置產物而留下來，就 `rm -rf` 它，再跑 `git worktree prune`。分支的 ref 會留著，所以不會丟任何 commit。用 `df -h /` 確認，並重新列一次。
6. 模擬器和其他能騰出空間的地方。模擬器通常是收穫第二大的。`xcrun simctl --set testing delete all`（XCTestDevices 的複本）、`xcrun simctl delete unavailable`，以及先 `xcrun simctl runtime list` 再 `runtime delete <id>` 刪掉舊的 runtime。需要時還有更多：Xcode 的 `DerivedData` 和 `iOS DeviceSupport`、`~/Library/Application Support/Cursor`（`state.vscdb.backup`，以及 `snapshots/roots/<root>`，其中以你當成工作區開過的資料夾命名的 `<root>` 會膨脹得很大）、套件快取（pnpm、uv、brew、yarn）。只清使用者沒說要留的快取。

這是唯一一份會刪掉使用者狀態、卻沒有程式碼審查能攔下失誤的劇本，所以上面這些關卡就是審查。

**回覆：** 前後的 `df -h /` 和騰出的空間、清掉的 worktree，以及每個保留下來的用一行說明原因（被哪段對話使用中，或有沒提交的工作）。
