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
# ============================================================
# ROTOR 2
# ============================================================

def test_rotor_2_rotates_by_key_each_byte():

    key = bytes(range(64))

    state = RotorState(
        communication_key=key,
        packet_type=1,
    )

    # Pour le test, on utilise le premier octet de la clé.
    key_value = key[0]

    state.update()

    assert state.positions[1] == key_value

    state.update()

    assert state.positions[1] == (
        key_value * 2
    ) & 0xFF


def test_rotor_2_wraps():

    key = bytes([7] * 64)

    state = RotorState(
        communication_key=key,
        packet_type=1,
    )

    state.positions[1] = 250

    state.update()

    assert state.positions[1] == 1
# ============================================================
# ROTOR 5
# ============================================================

def test_rotor_5_reacts_to_rotor_2_full_rotation():

    key = bytes([1] * 64)

    state = RotorState(
        communication_key=key,
        packet_type=1,
    )

    for _ in range(256):
        state.update()

    assert state.positions[1] == 0
    assert state.positions[4] == 251
# ============================================================
# ROTOR 3
# ============================================================

def test_rotor_3_rotates_by_packet_type():

    key = bytes([1] * 64)

    state = RotorState(
        communication_key=key,
        packet_type=7,
    )

    state.update()

    assert state.positions[2] == 249

    state.update()

    assert state.positions[2] == 242


def test_rotor_3_wraps():

    key = bytes([1] * 64)

    state = RotorState(
        communication_key=key,
        packet_type=7,
    )

    state.positions[2] = 3

    state.update()

    assert state.positions[2] == 252
# ============================================================
# ROTOR 6
# ============================================================

def test_rotor_6_rotates_by_seed_every_two_bytes():

    key = bytes([1] * 64)

    state = RotorState(
        communication_key=key,
        packet_type=1,
    )

    seed = derive_rotor_seed(key, 6)
    seed_value = seed & 0xFF

    # 1er octet : pas de rotation
    state.update()

    assert state.positions[5] == 0

    # 2e octet : + seed
    state.update()

    assert state.positions[5] == seed_value

    # 3e octet : pas de rotation
    state.update()

    assert state.positions[5] == seed_value

    # 4e octet : + seed
    state.update()

    assert state.positions[5] == (
        seed_value * 2
    ) & 0xFF
    def test_rotor_6_wraps():

    key = bytes([1] * 64)

    state = RotorState(
        communication_key=key,
        packet_type=1,
    )

    seed = derive_rotor_seed(key, 6)
    seed_value = seed & 0xFF

    state.positions[5] = (
        256 - seed_value
    ) & 0xFF

    state.update()
    state.update()

    assert state.positions[5] == 0
