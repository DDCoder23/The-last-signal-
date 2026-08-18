import pytest


# ============================================================
# OUTILS
# ============================================================

MASK = 0xFF


def rotl8(value: int, shift: int) -> int:
    """Rotation circulaire gauche sur 8 bits."""
    shift &= 7

    if shift == 0:
        return value & MASK

    return (
        ((value << shift) | (value >> (8 - shift)))
        & MASK
    )


def rotr8(value: int, shift: int) -> int:
    """Rotation circulaire droite sur 8 bits."""
    shift &= 7

    if shift == 0:
        return value & MASK

    return (
        ((value >> shift) | (value << (8 - shift)))
        & MASK
    )


def add8(a: int, b: int) -> int:
    """Addition modulo 256."""
    return (a + b) & MASK


def sub8(a: int, b: int) -> int:
    """Soustraction modulo 256."""
    return (a - b) & MASK


# ============================================================
# DONNÉES DE TEST
# ============================================================

@pytest.fixture
def test_data():
    """
    Données entièrement déterministes.

    Elles ne servent PAS de vraies clés.
    Elles servent uniquement à vérifier que
    chiffrement et déchiffrement sont inverses.
    """

    key = bytes(range(64))

    state = bytes(
        (i * 37 + 11) & 0xFF
        for i in range(64)
    )

    rotor_positions = [
        13, 87, 201, 44,
        152, 9, 73, 241,
        61, 188, 35, 116,
        222, 18, 94, 167,
    ]

    return {
        "key": key,
        "state": state,
        "rotor_positions": rotor_positions,
        "packet_type": 3,
        "byte_counter": 42,
        "previous_ciphertext": 91,
    }


# ============================================================
# GROUPES DE ROTORS
# ============================================================

def rotor_groups(positions):
    r = positions

    g1 = r[0] ^ r[4] ^ r[8] ^ r[12]
    g2 = r[1] ^ r[5] ^ r[9] ^ r[13]
    g3 = r[2] ^ r[6] ^ r[10] ^ r[14]
    g4 = r[3] ^ r[7] ^ r[11] ^ r[15]

    return g1, g2, g3, g4


# ============================================================
# MIX AVANT
# ============================================================

def mix_before(
    x,
    key,
    state,
    rotor_positions,
    packet_type,
    byte_counter,
    previous_ciphertext,
):
    """
    MIX_AVANT.

    Cette fonction doit être strictement réversible.
    """

    g1, g2, _, _ = rotor_groups(rotor_positions)

    k0 = key[byte_counter % 64]
    k1 = key[(byte_counter + 17) % 64]

    s0 = state[3]

    # 1. XOR k0
    x ^= k0

    # 2. + s0
    x = add8(x, s0)

    # 3. ROTL8
    rotation = (
        state[11]
        ^ byte_counter
        ^ positions[7]
    ) & 7

    x = rotl8(x, rotation)

    # 4. XOR previous ciphertext
    x ^= previous_ciphertext

    # 5. - G1
    x = sub8(x, g1)

    # 6. ROTL8
    rotation = (
        state[27]
        ^ byte_counter
        ^ positions[8]
    ) & 7

    x = rotl8(x, rotation)

    # 7. + G2
    x = add8(x, g2)

    # 8. XOR k1
    x ^= k1

    return x & MASK


# ============================================================
# INVERSE MIX AVANT
# ============================================================

def inverse_mix_before(
    x,
    key,
    state,
    rotor_positions,
    packet_type,
    byte_counter,
    previous_ciphertext,
):
    """
    Inverse exacte de MIX_AVANT.
    """

    g1, g2, _, _ = rotor_groups(rotor_positions)

    k0 = key[byte_counter % 64]
    k1 = key[(byte_counter + 17) % 64]

    s0 = state[3]

    # Inverse 8
    x ^= k1

    # Inverse 7
    x = sub8(x, g2)

    # Inverse 6
    rotation = (
        state[27]
        ^ byte_counter
        ^ positions[8]
    ) & 7

    x = rotr8(x, rotation)

    # Inverse 5
    x = add8(x, g1)

    # Inverse 4
    x ^= previous_ciphertext

    # Inverse 3
    rotation = (
        state[11]
        ^ byte_counter
        ^ positions[7]
    ) & 7

    x = rotr8(x, rotation)

    # Inverse 2
    x = sub8(x, s0)

    # Inverse 1
    x ^= k0

    return x & MASK


