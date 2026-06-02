import random
import level
import reset

# =========================================
# 데이터 테이블
# =========================================

JOB_DATA = {
    "전사": {
        "hp": 120,
        "attack": 30,
        "crit": 20,
        "evasion": 20,
        "lv": 1,
        "exp": 0
    },

    "궁수": {
        "hp": 60,
        "attack": 60,
        "crit": 25,
        "evasion": 25,
        "lv": 1,
        "exp": 0
    },

    "도적": {
        "hp": 90,
        "attack": 45,
        "crit": 50,
        "evasion": 50,
        "lv": 1,
        "exp": 0
    }
}

MONSTER_DATA = {
    "일반": {
        "hp": 50,
        "attack": 15,
        "lv": 1,
        "exp": 25
    },

    "정예": {
        "hp": 100,
        "attack": 30,
        "lv": 2,
        "exp": 50
    },

    "보스": {
        "hp": 300,
        "attack": 45,
        "lv": 3,
        "exp": 100
    }
}

MAP_DATA = {
    "1": {
        "name": "고블린 숲",
        "reward": 300,

        "waves": [
            [
                ("고블린", "일반"),
                ("고블린", "일반"),
                ("고블린", "일반")
            ],

            [
                ("정예 고블린", "정예"),
                ("정예 고블린", "정예")
            ],

            [
                ("킹 고블린", "보스")
            ]
        ]
    },

    "2": {
        "name": "슬라임 부족",
        "reward": 400,

        "waves": [
            [
                ("슬라임", "일반"),
                ("슬라임", "일반"),
                ("슬라임", "일반")
            ],

            [
                ("강화 슬라임", "정예"),
                ("강화 슬라임", "정예")
            ],

            [
                ("킹 슬라임", "보스")
            ]
        ]
    },

    "3": {
        "name": "골렘 마을",
        "reward": 500,

        "waves": [
            [
                ("돌 골렘", "정예"),
                ("돌 골렘", "정예")
            ],

            [
                ("강철 골렘", "정예"),
                ("강철 골렘", "정예")
            ],

            [
                ("골렘 군주", "보스")
            ]
        ]
    }
}


# =========================================
# 캐릭터 클래스
# =========================================

class Character:

    def __init__(self, name, hp, attack, lv, exp, crit, evasion):

        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.lv = lv
        self.exp = exp
        self.attack = attack
        self.crit = crit
        self.evasion = evasion

    def is_alive(self):

        return self.hp > 0


# =========================================
# 플레이어 클래스
# =========================================

class Player(Character):

    def __init__(self, job):

        data = JOB_DATA[job]

        super().__init__(
            job,
            data["hp"],
            data["attack"],
            data["lv"],
            data["exp"],
            data["crit"],
            data["evasion"]
        )

        self.job = job

        self.gold = 100

        # 직업별 스택 분리
        self.defense_stack = 0
        self.focus_stack = 0
        self.shadow_stack = 0

        self.inventory = {
            "하급 회복 포션": 3,
            "중급 회복 포션": 2,
            "상급 회복 포션": 1
        }

    # 상태 출력
    def show_status(self):

        print("\n==============================")
        print(f"직업 : {self.job}")
        print(f"HP : {self.hp}/{self.max_hp}")
        print(f"LV.{self.lv}")
        print(f"EXP : {self.exp}/{level.need_exp(self.lv)}")
        print(f"공격력 : {self.attack}")
        print(f"치명타 : {self.crit}%")
        print(f"회피율 : {self.evasion}%")
        print(f"골드 : {self.gold}")

        if self.job == "전사":
            print(f"방어 스택 : {self.defense_stack}")

        elif self.job == "궁수":
            print(f"집중 스택 : {self.focus_stack}")

        elif self.job == "도적":
            print(f"그림자 스택 : {self.shadow_stack}")

        print("==============================")

    # 데미지 계산
    def calculate_damage(self):

        damage = self.attack

        # 궁수 집중 스택
        if self.job == "궁수":
            damage += self.focus_stack * 5

        critical = False

        # 크리티컬 판정
        if random.randint(1, 100) <= self.crit:

            critical = True

            if self.job == "도적":

                multiplier = 1.5 + (self.shadow_stack * 0.2)
                damage = int(damage * multiplier)

            else:
                damage = int(damage * 1.5)

        return damage, critical

    # 공격
    def attack_target(self, target):

        miss_rate = {
            "전사": 15,
            "궁수": 10,
            "도적": 5
        }

        if random.randint(1, 100) <= miss_rate[self.job]:

            print(f"\n{self.name}의 공격이 빗나갔습니다!")

            if self.job == "궁수":
                self.focus_stack = 0

            return

        damage, critical = self.calculate_damage()

        target.hp -= damage

        print(f"\n{self.name}이(가) {target.name}에게 {damage} 데미지!")

        if critical:
            print(">>> 크리티컬 히트! <<<")

        # 궁수 스택 증가
        if self.job == "궁수":

            if self.focus_stack < 5:
                self.focus_stack += 1

            print(f"집중 스택 : {self.focus_stack}")

        print(f"{target.name} 남은 HP : {max(target.hp, 0)}")


