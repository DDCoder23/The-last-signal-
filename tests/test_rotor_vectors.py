import pytest

from client_python.crypto import (
    RotorState,
    generate_rotor,
    mix_before,
    mix_final,
    rotor_forward,
)


def encrypt_reference(
    communication_key,
    packet_type,
    plaintext,
):
    state = RotorState(
        communication_key=communication_key,
        packet_type=packet_type,
    )

    rotors = [
        generate_rotor(
            communication_key,
            rotor_id,
        )
        for rotor_id in range(1, 17)
    ]

    ciphertext = []
    previous_ciphertext = 0

    for byte_counter, value in enumerate(plaintext):
        state.update()

        positions = state.positions.copy()

        value = mix_before(
            value,
            communication_key,
            positions,
            byte_counter,
            previous_ciphertext,
        )

        for rotor, position in zip(rotors, positions):
            value = rotor_forward(
                value,
                position,
                rotor,
            )

        value = mix_final(
            value,
            communication_key,
            positions,
            byte_counter,
            previous_ciphertext,
            packet_type,
        )

        ciphertext.append(value)
        previous_ciphertext = value

    return bytes(ciphertext)


@pytest.mark.parametrize(
    "packet_type, expected",
    [
        (1, "e2d0c4f302ea3da12ce8af9b852460d4"),
        (2, "7fabeba06378b7008931bb28552e9c54"),
        (3, "0bd95e008752e01024d66fc1e2927d9a"),
        (4, "8169db319e9d65941cb6712d06c7f9e5"),
        (5, "95997b1d3274ba5b25f2a747337b06e3"),
        (6, "0a79ca20d68373815974a73c4e39db8e"),
        (7, "c746f799a8d46175cbfc50cd80fe7c85"),
        (8, "3cef509235062d02e5c7856d666ccc35"),
        (9, "696106774cfcaffd46d70629e4b00e1c"),
    ],
)
def test_reference_vectors_all_packet_types(
    packet_type,
    expected,
):
    communication_key = bytes(range(64))
    plaintext = bytes(range(16))

    ciphertext = encrypt_reference(
        communication_key,
        packet_type,
        plaintext,
    )

    assert ciphertext == bytes.fromhex(expected)
