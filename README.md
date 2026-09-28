# Adventure Mode — 手機觸控版

在手機瀏覽器直接玩的 3D 動作冒險遊戲。把手機轉成橫的玩。

- 原作：[Adventure Mode](https://github.com/EasterEggProductions/adventure-mode-godot) by Easter Egg Productions
- 授權：程式 MIT、美術 CC-BY 4.0（見原作 LICENSE.txt）
- 本倉庫只放改動：觸控搖桿與按鈕、手機可跑的畫面模式、手機網頁外殼。每次推到 `main`，GitHub Actions 會自動下載原作、套用改動、輸出網頁版並上線。

## 操作
- 左半邊拖動：走路
- 右半邊滑動：轉鏡頭
- ATK 攻擊・JUMP 跳・ROLL 翻滾（按住跑步）・GUARD 防禦・USE 互動・LOCK 鎖定・MENU 選單

## 檔案
- `mobile/touch_controls.gd`：觸控操作
- `mobile/patch.py`：改原作的設定（畫面模式、鏡頭觸控）
- `mobile/export_presets.cfg`：網頁輸出設定
- `web/index.html`：手機網頁外殼（下載進度、開始按鈕）
- `.github/workflows/build.yml`：自動建置與上線