# =========================================
# 몬스터 클래스
# =========================================

class Monster(Character):

    def __init__(self, name, grade):

        data = MONSTER_DATA[grade]

        super().__init__(
            name,
            data["hp"],
            data["attack"],
            data['lv'],
            data['exp'],
            10,
            0
        )

        self.grade = grade

        self.turn_count = 0
        self.used_potion = False
        self.enrage = False

    # 광폭화
    def handle_enrage(self):

        if self.hp <= self.max_hp // 2 and not self.enrage:

            self.enrage = True
            self.attack += 20

            print("\n보스가 광폭화했습니다!")
            print("공격력이 증가합니다!")

    # 소환
    def handle_summon(self, monster_list):

        if self.turn_count % 3 == 0:

            summon = Monster("고블린", "일반")
            monster_list.append(summon)

            print("부하 몬스터를 소환했습니다!")

    # 포션
    def handle_potion(self):

        if self.hp <= 120 and not self.used_potion:

            heal = 80

            self.hp += heal

            if self.hp > self.max_hp:
                self.hp = self.max_hp

            self.used_potion = True

            print("보스가 상급 포션을 사용했습니다!")
            print(f"HP +{heal}")

            return True

        return False

    # 몬스터 행동
    def monster_ai(self, player, monster_list):

        self.turn_count += 1

        print(f"\n[{self.name}의 턴]")

        # 플레이어 회피
        if random.randint(1, 100) <= player.evasion:

            print(f"{player.name}이(가) 공격을 회피했습니다!")

            # 도적 회피 스택
            if player.job == "도적":

                if player.shadow_stack < 5:
                    player.shadow_stack += 1

                print(f"그림자 스택 증가! ({player.shadow_stack}/5)")

            return

        damage = self.attack

        # 보스 로직
        if self.grade == "보스":

            self.handle_enrage()

            self.handle_summon(monster_list)

            if self.handle_potion():
                return

            # 강공격
            if random.randint(1, 100) <= 35:

                damage *= 2
                print("보스의 강공격!")

        # 정예 연속 공격
        elif self.grade == "정예":

            if random.randint(1, 100) <= 30:

                print("정예 몬스터의 연속 공격!")

                for i in range(2):

                    player.hp -= self.attack

                    print(f"{self.attack} 데미지!")

                return

        # 전사 피해 감소
        if player.job == "전사":

            if player.defense_stack < 5:
                player.defense_stack += 1

            reduction = player.defense_stack * 2

            damage -= reduction

            if damage < 0:
                damage = 0

            print(f"전사 방어 스택 발동! 피해 감소 {reduction}")

        player.hp -= damage

        print(f"{self.name}이(가) {player.name}에게 {damage} 데미지!")
        print(f"{player.name} 남은 HP : {max(player.hp, 0)}")


# =========================================
# 포션
# =========================================

def use_potion(player):

    potion_list = [
        ("하급 회복 포션", 25),
        ("중급 회복 포션", 50),
        ("상급 회복 포션", 100)
    ]

    print("\n===== 포션 선택 =====")

    for idx, (name, heal) in enumerate(potion_list):

        print(f"{idx+1}. {name} (+{heal}) x{player.inventory[name]}")

    print("0. 취소")

    choice = input("선택 : ")

    if choice == "0":
        return False

    try:

        choice = int(choice) - 1

        potion_name, heal_amount = potion_list[choice]

    except:

        print("잘못 입력했습니다.")
        return False

    if player.inventory[potion_name] <= 0:

        print("포션이 부족합니다.")
        return False

    player.inventory[potion_name] -= 1

    player.hp += heal_amount

    if player.hp > player.max_hp:
        player.hp = player.max_hp

    print(f"\n{potion_name} 사용!")
    print(f"HP +{heal_amount}")
    print(f"현재 HP : {player.hp}/{player.max_hp}")

    return True