# ============================================================
# MIX FINAL
# ============================================================

def mix_final(
    x,
    key,
    state,
    rotor_positions,
    packet_type,
    byte_counter,
    previous_ciphertext,
):
    """
    MIX_FINAL.
    """

    _, _, g3, g4 = rotor_groups(rotor_positions)

    k0 = key[byte_counter % 64]
    k2 = key[(byte_counter + 43) % 64]

    s2 = state[42]

    # 1. XOR G3
    x ^= g3

    # 2. + k2
    x = add8(x, k2)

    # 3. ROTL8
    rotation = (
        state[19]
        ^ byte_counter
        ^ positions[7]
        ^ packet_type
    ) & 7

    x = rotl8(x, rotation)

    # 4. XOR previous ciphertext
    x ^= previous_ciphertext

    # 5. + s2
    x = add8(x, s2)

    # 6. ROTL8
    rotation = (
        state[47]
        ^ byte_counter
        ^ positions[8]
    ) & 7

    x = rotl8(x, rotation)

    # 7. - G4
    x = sub8(x, g4)

    # 8. XOR k0
    x ^= k0

    return x & MASK


# ============================================================
# INVERSE MIX FINAL
# ============================================================

def inverse_mix_final(
    x,
    key,
    state,
    rotor_positions,
    packet_type,
    byte_counter,
    previous_ciphertext,
):
    """
    Inverse exacte de MIX_FINAL.
    """

    _, _, g3, g4 = rotor_groups(rotor_positions)

    k0 = key[byte_counter % 64]
    k2 = key[(byte_counter + 43) % 64]

    s2 = state[42]

    # Inverse 8
    x ^= k0

    # Inverse 7
    x = add8(x, g4)

    # Inverse 6
    rotation = (
        state[47]
        ^ byte_counter
        ^ positions[8]
    ) & 7

    x = rotr8(x, rotation)

    # Inverse 5
    x = sub8(x, s2)

    # Inverse 4
    x ^= previous_ciphertext

    # Inverse 3
    rotation = (
        state[19]
        ^ byte_counter
        ^ positions[7]
        ^ packet_type
    ) & 7

    x = rotr8(x, rotation)

    # Inverse 2
    x = sub8(x, k2)

    # Inverse 1
    x ^= g3

    return x & MASK


# ============================================================
# TESTS DES ROTATIONS
# ============================================================

@pytest.mark.parametrize("value", range(256))
@pytest.mark.parametrize("shift", range(8))
def test_rotl_rotr_inverse(value, shift):
    result = rotl8(value, shift)
    result = rotr8(result, shift)

    assert result == value


# ============================================================
# TEST MIX AVANT
# ============================================================

@pytest.mark.parametrize("plaintext", range(256))
def test_mix_before_is_reversible(test_data, plaintext):

    encrypted = mix_before(
        plaintext,
        **test_data,
    )

    decrypted = inverse_mix_before(
        encrypted,
        **test_data,
    )

    assert decrypted == plaintext


# ============================================================
# TEST MIX FINAL
# ============================================================

@pytest.mark.parametrize("value", range(256))
def test_mix_final_is_reversible(test_data, value):

    encrypted = mix_final(
        value,
        **test_data,
    )

    decrypted = inverse_mix_final(
        encrypted,
        **test_data,
    )

    assert decrypted == value


# ============================================================
# TEST CHAÎNE MIX AVANT → MIX FINAL
# ============================================================

@pytest.mark.parametrize("plaintext", range(256))
def test_complete_mix_chain(test_data, plaintext):

    value = mix_before(
        plaintext,
        **test_data,
    )

    value = mix_final(
        value,
        **test_data,
    )

    value = inverse_mix_final(
        value,
        **test_data,
    )

    value = inverse_mix_before(
        value,
        **test_data,
    )
    print(value,plaintext)
    assert value == plaintext
