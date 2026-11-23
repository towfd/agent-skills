TOPIC: 開 PR

### 開 PR

其他每份劇本的最後都會叫用這份。

在一個從主幹開出來的 git worktree 裡工作，不相干的工作不要放進去。rebase 成小的、可以落地的 commit。commit 之前，對 diff 跑 `cursor-team-kit` 的 `/deslop`。

標題：`type(scope): subject`，如果修改主要落在某個真實的符號上，就點名它。內文：一份一分鐘看得完、不超過 40 行的簡報，照順序用這些 `##` 標題，空的就拿掉：`## Why`、`## What changed`、`## Scope`、`## Tradeoffs`（只寫審查者不寫就會來問的、被否決的替代方案）、`## Blast Radius`、`## Verification`。

後續的修改照基底分支疊上去。PR 開成可以審查的狀態，透過這次執行的 PR 工具，用 `draft: false`。沒有那種工具時，用 `gh pr create` 而且不加 `--draft`，或者在 Origin 的 CLI 認得這個倉庫時，用 `origin pr create --status open`。開 PR 不會啟動看顧。