# =========================================
# 출력 함수
# =========================================

def show_monsters(monsters):

    print("\n===================================")
    print("현재 몬스터")
    print("===================================")

    for idx, monster in enumerate(monsters):

        print(
            f"{idx+1}. "
            f"[{monster.grade}] "
            f"{monster.name} "
            f"({monster.hp} HP)"
        )


# =========================================
# 플레이어 턴
# =========================================

def player_turn(player, monsters):

    used_potion = False

    while True:

        i = 0

        print("\n1. 공격")
        print("2. 포션 사용")
        print("3. 도망")

        choice = input("선택 : ")

        # 공격
        if choice == "1":

            try:

                target_num = int(
                    input("공격할 몬스터 번호 : ")
                ) - 1

                if target_num < 0 or target_num >= len(monsters):

                    print("잘못된 번호입니다.")
                    continue

                target = monsters[target_num]

            except:

                print("잘못 입력했습니다.")
                continue

            player.attack_target(target)

            if target.hp <= 0:

                print(f"\n{target.name} 처치!")
                level.gain_exp(player, target.exp)
                monsters.remove(target)

            return "continue"

        # 포션
        elif choice == "2":

            if used_potion:

                print("이번 턴에는 이미 포션을 사용했습니다.")
                continue

            success = use_potion(player)

            if success:
                used_potion = True

        # 도망
        elif choice == "3":

            if random.randint(1, 100) <= 40:

                print("\n도망 성공!")
                return "escape"

            else:

                print("\n도망 실패!")
                return "continue"

        else:
            print("잘못 입력했습니다.")


# =========================================
# 몬스터 턴
# =========================================

def monster_turn(player, monsters):

    for monster in monsters[:]:

        if monster.is_alive():

            monster.monster_ai(player, monsters)

            if not player.is_alive():
                return "dead"

    return "continue"


# =========================================
# 전투
# =========================================

def battle_wave(player, monsters):

    while player.is_alive() and len(monsters) > 0:

        show_monsters(monsters)

        player.show_status()

        result = player_turn(player, monsters)

        if result == "escape":
            return "escape"

        if len(monsters) == 0:
            break

        result = monster_turn(player, monsters)

        if result == "dead":
            return "dead"
        
        input("\n Enter 키를 눌러 진행")
        reset.clear_screen()
    return "victory"


# =========================================
# 맵 입장
# =========================================

def enter_map(player, map_data):

    print("\n==============================")
    print(f"{map_data['name']} 입장")
    print("==============================")

    for i, wave_data in enumerate(map_data["waves"]):

        print(f"\n===== {i+1} 웨이브 시작 =====")

        monsters = [
            Monster(name, grade)
            for name, grade in wave_data
        ]

        result = battle_wave(player, monsters)

        if result == "dead":

            print("\n당신은 쓰러졌습니다...")
            print("GAME OVER")

            return "gameover"

        elif result == "escape":

            print("\n마을로 복귀합니다.")
            return "escape"

        print(f"\n{i+1} 웨이브 클리어!")

    print(f"\n{map_data['name']} 클리어!")
    print(f"골드 +{map_data['reward']}")

    player.gold += map_data["reward"]

    return "clear"


# =========================================
# 직업 선택
# =========================================

def select_job():

    print("===================================")
    print("텍스트 RPG")
    print("===================================")

    print("\n직업 선택")
    print("1. 전사")
    print("2. 궁수")
    print("3. 도적")

    job_choice = input("선택 : ")

    job_map = {
        "1": "전사",
        "2": "궁수",
        "3": "도적"
    }

    if job_choice not in job_map:

        print("잘못 입력했습니다.")
        return None

    return Player(job_map[job_choice])


# =========================================
# 메인 게임
# =========================================

def main():

    player = select_job()

    if player is None:
        return

    while True:

        print("\n===================================")
        print("맵 선택")
        print("===================================")

        for key, data in MAP_DATA.items():

            print(f"{key}. {data['name']}")

        print("4. 종료")

        map_choice = input("선택 : ")

        if map_choice == "4":

            print("\n게임 종료")
            break

        if map_choice not in MAP_DATA:

            print("잘못 입력했습니다.")
            continue

        result = enter_map(player, MAP_DATA[map_choice])

        if result == "gameover":
            break


# =========================================
# 실행
# =========================================

if __name__ == "__main__":
    main()
