# 2026 新式國民健康操｜AI Motion Party Game
## 動機
因為最近接近期末大家壓力都太大系上的同學都呈現 「壓力爆棚、久坐到屁股痛、報告越寫越麻木」 的狀態。大家每天不是盯著電腦，就是同時趕三份作業，看起來離「國民健康」越來越遠。
於是我們決定：與其每天喊著「要運動」，不如做一個 讓大家動起來又能放鬆心情的遊戲。
## 1.專案簡介
「2026 新式國民健康操」是一個整合 Python aiohttp 非同步伺服器、Nginx 反向代理、WebSocket 即時通訊 與 MediaPipe AI 邊緣運算 的體感遊戲專題。
不同於傳統鍵盤滑鼠操作，本系統透過鏡頭捕捉玩家的「臉部」、「手部」與「身體軀幹」動作，將真實的運動轉化為遊戲指令。系統部署於 AWS雲端 (Osaka)，透過 Nginx 處理 SSL 加密以啟用瀏覽器鏡頭權限，支援低延遲的多人連線對戰。
玩家可以：

•	單人練習 / 多人對戰：支援開房 (Host) 與加入 (Join) 模式，透過 4 位數 PIN 碼快速配對。

•	三合一分割畫面：同一個螢幕同時遊玩三款不同機制的體感遊戲。

•	即時觀戰：觀眾可透過觀戰模式 (Spectator) 觀看賽況。

•	跨裝置遊玩：基於 Web 技術，支援 PC 與筆電瀏覽器。

## 2.系統特色
遊戲模式

•	單人模式 (Single)：自我挑戰最高分。

•	開房模式 (Host)：建立房間，等待對手加入。

•	加入模式 (Join)：輸入 PIN 碼，與房主進行 1v1 對戰。

•	觀戰模式 (Spectator)：即時觀看兩位玩家的比賽畫面與分數。

收錄遊戲 (三合一體感玩法)

1.	東尼速成班 (Bird Game)：偵測嘴巴開合與舌頭動作，控制小鳥飛行。
2.	好寶寶訓練班 (Rhythm Game)：偵測手腕位置，擊打落下的節奏點。
3.	大岩壁 (Tower/Stack Game)：偵測臀部深蹲動作，堆疊搖晃的房子。
## 3.系統架構
本系統採用 Nginx 反向代理 (Reverse Proxy) 架構，確保 HTTPS 安全連線與 WebSocket 的穩定傳輸。
程式碼片段
graph TD
    User[玩家 Browser] -->|HTTPS (Port 443)| Nginx[Nginx Reverse Proxy]
    Nginx -->|Proxy Pass (Port 8000)| Python[Python aiohttp Server]
    
    subgraph "AWS EC2 Server (Osaka)"
        Nginx
        Python
        SSL[SSL Certificates]
    end

    subgraph "前端運算"
        MediaPipe[MediaPipe AI 模型]
    end

    Python -->|Broadcast| User2[對手 Browser]
關鍵技術流程：
1.	SSL 加密 (Nginx)：瀏覽器限制 getUserMedia (開啟鏡頭) 必須在 HTTPS 環境下執行。Nginx 負責處理 SSL 憑證，並將加密流量解密後轉送給後端。
2.	WebSocket 升級：Nginx 配置 proxy_set_header Upgrade $http_upgrade，支援將 HTTP 協定升級為 WebSocket 全雙工通訊。
3.	非同步處理 (aiohttp)：後端使用 uvloop 高速處理大量併發的遊戲訊號。
## 4. 技術與工具

伺服器端 (Server-Side)

•	Nginx：高效能網頁伺服器

  -	Reverse Proxy：將 Port 80/443 流量導向後端 Port 8000。
  
  -	SSL Termination：處理 HTTPS 加密 (Let's Encrypt / Self-signed)。

•	Python 3.9 + aiohttp：非同步 WebSocket 後端核心。

•	uvloop：取代標準 asyncio 事件迴圈，效能接近 Go/Node.js。

•	Gunicorn：Process Manager，管理 Python 應用程式。

客戶端 (Client-Side)

•	HTML5 / CSS3 / JavaScript：RWD 介面設計。

•	Canvas API：高效能 2D 遊戲畫面繪製。

•	MediaPipe Holistic：Google 機器學習模型，同時偵測臉、手、身體關鍵點。

基礎設施 (Infrastructure)

•	AWS EC2：運算伺服器 (部署於 Osaka Region)。

•	Linux (Rocky Linux)：作業系統環境。
##5. 專案結構

2026-health-exercise/
├── nginx.conf          # Nginx 設定檔 (反向代理與 SSL 設定)
├── server.py           # 核心後端 (aiohttp WebSocket Server)
├── index.html          # 遊戲大廳 (模式選擇、PIN碼輸入)
├── game_split.html     # 三合一綜合遊戲主程式
├── bird_game.html      # 獨立遊戲：吐舌頭控制
├── rhythm_game.html    # 獨立遊戲：節奏擊鼓
├── tower.html          # 獨立遊戲：深蹲蓋樓
├── game.log            # 伺服器運行與錯誤日誌
└── README.md           # 專案說明文件

## 6. Nginx 關鍵配置說明

為了讓 WebSocket 與鏡頭權限正常運作，nginx.conf 做了以下關鍵設定：
Nginx
server {
    listen 443 ssl http2;
    
    # SSL 憑證路徑
    ssl_certificate "/etc/pki/nginx/server.crt";
    ssl_certificate_key "/etc/pki/nginx/private/server.key";

    location / {
        # 轉發給 Python 後端
        proxy_pass http://127.0.0.1:8000;
        
        # ★★★ WebSocket 支援關鍵 ★★★
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        
        # 傳遞真實 IP
        proxy_set_header X-Real-IP $remote_addr;
    }
}
## 7. 遇到的挑戰與解決方案

1.	瀏覽器無法開啟鏡頭
-	問題：Chrome/Safari 基於安全性，禁止在 HTTP 協定下使用 navigator.mediaDevices.getUserMedia。
-	解決：架設 Nginx 並配置 SSL 憑證，將網站升級為 HTTPS，成功啟用鏡頭權限。
2.	WebSocket 連線不穩
-	問題：直接使用 Python 處理 SSL 效能較差。
- 解決：採用 Nginx 處理 SSL 握手 (SSL Termination)，Python 專注於遊戲邏輯運算，大幅提升連線穩定度。
## 8. 未來展望

•	更多運動類型：加入伏地挺身 (Push-up) 與開合跳 (Jumping Jack) 偵測。

•	手機端適配：優化 Canvas 比例與 MediaPipe 參數，支援手機瀏覽器遊玩。

•	成就系統：紀錄玩家歷史最高分與燃燒卡路里估算。
## 9. 開發團隊

| **學號**   | **姓名** | **分工** |
|------------|----------|----------|
| 111213002 |呂恆毅   | 好寶寶訓練班遊戲設計|
| 111213032 | 李宗霖 |大岩壁遊戲設計|
| 111213037 |李昱杰|東尼速成班遊戲設計/網站架設/專案統整|
| 113321059 | 馮可棠|網站架設|





