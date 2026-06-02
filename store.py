import reset

SHOP_ITEMS = {
    "1": ("하급 회복 포션", 25),
    "2": ("중급 회복 포션", 50),
    "3": ("상급 회복 포션", 100)
}

def store(player):

    while True:

        print("\n===================================")
        print("[ 상점 ]")
        print("===================================")
        print(f"보유 골드 : {player.gold}")

        for key, (name, price) in SHOP_ITEMS.items():
            print(f"{key}. {name} ({price}골드)")

        print("0. 마을로 돌아가기")

        choice = input("선택 : ")

        if choice == "0":
            reset.clear_screen()
            return

        if choice not in SHOP_ITEMS:
            print("잘못 입력했습니다.")
            continue

        item_name, price = SHOP_ITEMS[choice]

        if player.gold < price:
            print("골드가 부족합니다.")
            continue

        player.gold -= price
        player.inventory[item_name] += 1

        print(f"{item_name} 구매 완료!")
