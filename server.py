import socket
import threading
from characters import create_character

class GameServer:
    def __init__(self, host='10.22.215.154', port=63569):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 避免埠被佔用
        self.server_socket.bind((self.host, self.port))
        self.clients = []  # 存放玩家的 socket
        self.players = {}  # 存放玩家角色資料

    def start(self):
        self.server_socket.listen(1)
        print("伺服器已啟動，等待玩家連線...")

        # **讓 Server（玩家1）選擇角色**
        print("你是玩家1，請選擇職業: \n1) 戰士\n2) 法師")
        p1_choice = input("請輸入你的選擇 (1 或 2): ").strip()
        p1_class = "戰士" if p1_choice == "1" else "法師"
        self.players["玩家1"] = create_character(p1_class, "玩家1")
        print(f"你選擇了 {p1_class}！")

        # **等待玩家2 連線**
        client_socket, client_address = self.server_socket.accept()
        self.clients.append(client_socket)
        print(f"玩家2（Client）連線成功: {client_address}")
        self.send_message(client_socket, "你是玩家2，請選擇職業: \n1) 戰士\n2) 法師")

        # **讓玩家2（Client）選擇職業**
        p2_choice = self.receive_message(client_socket)
        p2_class = "戰士" if p2_choice == "1" else "法師"
        self.players["玩家2"] = create_character(p2_class, "玩家2")

        # **通知雙方遊戲開始**
        self.send_message(client_socket, f"遊戲開始！你的對手是 {self.players['玩家1'].name}")
        print(f"遊戲開始！你的對手是 {self.players['玩家2'].name}")

        # **開始戰鬥**
        self.battle()

    def battle(self):
        player_turn = 0  # 0: 玩家1, 1: 玩家2
        player_names = ["玩家1", "玩家2"]

        while all(player.health > 0 for player in self.players.values()):
            attacker = self.players[player_names[player_turn]]
            defender = self.players[player_names[1 - player_turn]]

            if player_turn == 0:
                print("你的回合！選擇行動:\n1) 普通攻擊\n2) 使用技能")
                action = input("請輸入你的選擇 (1 或 2): ").strip()
            else:
                self.send_message(self.clients[0], "你的回合！選擇行動:\n1) 普通攻擊\n2) 使用技能")
                action = self.receive_message(self.clients[0])

            if action == "1":
                damage = attacker.attack(defender)
                battle_log = f"[{attacker.name} 回合] {attacker.name} 對 {defender.name} 造成 {damage} 點傷害！"
            elif action == "2":
                damage = attacker.use_skill(defender)
                battle_log = f"[{attacker.name} 回合] {attacker.name} 使用技能，對 {defender.name} 造成 {damage} 傷害！" if damage > 0 else f"[{attacker.name} 回合] {attacker.name} MP 不足，無法使用技能！"
            else:
                continue

            print(battle_log)
            if player_turn == 1:
                self.send_message(self.clients[0], battle_log)

            if defender.health <= 0:
                if player_turn == 0:
                    print(f"恭喜！你擊敗了 {defender.name}！")
                else:
                    self.send_message(self.clients[0], f"恭喜！你擊敗了 {defender.name}！")
                    self.send_message(self.clients[0], "你被擊敗了！")
                break

            player_turn = 1 - player_turn  # 切換回合

        print("遊戲結束！")
        self.server_socket.close()

    def send_message(self, client_socket, message):
        client_socket.send(message.encode('utf-8'))

    def receive_message(self, client_socket):
        return client_socket.recv(1024).decode('utf-8').strip()

if __name__ == "__main__":
    server = GameServer()
    server.start()
