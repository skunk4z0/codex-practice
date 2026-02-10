from __future__ import annotations

import random
import sys
from pathlib import Path

from config import FINAL_TAGS_JSON_PATH
from core.engine import PokerEngine
from core.models import Difficulty
from core.generator import JuegoProblemGenerator
from juego_judge import JUEGOJudge
from json_range_repository import JsonRangeRepository


def main() -> int:
    json_path = Path(FINAL_TAGS_JSON_PATH)
    if not json_path.exists():
        print(
            "[SMOKE] missing required file: data/final_tags.json\n"
            f"Expected path: {json_path}\n"
            "Build it first, e.g.:\n"
            "  python -m tools.build_final_tags_json",
            file=sys.stderr,
        )
        return 2

    repo = JsonRangeRepository(json_path)
    judge = JUEGOJudge(repo)
    gen = JuegoProblemGenerator(rng=random.Random(0), positions_3bet=[])
    engine = PokerEngine(generator=gen, juego_judge=judge, enable_debug=False)

    engine.start_juego(Difficulty.BEGINNER)
    generated = engine.new_question()
    ctx = generated.ctx

    user_action = "FOLD"
    res = engine.submit(user_action)

    judge_result = getattr(res, "judge_result", None)
    expected_action = getattr(judge_result, "action", "")

    print(f"kind/mode: {generated.problem_type.name}/{generated.answer_mode}")
    print(f"position: {ctx.position}")
    print(f"hand: {ctx.excel_hand_key}")
    print(f"expected/correct: {expected_action}/{res.is_correct}")
    print(f"user_action: {user_action}")
    print(f"result summary: {res.text}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
