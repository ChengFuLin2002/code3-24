#server portion
import socket
import threading
import random
import time
import datetime
from characters import create_character

class GameServer:
    def __init__(self, host='10.22.215.154', port=63569):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.clients = []
        
    def start(self):
        self.server_socket.listen(5)
        print(f"伺服器已啟動，等待玩家連線...")
        
        while True:
            client_socket, client_address = self.server_socket.accept()
            print(f"玩家連線: {client_address}")
            client_thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
            client_thread.start()
            
    def handle_client(self, client_socket, client_address):
        try:
            # 發送歡迎訊息
            self.send_message(client_socket, "歡迎來到回合制戰鬥！")
            
            # 讓玩家選擇角色
            self.send_message(client_socket, "請選擇你的角色:")
            self.send_message(client_socket, "1) 戰士")
            self.send_message(client_socket, "2) 法師")
            
            choice = self.receive_message(client_socket)
            player_character_type = "戰士" if choice == "1" else "法師"
            player_character = create_character(player_character_type, "玩家")
            
            # AI 選擇角色
            ai_character = create_character("戰士", "電腦戰士")
            
            self.send_message(client_socket, f"你選擇了 {player_character_type}，你的對手是 {ai_character.name}！")
            self.send_message(client_socket, "遊戲開始！")
            
            # 記錄開始時間
            start_time = datetime.datetime.now()
            print(f"=== 遊戲開始 ({start_time.strftime('%Y-%m-%d %H:%M:%S')}) ===")
            print(f"玩家連線自 {client_address}")
            print(f"玩家選擇: {player_character_type}, AI 對手是 {ai_character.name}")
            
            # 開始戰鬥
            self.battle(client_socket, player_character, ai_character)
            
            # 記錄結束時間
            print(f"=== 遊戲結束 ===")
            
        except Exception as e:
            print(f"處理客戶端時出錯: {e}")
        finally:
            client_socket.close()
            
    def battle(self, client_socket, player, ai):
        player_turn = True
        
        while player.health > 0 and ai.health > 0:
            if player_turn:
                # 玩家回合
                self.send_message(client_socket, "你的回合！選擇行動:")
                self.send_message(client_socket, "1) 普通攻擊")
                self.send_message(client_socket, "2) 使用技能")
                
                action = self.receive_message(client_socket)
                
                if action == "1":
                    damage = player.attack(ai)
                    battle_log = f"[玩家回合] 玩家 對 {ai.name} 造成 {damage} 點傷害！"
                    print(battle_log + f" (AI 剩餘 HP: {ai.health})")
                    self.send_message(client_socket, battle_log)
                    self.send_message(client_socket, f"對方剩餘血量: {ai.health}")
                elif action == "2":
                    damage = player.use_skill(ai)
                    if damage > 0:
                        battle_log = f"[玩家回合] 玩家 使用 [猛擊]，對 {ai.name} 造成 {damage} 傷害！(MP -10)"
                        print(battle_log + f" (AI 剩餘 HP: {ai.health})")
                        self.send_message(client_socket, battle_log)
                        self.send_message(client_socket, f"對方剩餘血量: {ai.health}")
                    else:
                        battle_log = f"[玩家回合] 玩家 MP 不足，無法使用 [猛擊]！"
                        print(battle_log + f" (AI 剩餘 HP: {ai.health})")
                        self.send_message(client_socket, battle_log)
            else:
                # AI 回合
                time.sleep(1)  # 稍微延遲，讓玩家有時間閱讀
                
                # AI 隨機選擇攻擊或使用技能
                ai_action = random.choice(["attack", "skill"])
                
                if ai_action == "attack" or ai.mana < 10:
                    damage = ai.attack(player)
                    battle_log = f"[AI 回合] {ai.name} 對 玩家 造成 {damage} 點傷害！"
                    print(battle_log + f" (玩家剩餘 HP: {player.health})")
                    self.send_message(client_socket, battle_log)
                    self.send_message(client_socket, f"你剩餘血量: {player.health}")
                else:
                    damage = ai.use_skill(player)
                    battle_log = f"[AI 回合] {ai.name} 使用 [猛擊]，對 玩家 造成 {damage} 傷害！(MP -10)"
                    print(battle_log + f" (玩家剩餘 HP: {player.health})")
                    self.send_message(client_socket, battle_log)
                    self.send_message(client_socket, f"你剩餘血量: {player.health}")
                    
            # 切換回合
            player_turn = not player_turn
            
        # 戰鬥結束
        if player.health <= 0:
            winner = f"{ai.name} 獲勝！"
            self.send_message(client_socket, f"你被擊敗了！{ai.name} 獲勝！")
        else:
            winner = "玩家勝利！"
            self.send_message(client_socket, f"恭喜你擊敗了 {ai.name}！")
            
        print(winner)
            
    def send_message(self, client_socket, message):
        client_socket.send(message.encode('utf-8'))
        
    def receive_message(self, client_socket):
        return client_socket.recv(1024).decode('utf-8').strip()
        
if __name__ == "__main__":
    server = GameServer()
    server.start()