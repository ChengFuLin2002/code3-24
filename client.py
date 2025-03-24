import socket
import sys

class GameClient:
    def __init__(self, host='10.22.215.154', port=63569):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
    def connect(self):
        try:
            self.client_socket.connect((self.host, self.port))
            return True
        except Exception as e:
            print(f"連線失敗: {e}")
            return False
            
    def start_game(self):
        try:
            while True:
                # 接收伺服器訊息
                data = self.client_socket.recv(1024).decode('utf-8')
                if not data:
                    break

                print(data)

                # 選擇職業或行動
                if "請選擇" in data or "選擇行動" in data:
                    user_input = input(">>> ")
                    self.client_socket.send(user_input.encode('utf-8'))
                
        except Exception as e:
            print(f"遊戲中斷: {e}")
        finally:
            self.client_socket.close()

if __name__ == "__main__":
    client = GameClient()
    
    print("歡迎來到回合制戰鬥！")
    if client.connect():
        print("連線成功！")
        client.start_game()
    else:
        print("無法連線到伺服器，請確認伺服器是否已啟動。")
