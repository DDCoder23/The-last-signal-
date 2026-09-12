import pytest

from client_python.crypto import RotorState


# ============================================================
# INITIALISATION
# ============================================================

def test_rotor_state_has_16_positions():

    state = RotorState(
        communication_key=bytes(range(64)),
        packet_type=1,
    )

    assert len(state.positions) == 16


def test_rotor_state_starts_at_zero():

    state = RotorState(
        communication_key=bytes(range(64)),
        packet_type=1,
    )

    assert state.positions == [0] * 16


# ============================================================
# ROTOR 1
# ============================================================

def test_rotor_1_rotates_by_one_each_byte():

    state = RotorState(
        communication_key=bytes(range(64)),
        packet_type=1,
    )

    state.update()

    assert state.positions[0] == 1

    state.update()

    assert state.positions[0] == 2


def test_rotor_1_wraps():

    state = RotorState(
        communication_key=bytes(range(64)),
        packet_type=1,
    )

    state.positions[0] = 255

    state.update()

    assert state.positions[0] == 0


# ============================================================
# TOURS COMPLETS
# ============================================================

def test_rotor_1_full_rotation():

    state = RotorState(
        communication_key=bytes(range(64)),
        packet_type=1,
    )

    for _ in range(256):
        state.update()

    assert state.positions[0] == 0


def test_rotor_4_reacts_to_rotor_1_full_rotation():

    state = RotorState(
        communication_key=bytes(range(64)),
        packet_type=1,
    )

    for _ in range(256):
        state.update()

    assert state.positions[3] == 8
