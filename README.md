# 2026 新式國民健康操｜AI Motion Party Game
## Concept Development
「2026 新式國民健康操（AI Motion Party Game）」是一款結合 AI 體感偵測 + 多人派對互動 + 網頁遊戲 的創新專案。
目標是讓玩家 拒絕久坐、舒緩壓力、促進手眼協調、活絡氣氛，並透過搞笑逗趣的動作創造派對感與娛樂性。

遊戲強調：

- 免安裝 App，瀏覽器直接遊玩

- AI 偵測臉、手、身體動作

- 多人同步競賽、觀戰模式

- 三款體感遊戲整合於同一畫面

## Implementation Resources（使用資源）

- AWS EC2（Osaka）雲端伺服器

- MediaPipe Holistic（AI 偵測模型）

- HTML / CSS / JavaScript 前端資源

- Canvas API 繪圖

- WebSocket 通訊工具

- Linux（Rocky Linux）執行環境

## Existing Library / Software
- MediaPipe：骨架與嘴部 AI 偵測

- aiohttp：Python WebSocket Server

- uvloop：高效非同步 Loop

- Nginx：反向代理、SSL

- Gunicorn：後端 process manager

## Implementation Process（執行過程）

1.使用 HTTPS 讓瀏覽器允許開啟鏡頭

2.部署 Nginx → 處理 SSL

3.Nginx 反向代理到 Python 後端

4.Python aiohttp 接收 WebSocket 訊號

5.前端 MediaPipe → 取得關鍵點

6.將玩家動作轉換成遊戲指令

7.後端同步兩位玩家與觀眾畫面

8.Canvas 繪製遊戲畫面與分數

## Knowledge from Lecture

- 以 Nginx Reverse Proxy 改善效能（課堂網路架構應用）

- SSL / HTTPS → 資安課程中的憑證與加密應用

## Installation
### 伺服器端

1.安裝 Python 3.9+

2.安裝 aiohttp、uvloop、Gunicorn

3.安裝 Nginx

4.設定 SSL 憑證（Let's Encrypt 或自簽）

5.設定 proxy_pass

6.開啟 80 / 443 Port

### 本機測試

1.Clone 專案

2.`pip install -r requirements.txt`

3.透過 `python server.py` 啟動後端

4.使用 `index.html`開啟遊戲大廳
## Job Assignment

| **姓名**   | **工作內容** |
|------------|----------|
| 呂恆毅       | 好寶寶訓練班遊戲設計|
| 李宗霖     | 大岩壁遊戲設計 |
| 李昱杰       | 東尼速成班遊戲設計/網站架設/專案統整|
| 馮可堂 | 網站架設|
## 遇到的挑戰

1.	瀏覽器無法開啟鏡頭
   
- 問題：Chrome/Safari 基於安全性，禁止在 HTTP 協定下使用 navigator.mediaDevices.getUserMedia。

- 解決：架設 Nginx 並配置 SSL 憑證，將網站升級為 HTTPS，成功啟用鏡頭權限。

2.	WebSocket 連線不穩
   
- 問題：直接使用 Python 處理 SSL 效能較差。

- 解決：採用 Nginx 處理 SSL 握手 (SSL Termination)，Python 專注於遊戲邏輯運算，大幅提升連線穩定度。
## 未來展望

•	更多運動類型：加入伏地挺身 (Push-up) 與開合跳 (Jumping Jack) 偵測。

•	手機端適配：優化 Canvas 比例與 MediaPipe 參數，支援手機瀏覽器遊玩。

•	成就系統：紀錄玩家歷史最高分與燃燒卡路里估算。
## 感謝名單
- Blue T
- ChatGPT
- Gemini


