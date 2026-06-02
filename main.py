# -*- coding: utf-8 -*-
"""
main.py  -  통합 진입점
============================================================
실행 방법:
    python main.py

이 게임은 두 팀원의 코드를 합쳐서 동작합니다.

  - 공기민 (Combat.py) : 직업·전투·몬스터·포션 시스템
  - 현민우 (이 파일들)    : 세계관·스토리·지역 이동·엔딩

같은 폴더에 다음 파일들이 모두 있어야 합니다:
    Combat.py    (공기민)
    world.py        (현민우)
    story.py        (현민우)
    movement.py     (현민우)
    main.py         (현민우 — 본 파일)
    level.py        (유채운)
    store.py        (유채운)
    reset.py        (유채운)
"""

import story
import movement
from Combat import select_job   # ← 공기민의 직업 선택 함수
import reset

def main():
    # 1) 오프닝 인트로 (현민우)
    story.show_opening()

    # 2) 직업 선택 — 공기민의 select_job() 호출
    print()
    player = select_job()
    if player is None:
        # 잘못된 입력 시 select_job() 이 None 을 반환함 → 종료
        return

    # 3) 모험가의 이름을 따로 입력받아 player.name 갱신
    #    (공기민의 select_job 은 player.name 을 직업명으로 설정하므로,
    #     실제 모험가 이름으로 덮어쓰기)
    raw_name = input("\n모험가의 이름을 입력하세요: ").strip()
    if raw_name:
        player.name = raw_name

    reset.clear_screen()

    print(f"\n⚔️  [{player.job}] '{player.name}' 의 모험이 시작됩니다!\n")

    # 4) 게임 상태 생성 후 메인 루프 시작 (현민우의 이동 시스템)
    state = movement.GameState()
    movement.main_loop(player, state)

    print("\n플레이해 주셔서 감사합니다! 👋")


if __name__ == "__main__":
    main()
