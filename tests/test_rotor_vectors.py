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


def test_reference_vector_packet_type_1():
    communication_key = bytes.fromhex(
        "000102030405060708090a0b0c0d0e0f"
        "101112131415161718191a1b1c1d1e1f"
        "202122232425262728292a2b2c2d2e2f"
        "303132333435363738393a3b3c3d3e3f"
    )

    packet_type = 1

    plaintext = bytes.fromhex(
        "000102030405060708090a0b0c0d0e0f"
    )

    expected_ciphertext = bytes.fromhex(
        "e2d0c4f302ea3da12ce8af9b852460d4"
    )

    ciphertext = encrypt_reference(
        communication_key,
        packet_type,
        plaintext,
    )

    assert ciphertext == expected_ciphertext
def test_reference_vector_packet_type_2():
    communication_key = bytes.fromhex(
        "000102030405060708090a0b0c0d0e0f"
        "101112131415161718191a1b1c1d1e1f"
        "202122232425262728292a2b2c2d2e2f"
        "303132333435363738393a3b3c3d3e3f"
    )

    plaintext = bytes.fromhex(
        "000102030405060708090a0b0c0d0e0f"
    )

    expected_ciphertext = encrypt_reference(
        communication_key,
        2,
        plaintext,
    )

    assert expected_ciphertext != bytes.fromhex(
        "e2d0c4f302ea3da12ce8af9b852460d4"
    )
def test_reference_vector_packet_type_9():
    communication_key = bytes.fromhex(
        "000102030405060708090a0b0c0d0e0f"
        "101112131415161718191a1b1c1d1e1f"
        "202122232425262728292a2b2c2d2e2f"
        "303132333435363738393a3b3c3d3e3f"
    )

    plaintext = bytes.fromhex(
        "000102030405060708090a0b0c0d0e0f"
    )

    expected_ciphertext = encrypt_reference(
        communication_key,
        9,
        plaintext,
    )

    assert expected_ciphertext != bytes.fromhex(
        "e2d0c4f302ea3da12ce8af9b852460d4"
    )
