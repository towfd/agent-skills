---
name: rwd-check
description: 用瀏覽器在桌機、平板、手機三種寬度實際打開網頁，截圖並量有沒有超出畫面。
disable-model-invocation: true
---

# 三種寬度檢查

用瀏覽器工具實際打開頁面。只讀程式碼不算檢查。

| 寬度 | 視窗 |
|---|---|
| 桌機 | 1440 × 900 |
| 平板 | 768 × 1024 |
| 手機 | 390 × 844 |

每種寬度：

1. 調整視窗，截一張整頁的圖。
2. 在頁面裡跑下面這段，量有沒有左右捲動、哪些元素超出畫面。
3. 自己看過截圖，再交出去。

```js
() => ({
  overflowX: document.documentElement.scrollWidth > window.innerWidth,
  wide: [...document.querySelectorAll('body *')]
    .filter(e => e.getBoundingClientRect().right > window.innerWidth + 1)
    .slice(0, 10)
    .map(e => e.tagName + '.' + e.className),
})
```

過關：三種寬度的 `overflowX` 都是 `false`。沒過就修，修完三種寬度重量一次。

回報三張截圖的路徑和量到的結果。沒有瀏覽器工具就回報「沒辦法實際檢查」，不要用讀程式碼代替。
