import socket
import threading
from characters import create_character

class GameServer:
    def __init__(self, host='10.22.215.154', port=63569):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.clients = []  # 存放兩名玩家的 socket
        self.players = {}  # 存放玩家角色資料
        
    def start(self):
        self.server_socket.listen(2)
        print("伺服器已啟動，等待玩家連線...")

        # 伺服器作為玩家1
        self.clients.append(self.server_socket.accept()[0])
        print("玩家1（伺服器）已準備好")
        self.send_message(self.clients[0], "你是玩家1，請選擇職業: \n1) 戰士\n2) 法師")

        # 讓玩家1（server）選擇職業
        p1_choice = self.receive_message(self.clients[0])
        self.players[self.clients[0]] = create_character("戰士" if p1_choice == "1" else "法師", "玩家1")

        # 等待玩家2 連線
        client_socket, client_address = self.server_socket.accept()
        self.clients.append(client_socket)
        print(f"玩家2（Client）連線成功: {client_address}")
        self.send_message(client_socket, "你是玩家2，請選擇職業: \n1) 戰士\n2) 法師")

        # 讓玩家2（client）選擇職業
        p2_choice = self.receive_message(client_socket)
        self.players[client_socket] = create_character("戰士" if p2_choice == "1" else "法師", "玩家2")

        # 通知雙方遊戲開始
        self.send_message(self.clients[0], f"遊戲開始！你的對手是 {self.players[self.clients[1]].name}")
        self.send_message(self.clients[1], f"遊戲開始！你的對手是 {self.players[self.clients[0]].name}")

        # 進入戰鬥
        self.battle()

    def battle(self):
        player_turn = 0  # 0: 玩家1, 1: 玩家2

        while all(player.health > 0 for player in self.players.values()):
            attacker_socket = self.clients[player_turn]
            defender_socket = self.clients[1 - player_turn]
            attacker = self.players[attacker_socket]
            defender = self.players[defender_socket]

            self.send_message(attacker_socket, "你的回合！選擇行動:\n1) 普通攻擊\n2) 使用技能")
            self.send_message(defender_socket, "等待對手行動...")

            action = self.receive_message(attacker_socket)

            if action == "1":
                damage = attacker.attack(defender)
                battle_log = f"[{attacker.name} 回合] {attacker.name} 對 {defender.name} 造成 {damage} 點傷害！"
            elif action == "2":
                damage = attacker.use_skill(defender)
                battle_log = f"[{attacker.name} 回合] {attacker.name} 使用技能，對 {defender.name} 造成 {damage} 傷害！" if damage > 0 else f"[{attacker.name} 回合] {attacker.name} MP 不足，無法使用技能！"
            else:
                continue

            print(battle_log)
            self.send_message(attacker_socket, battle_log)
            self.send_message(defender_socket, battle_log)

            if defender.health <= 0:
                self.send_message(attacker_socket, f"恭喜！你擊敗了 {defender.name}！")
                self.send_message(defender_socket, "你被擊敗了！")
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
