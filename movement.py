# -*- coding: utf-8 -*-
"""
movement.py  -  이동 & 탐색 시스템  (담당: 현민우)
------------------------------------------------------------
플레이어가 장소 이름을 입력해서 지역을 이동하고,
던전에 진입하면 공기민의 전투 시스템(enter_map)을 호출하는 흐름.

[공기민 코드 연결 지점]
  - enter_map(player, MAP_DATA[map_key])   → "clear"/"gameover"/"escape"
  - MAP_DATA                               → 던전 데이터 테이블
  - use_potion(player)                     → 필드에서 포션 사용
"""

import world
import story
import reset
from store import store
# ── 공기민의 모듈에서 필요한 함수 / 데이터 import ──
# (공기민 파일명: 팀플_정리.py)
from Combat import enter_map, MAP_DATA, use_potion


# ============================================================
# 게임 진행 상태
# ============================================================
class GameState:
    """
    - current   : 현재 위치한 지역 key
    - unlocked  : 입장 가능한 지역 key 집합
    - visited   : 한 번이라도 방문한 지역 (첫 방문 판정용)
    - cleared   : 클리어한 던전 key 집합
    - finished  : 게임 종료 여부 (최종 던전 클리어 or 사망)
    """
    def __init__(self):
        self.current = world.START_LOCATION
        # 시작 시: 마을 + 첫 번째 던전(고블린 숲)이 열려 있음
        self.unlocked = {world.START_LOCATION, world.PROGRESSION[0]}
        self.visited = set()
        self.cleared = set()
        self.finished = False


# ============================================================
# 지역 이동
# ============================================================
def move_to(state, target_key):

    reset.clear_screen()
    """지역을 이동하고 도착 연출을 출력."""

    first_visit = target_key not in state.visited
    state.current = target_key
    state.visited.add(target_key)
    story.show_arrival(target_key, first_visit)


def unlock_next(state, cleared_key):
    """클리어한 던전 다음 단계 던전을 잠금 해제."""
    if cleared_key not in world.PROGRESSION:
        return
    idx = world.PROGRESSION.index(cleared_key)
    if idx + 1 < len(world.PROGRESSION):
        next_key = world.PROGRESSION[idx + 1]
        if next_key not in state.unlocked:
            state.unlocked.add(next_key)
            next_name = world.get_location(next_key)["name"]
            print(f"\n✨ 새로운 지역이 열렸습니다 → [{next_name}]")


# ============================================================
# 던전 진입 — 공기민의 enter_map 호출
# ============================================================
def enter_dungeon(state, player, loc_key):
    """
    던전에 입장한다.
    1) 공기민의 enter_map(player, MAP_DATA[..]) 호출
    2) 결과에 따라 다음 던전 개방 / 게임 종료 / 마을 복귀 처리
    """
    location = world.get_location(loc_key)
    map_key = location["map_key"]
    if map_key is None or map_key not in MAP_DATA:
        print("(이 장소는 던전이 아닙니다)")
        return

    # ── 공기민의 전투 모듈로 위임 ──
    result = enter_map(player, MAP_DATA[map_key])

    # ── 결과 처리 ──
    if result == "gameover":
        # 사망 → 게임 종료
        state.finished = True

    elif result == "clear":
        state.cleared.add(loc_key)
        if location.get("is_final"):
            # 최종 던전 클리어 → 엔딩
            state.finished = True
            story.show_ending(player.name)
        else:
            # 일반 던전 클리어 → 다음 던전 개방 + 마을 복귀
            unlock_next(state, loc_key)
            print("\n무사히 마을로 돌아옵니다...")
            move_to(state, world.START_LOCATION)

    elif result == "escape":
        # 도망 → 마을 복귀
        print("\n무사히 마을로 돌아옵니다...")
        move_to(state, world.START_LOCATION)


# ============================================================
# 메뉴 출력
# ============================================================
def show_menu(state):
    """현재 위치 + 이동 가능 장소 + 명령어를 보여준다."""
    location = world.get_location(state.current)
    story.line("-")
    print(f"📍 현재 위치: {location['name']}")

    if location["is_safe"]:
        # 마을에서는 입장 가능한 던전 목록을 보여준다.
        print("\n[입장 가능한 던전]")
        for key in world.PROGRESSION:
            data = world.get_location(key)
            if key in state.unlocked:
                tag = "  ✓ 클리어" if key in state.cleared else ""
                print(f"  - {data['name']}  (입력: {key}){tag}")
            else:
                print(f"  - {data['name']}  🔒 (잠김)")
    print("\n[명령어]")
    print("  상태  : 캐릭터 상태창 보기")
    print("  포션  : 포션 사용 (HP 회복)")
    print("  상점  : 포션 구매")
    print("  종료  : 게임 종료")
    if location["is_safe"]:
        print("  (장소 이름 입력) : 해당 던전에 입장")
    story.line("-")


# ============================================================
# 메인 게임 루프
# ============================================================
def main_loop(player, state):
    """이동 / 탐색을 반복하는 메인 루프."""
    # 시작 지역 도착 연출
    move_to(state, state.current)

    while not state.finished:
        if not player.is_alive():
            print("\n💀 당신은 쓰러졌습니다... GAME OVER")
            break

        show_menu(state)
        cmd = input(">> ").strip()

        # 명령어 처리
        if cmd in ("종료", "exit", "quit"):
            print("게임을 종료합니다.")
            return

        elif cmd in ("상태", "상태창", "status"):
            player.show_status()
            continue

        elif cmd in ("포션", "potion"):
            use_potion(player)
            continue

        elif cmd in ("상점", "store"):
            store(player)
            continue
        # 그 외 입력 → 장소 이동 시도
        target = world.normalize_input(cmd)
        if target is None:
            print("❓ 알 수 없는 명령어이거나 장소입니다. 다시 시도해 주세요.")
            continue
        if target not in state.unlocked:
            print("🔒 아직 갈 수 없는 장소입니다. 앞 던전을 먼저 클리어하세요.")
            continue
        if target == state.current:
            print("이미 이 장소에 있습니다.")
            continue

        # ── 이동 처리 ──
        move_to(state, target)

        # 던전이면 곧바로 진입 (마을은 그냥 머무름)
        if not world.get_location(target)["is_safe"]:
            enter_dungeon(state, player, target)
