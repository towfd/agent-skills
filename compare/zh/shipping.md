TOPIC: 讓一疊 PR 落地

### 出貨

**落地的東西是你的責任。每個 PR 各自獨立驗證，只讓從根部算起、已驗證的那一串落地，然後就別再碰這疊 PR。**

1. **先確定程式碼託管平台，再在每個 PR 落地前各自獨立驗證。** 預設用 GitHub CLI（`gh`）。如果 `command -v origin` 成功，而且 Origin 解析得到這個儲存庫，每一個 PR 操作都用 `origin pr`。否則就留在 `gh`，並把改用備援這件事記下來。絕不要求 Graphite（`gt`）。每個 PR 一個驗證者，每個都是一個 Cursor 雲端 agent，用對應的 control skill（例如 `cursor-team-kit` 的 `control-ui` 或 `control-cli`）照使用者的方式跑這次修改，拿父層對照 head，然後在那個 PR 上貼出 `PASS`、`PASS+NOTES` 或 `FAIL`。只有沒寫這段程式的 agent 給的判定才算數，因為作者檢查的是它本來想做出來的東西。CI 綠燈和機器人審查通過都不算判定，因為兩者都沒有像使用者那樣跑這次修改。
2. **只讓從最底下開始、連續已驗證的那一串落地。** 從最低的未合併 PR 往上走，停在第一個沒有 `PASS` 或 `PASS+NOTES` 的。它下面的 PR 就是這一串，其中最上面那個是天花板。在未驗證 PR 上面的已驗證 PR 要等，因為少了下面的程式，它落不了地。如果某個 PR 的分支既不含、也不需要那段程式，它可以移到主幹上自己落地。它要先拿到新的判定，因為它舊的判定是在底下有那段程式的情況下跑的，而主幹沒有那段程式。
3. **重新確認判定還符合目前的程式。** 判定涵蓋的是一份 patch，而整串 rebase 會把它上面的每個 PR 移到新的 SHA，卻不會讓任何檢查失敗。相信一個比較舊的判定之前，先拿判定當時那個 SHA 的 `git patch-id` 和目前的 head 比對。如果兩份 patch 只差在測試、文件或 lint 設定，那麼一條驗證線跑的東西，在兩個 SHA 上建置出來除了雜訊之外都一樣時，它的結果就仍然成立。雜訊指的是：同一個判定 SHA 建置兩次也會出現的差異，或內嵌的 commit SHA。每一種雜訊都附上它的檔案回報，讓讀的人能檢查這個判斷。那些修改本身仍然要重新檢查、重新審查，因為舊的判定從來沒看過它們。沒有建置產出的驗證線，例如 dev server，沒辦法證明這一點，所以要重跑；其他有偏移的東西也都要重新驗證。
4. **由下往上落地，一次一個 PR。** 一律合併這一串裡最低的未合併 PR，用 `origin pr merge <pr>` 或 `gh pr merge <pr> --squash`。在 Origin 上，單純下這個指令也會把你指定的 PR 下面的每個 PR 一起合併；在 GitHub 上，base 還是父分支的 PR 會合併進那個分支，而不是主幹。把 PR 讀回來看結果（`origin pr view <pr>` 或 `gh pr view <pr> --json state,mergedAt,baseRefName`），因為合併佇列只是把 PR 排進佇列時，合併指令也可能回報成功，而要求了自動合併也不等於已經合併。已落地的 PR 讀起來會是 merged，base 是主幹，不是父分支。只在判定涵蓋目前 head 的 PR 上開啟 `--auto`（Origin 的 merge-when-ready 或 GitHub 的 auto-merge），因為它會把任何準備好的 head 落地。一次合併落地後，把 base 原本是那個被合併分支的 PR 改指向主幹（`origin pr edit <pr> --base <trunk>` 或 `gh pr edit <pr> --base <trunk>`），把它的 patch 移到合併的結果上，再用 `--force-with-lease` 推送。判定涵蓋的是 patch，不是它的 commit，所以判定還算不算數，由第 3 步的 patch-id 規則決定。等它的檢查通過、判定也還算數，就合併它。
5. **落地的過程中別碰這疊 PR。** 第 4 步搬動下一個 PR，是對分支或 base 唯一的改動，因為一次合併會把它的分支和 base 在那一刻裝著的東西落地，不管有沒有判定。在 GitHub 上，在 `/loop` 底下用 `scripts/watch-pr/watch-pr --queued-stack` 盯著這一串，直到它在天花板回報 `COMPLETE`。在 `--stack-prs` 裡由下往上傳入這一串的 PR 編號，每次重新啟動監看程式都傳同一份清單。在 Origin 上，每次 `origin pr checks <pr> --watch` 返回時，就用 `origin pr view <pr> --checks` 重新讀一次目前的 PR，直到天花板顯示 merged。父 PR 合併時 base 移到主幹，是預期中的事，不是要修的損壞。如果某次合併卡住了，先查出原因，再改任何東西。
6. **停在天花板。** 要延長這一串得有新的判定，所以那是從第 1 步重新走一輪。

**回覆：** 已驗證的那一串和它的天花板、每個 PR 的判定以及是誰給的、哪些落地了以及你怎麼確認、下一個缺口需要什麼。
