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


def test_generate_reference_vector():
    communication_key = bytes(range(64))
    packet_type = 1
    plaintext = bytes(range(16))

    ciphertext = encrypt_reference(
        communication_key,
        packet_type,
        plaintext,
    )

    print()
    print("Communication key :", communication_key.hex())
    print("Packet type       :", packet_type)
    print("Plaintext         :", plaintext.hex())
    print("Ciphertext        :", ciphertext.hex())

    assert len(ciphertext) == len(plaintext)
