# -*- coding: utf-8 -*-
"""
story.py  -  스토리 연출 & 텍스트  (담당: 현민우)
------------------------------------------------------------
게임의 '이야기' 부분 — 오프닝, 지역 도착 묘사, 엔딩 크레딧.
"""

import time
import world


# ============================================================
# 텍스트 연출 보조 함수
# ============================================================
def slow_print(text, delay=0.025):
    """한 글자씩 천천히 출력해서 분위기를 살린다."""
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print()


def line(char="=", length=50):
    print(char * length)


def pause(msg="(Enter 키를 눌러 계속...)"):
    input(msg)


# ============================================================
# 1. 오프닝 인트로
# ============================================================
def show_opening():
    """게임 시작 시 출력되는 오프닝."""
    line("=")
    print(world.WORLD_TITLE.center(46))
    line("=")
    print()
    slow_print(world.WORLD_LORE, delay=0.02)
    print()
    line("-")
    pause()


# ============================================================
# 2. 지역 도착 묘사
# ============================================================
def show_arrival(loc_key, first_visit):
    """
    지역에 도착했을 때 분위기 묘사를 출력한다.
    first_visit=True 이면 첫 방문 전용 스토리 이벤트도 함께 보여준다.
    """
    location = world.get_location(loc_key)
    if not location:
        return
    line("-")
    print(f"[ {location['name']} ]")
    line("-")
    slow_print(location["description"], delay=0.02)
    if first_visit and "first_visit_story" in location:
        print()
        slow_print(location["first_visit_story"], delay=0.02)
    print()


# ============================================================
# 3. 엔딩 + 제작진 크레딧
# ============================================================
def show_ending(player_name="모험가"):
    """최종 던전 클리어 후 출력되는 엔딩."""
    print()
    line("*")
    print("게임 클리어!".center(46))
    line("*")
    print()
    ending_text = (
        f"마침내 골렘 군주가 쓰러졌습니다.\n"
        f"세 종족의 침공이 모두 막혀, 에르하임 왕국에\n"
        f"다시 따스한 평화가 찾아옵니다.\n\n"
        f"용감한 모험가 '{player_name}'의 이름은\n"
        f"왕국을 구한 영웅으로 영원히 기억될 것입니다.\n"
    )
    slow_print(ending_text, delay=0.03)
    pause()

    # ── 제작진 크레딧 ──
    print()
    line("=")
    print("PYTHON 텍스트 RPG".center(46))
    print("에르하임 — 침공의 시대".center(44))
    line("=")
    credits = [
        ("기획 / 스토리 / 이동 시스템", "현민우 (조장)"),
        ("전투 시스템 / 직업 / 몬스터", "공기민"),
        ("기본 시스템 / UI",            "유채운"),
    ]
    print()
    for role, name in credits:
        print(f"   {role:<25} ...  {name}")
        time.sleep(0.4)
    print()
    line("-")
    print("플레이해 주셔서 감사합니다!".center(44))
    line("=")
