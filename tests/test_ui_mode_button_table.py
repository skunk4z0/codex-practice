import pytest

from ui import MODE_ALIAS, MODE_BUTTON_TABLE, get_mode_spec


def test_mode_button_table_contract_and_unknown_mode_behavior():
    required_modes = {"OR", "OR_SB", "3BET", "ROL_NONBB", "ROL_BB_OOP", "ROL_BBVS_SB"}
    allowed_slots = {"fold", "raise", "limp_call"}

    for mode in required_modes:
        spec = get_mode_spec(mode)
        assert isinstance(spec, list)
        for entry in spec:
            assert isinstance(entry, tuple)
            assert len(entry) == 3
            slot, label, action = entry
            assert slot in allowed_slots
            assert isinstance(label, str) and label != ""
            assert isinstance(action, str) and action != ""

    three_bet_raise = [entry for entry in MODE_BUTTON_TABLE["3BET"] if entry[0] == "raise"]
    assert len(three_bet_raise) == 1
    _, label, action = three_bet_raise[0]
    assert label == "3BET"
    assert action == "RAISE"

    assert MODE_ALIAS.get("OR_SB") == "OR"
    assert get_mode_spec("OR_SB") is get_mode_spec("OR")

    with pytest.raises(ValueError):
        get_mode_spec("UNKNOWN")
