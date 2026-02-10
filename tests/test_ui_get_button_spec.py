from types import SimpleNamespace

from ui import get_button_spec


class DummyProblemType:
    def __init__(self, name: str) -> None:
        self.name = name


def test_get_button_spec_rol_bbvssb_returns_check_and_raise():
    ctx = SimpleNamespace(position="BBvsSB")
    spec = get_button_spec(DummyProblemType("JUEGO_ROL"), ctx)

    assert len(spec) == 2
    assert spec[0] == ("fold", "CHECK", "CHECK")
    assert spec[1] == ("raise", "RAISE", "RAISE")


def test_get_button_spec_3bet_raise_slot_is_3bet_raise_action():
    spec = get_button_spec(DummyProblemType("JUEGO_3BET"), None)

    raise_entries = [entry for entry in spec if entry[0] == "raise"]
    assert len(raise_entries) == 1
    _, label, action = raise_entries[0]
    assert label == "3BET"
    assert action == "RAISE"
