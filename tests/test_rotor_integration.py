import pytest

from client_python.crypto import (
    RotorState,
    generate_rotor,
    rotor_forward,
    rotor_inverse,
)


@pytest.mark.parametrize(
    "value",
    range(256),
)
def test_rotor_state_round_trip(
    value,
):

    communication_key = bytes(range(64))

    state = RotorState(
        communication_key=communication_key,
        packet_type=1,
    )

    rotors = [
        generate_rotor(
            communication_key,
            rotor_id,
        )
        for rotor_id in range(1, 17)
    ]

    state.update()

    positions = state.positions.copy()

    original = value

    # Forward : R1 → R16
    for rotor, position in zip(
        rotors,
        positions,
    ):
        value = rotor_forward(
            value,
            position,
            rotor,
        )

    # Inverse : R16 → R1
    for rotor, position in reversed(
        list(zip(rotors, positions))
    ):
        value = rotor_inverse(
            value,
            position,
            rotor,
        )

    assert value == original
