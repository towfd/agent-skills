TOPIC: 換完就刪舊 API

---
name: principle-migrate-callers-then-delete-legacy-apis
description: 「引進新的內部 API、而舊的呼叫者還在時套用。在同一波裡遷移呼叫者並刪掉舊 API，不要保留相容層。」
disable-model-invocation: true（只有使用者打指令才啟動）
---

# 先遷移呼叫者再刪舊 API

- 更新測試，讓它們斷言新的約定，並刪掉只在保護重構前實作細節的測試

**什麼時候適用：**
- 沒有外部使用者依賴向後相容
- 專案承受得了協調好的破壞性修改
- 新 API 是某個簡化或重構計畫的一部分
