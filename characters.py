#character portion
class Character:
    def __init__(self, name, health, mana, attack_power):
        self._name = name
        self._health = health
        self._mana = mana
        self._attack_power = attack_power
        self._status = "正常"  # 狀態系統：正常, 中毒, 暈眩

    # Getter 和 Setter 方法
    @property
    def name(self):
        return self._name

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        if value < 0:
            self._health = 0
        else:
            self._health = value

    @property
    def mana(self):
        return self._mana

    @mana.setter
    def mana(self, value):
        if value < 0:
            self._mana = 0
        else:
            self._mana = value

    @property
    def attack_power(self):
        return self._attack_power

    @attack_power.setter
    def attack_power(self, value):
        if value < 0:
            self._attack_power = 0
        else:
            self._attack_power = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    def attack(self, target):
        if self._status == "暈眩":
            print(f"{self._name} 被暈眩了，無法攻擊！")
            return
        damage = self._attack_power
        target.take_damage(damage)
        print(f"{self._name} 攻擊了 {target.name}，造成了 {damage} 點傷害！")
        return damage

    def take_damage(self, damage):
        self._health -= damage
        if self._health <= 0:
            self._health = 0
            print(f"{self._name} 已被擊敗！")
        else:
            print(f"{self._name} 剩餘 {self._health} 點生命值。")

    def use_skill(self, skill_name, target):
        if self._status == "暈眩":
            print(f"{self._name} 被暈眩了，無法使用技能！")
            return 0
        if self._mana < 10:
            print(f"{self._name} 的魔力不足，無法使用 {skill_name}！")
            return 0
        self._mana -= 10
        damage = self._attack_power * 1.5
        target.take_damage(damage)
        print(f"{self._name} 對 {target.name} 使用了 {skill_name}，造成了 {damage} 點傷害！")
        return damage

    def __str__(self):
        return f"{self._name} (生命值: {self._health}, 魔力: {self._mana}, 攻擊力: {self._attack_power}, 狀態: {self._status})"


class Warrior(Character):
    def __init__(self, name, health=150, mana=50, attack_power=20):
        super().__init__(name, health, mana, attack_power)
        self._skill_name = "猛擊"

    def use_skill(self, target):
        if self._status == "暈眩":
            print(f"{self._name} 被暈眩了，無法使用技能！")
            return 0
        if self._mana < 10:
            print(f"{self._name} MP 不足，無法使用 [{self._skill_name}]！")
            return 0
        self._mana -= 10
        damage = int(self._attack_power * 1.5)
        target.take_damage(damage)
        print(f"{self._name} 使用 [{self._skill_name}]，對 {target.name} 造成 {damage} 傷害！(MP -10)")
        return damage

    def __str__(self):
        return f"戰士 {self._name} (HP: {self._health}, MP: {self._mana}, 攻擊力: {self._attack_power}, 狀態: {self._status})"


class Mage(Character):
    def __init__(self, name, health=120, mana=100, attack_power=15):
        super().__init__(name, health, mana, attack_power)
        self._skill_name = "猛擊"

    def use_skill(self, target):
        if self._status == "暈眩":
            print(f"{self._name} 被暈眩了，無法使用技能！")
            return 0
        if self._mana < 10:
            print(f"{self._name} MP 不足，無法使用 [{self._skill_name}]！")
            return 0
        self._mana -= 10
        damage = 30  # 固定傷害
        target.take_damage(damage)
        print(f"{self._name} 使用 [{self._skill_name}]，對 {target.name} 造成 {damage} 傷害！(MP -10)")
        return damage

    def __str__(self):
        return f"法師 {self._name} (HP: {self._health}, MP: {self._mana}, 攻擊力: {self._attack_power}, 狀態: {self._status})"


# 建立角色函數
def create_character(character_type, name):
    if character_type == "戰士":
        return Warrior(name)
    elif character_type == "法師":
        return Mage(name)
    else:
        return Character(name, 100, 50, 10)  # 默認角色