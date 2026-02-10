from types import SimpleNamespace

from core.engine import PokerEngine, SubmitResult
from core.models import Difficulty, OpenRaiseProblemContext, ProblemType


class _FakeGenerator:
    def generate(self, difficulty):
        ctx = OpenRaiseProblemContext(
            hole_cards=("As", "Kd"),
            position="CO",
            open_size_bb=3.0,
            loose_player_exists=False,
            excel_hand_key="AKo",
            excel_position_key="CO",
            limpers=0,
        )
        return SimpleNamespace(
            problem_type=ProblemType.JUEGO_OR,
            ctx=ctx,
            answer_mode="OR",
            header_text="test",
        )


class _FakeJudge:
    def judge_or(self, position, hand, user_action, loose):
        return SimpleNamespace(correct=True, reason="ok", debug={"tag_upper": "FOLD"})


def test_submit_normal_case_returns_submit_result_not_none():
    eng = PokerEngine(generator=_FakeGenerator(), juego_judge=_FakeJudge(), enable_debug=False)
    eng.start_juego(Difficulty.BEGINNER)
    eng.new_question()

    res = eng.submit("RAISE")

    assert res is not None
    assert isinstance(res, SubmitResult)
    assert isinstance(res.text, str) and res.text != ""
    assert isinstance(res.show_next_button, bool)
    assert isinstance(res.show_followup_buttons, bool)
    assert isinstance(res.hide_followup_buttons, bool)
    assert res.judge_result is not None
