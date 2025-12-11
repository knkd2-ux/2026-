import socket
import threading
import time
from collections import deque

# --- 設定 ---
HOST = '0.0.0.0'
PORT = 5555
SPECTATOR_DELAY = 1.5  # 觀戰延遲秒數 (建議 1.5 ~ 2.0 秒)

# --- 全域變數 ---
# 緩衝區，結構為: (接收時間戳, 原始資料)
packet_buffer = deque()
# 存放觀眾的連線 socket
spectators = []
# 存放玩家的連線 (假設只有一個玩家)
player_socket = None

def spectator_broadcast_loop():
    """
    這是一個獨立執行緒，專門負責將緩衝區內「已經夠舊」的資料傳給觀眾
    """
    while True:
        if not packet_buffer:
            time.sleep(0.01) # 如果沒資料，稍微休息避免 CPU 飆高
            continue

        # 查看緩衝區最舊的一筆資料 (不要取出，先看)
        arrival_time, data = packet_buffer[0]
        
        # 計算這筆資料已經存了多久
        time_in_buffer = time.time() - arrival_time

        if time_in_buffer >= SPECTATOR_DELAY:
            # 時間到了！從緩衝區取出並發送
            packet_buffer.popleft()
            
            # 發送給所有觀眾 (加上錯誤處理以防觀眾斷線)
            for spec in spectators[:]:
                try:
                    spec.sendall(data)
                except Exception as e:
                    print(f"觀眾斷線: {e}")
                    spectators.remove(spec)
                    spec.close()
        else:
            # 資料還不夠舊，計算還需要睡多久，避免無效迴圈
            # 例如：還差 0.5 秒，那就睡 0.1 秒後再檢查
            sleep_time = SPECTATOR_DELAY - time_in_buffer
            if sleep_time > 0.1:
                time.sleep(0.1)
            else:
                time.sleep(sleep_time)

def handle_client(conn, addr):
    global player_socket
    print(f"新連線: {addr}")
    
    # 簡單的握手協議 (真實情況請依你的需求修改)
    # 假設 Client 連線後會先傳送 "PLAYER" 或 "SPECTATOR" 來表明身分
    identity = conn.recv(1024).decode('utf-8').strip()
    
    if identity == "SPECTATOR":
        spectators.append(conn)
        print(f"觀眾加入: {addr}")
        # 觀眾只收不發，所以這裡就可以讓它 pending 或做心跳檢測
        try:
            while True:
                if not conn.recv(1024): break
        except:
            pass
        finally:
            if conn in spectators: spectators.remove(conn)
            conn.close()

    elif identity == "PLAYER":
        player_socket = conn
        print(f"玩家加入: {addr}")
        try:
            while True:
                data = conn.recv(4096)
                if not data: break
                
                # --- 關鍵修改 ---
                # 收到玩家資料，不直接轉傳，而是存入緩衝區
                current_time = time.time()
                packet_buffer.append((current_time, data))
                
        except Exception as e:
            print(f"玩家連線錯誤: {e}")
        finally:
            conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"Server 啟動於 {HOST}:{PORT}，觀戰延遲設定為 {SPECTATOR_DELAY} 秒")

    # 啟動負責延遲廣播的執行緒
    broadcast_thread = threading.Thread(target=spectator_broadcast_loop, daemon=True)
    broadcast_thread.start()

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
