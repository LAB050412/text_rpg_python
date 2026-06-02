def gain_exp(player, exp):

    print(f"경험치 +{exp}")

    player.exp += exp

    while player.exp >= need_exp(player.lv):

        player.exp -= need_exp(player.lv)

        level_up(player)


def need_exp(lv):

    return lv * 100


def level_up(player):

    player.lv += 1

    print("\n================")
    print("LEVEL UP!")
    print(f"Lv.{player.lv}")
    print("================")

    stat_growth(player)


def stat_growth(player):

    if player.job == "전사":

        player.max_hp += 30
        player.attack += 10

    elif player.job == "궁수":

        player.max_hp += 10
        player.attack += 20

    elif player.job == "도적":

        player.max_hp += 5
        player.attack += 5

    player.hp = player.max_hp

    print("능력치가 상승했습니다!")