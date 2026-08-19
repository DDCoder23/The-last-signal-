import hashlib

import pytest


MASK_64 = 0xFFFFFFFFFFFFFFFF


# ============================================================
# SPLITMIX64
# ============================================================

def splitmix64(state):
    """
    Générateur SplitMix64 déterministe.

    Retourne :
        (nouvel_etat, valeur)
    """

    state = (
        state + 0x9E3779B97F4A7C15
    ) & MASK_64

    z = state

    z = (
        (z ^ (z >> 30))
        * 0xBF58476D1CE4E5B9
    ) & MASK_64

    z = (
        (z ^ (z >> 27))
        * 0x94D049BB133111EB
    ) & MASK_64

    z ^= z >> 31

    z &= MASK_64

    return state, z


# ============================================================
# DERIVATION DES SEEDS
# ============================================================

ROTOR_DOMAIN = b"TheLastSignal-Rotor-v1"


def derive_rotor_seed(
    communication_key,
    rotor_id,
):
    """
    Dérive le seed d'un rotor.

    communication_key :
        64 octets.

    rotor_id :
        entier compris entre 1 et 16.
    """

    assert len(communication_key) == 64
    assert 1 <= rotor_id <= 16

    rotor_id_bytes = rotor_id.to_bytes(
        4,
        "big",
    )

    data = (
        communication_key
        + ROTOR_DOMAIN
        + rotor_id_bytes
    )

    digest = hashlib.sha256(data).digest()

    return int.from_bytes(
        digest[:8],
        "big",
    )


# ============================================================
# GÉNÉRATION D'UN ROTOR
# ============================================================

def generate_rotor(
    communication_key,
    rotor_id,
):
    """
    Génère une permutation de 0..255.
    """

    seed = derive_rotor_seed(
        communication_key,
        rotor_id,
    )

    rotor = list(range(256))

    state = seed

    for i in range(255, 0, -1):

        state, random_value = splitmix64(
            state
        )

        j = random_value % (i + 1)

        rotor[i], rotor[j] = (
            rotor[j],
            rotor[i],
        )

    return rotor


# ============================================================
# PERMUTATION INVERSE
# ============================================================

def inverse_permutation(permutation):

    inverse = [0] * 256

    for index, value in enumerate(permutation):
        inverse[value] = index

    return inverse


# ============================================================
# ROTOR FORWARD
# ============================================================

def rotor_forward(
    value,
    position,
    permutation,
):
    """
    Passage normal dans le rotor.
    """

    value = (
        value + position
    ) & 0xFF

    value = permutation[value]

    value = (
        value - position
    ) & 0xFF

    return value


# ============================================================
# ROTOR INVERSE
# ============================================================

def rotor_inverse(
    value,
    position,
    permutation,
):
    """
    Passage inverse dans le rotor.
    """

    inverse = inverse_permutation(
        permutation
    )

    value = (
        value + position
    ) & 0xFF

    value = inverse[value]

    value = (
        value - position
    ) & 0xFF

    return value


# ============================================================
# FIXTURE
# ============================================================

@pytest.fixture
def communication_key():

    return bytes(
        range(64)
    )


# ============================================================
# TESTS SPLITMIX64
# ============================================================

def test_splitmix64_deterministic():

    state1, value1 = splitmix64(123456789)

    state2, value2 = splitmix64(123456789)

    assert state1 == state2
    assert value1 == value2


def test_splitmix64_different_seeds():

    _, value1 = splitmix64(1)

    _, value2 = splitmix64(2)

    assert value1 != value2


def test_splitmix64_is_u64():

    state, value = splitmix64(
        0xFFFFFFFFFFFFFFFF
    )

    assert 0 <= state <= MASK_64
    assert 0 <= value <= MASK_64


# ============================================================
# TESTS DES SEEDS
# ============================================================

def test_rotor_seed_deterministic(
    communication_key,
):

    seed1 = derive_rotor_seed(
        communication_key,
        1,
    )

    seed2 = derive_rotor_seed(
        communication_key,
        1,
    )

    assert seed1 == seed2


def test_rotor_seeds_are_different(
    communication_key,
):

    seeds = [
        derive_rotor_seed(
            communication_key,
            rotor_id,
        )
        for rotor_id in range(1, 17)
    ]

    assert len(set(seeds)) == 16


def test_rotor_seed_is_u64(
    communication_key,
):

    for rotor_id in range(1, 17):

        seed = derive_rotor_seed(
            communication_key,
            rotor_id,
        )

        assert 0 <= seed <= MASK_64


# ============================================================
# TESTS DES ROTORS
# ============================================================

def test_rotor_has_256_values(
    communication_key,
):

    rotor = generate_rotor(
        communication_key,
        1,
    )

    assert len(rotor) == 256


def test_rotor_is_permutation(
    communication_key,
):

    rotor = generate_rotor(
        communication_key,
        1,
    )

    assert sorted(rotor) == list(
        range(256)
    )


def test_all_16_rotors_are_valid(
    communication_key,
):

    for rotor_id in range(1, 17):

        rotor = generate_rotor(
            communication_key,
            rotor_id,
        )

        assert len(rotor) == 256

        assert sorted(rotor) == list(
            range(256)
        )


def test_rotor_is_deterministic(
    communication_key,
):

    rotor1 = generate_rotor(
        communication_key,
        1,
    )

    rotor2 = generate_rotor(
        communication_key,
        1,
    )

    assert rotor1 == rotor2


def test_rotors_are_different(
    communication_key,
):

    rotors = [
        generate_rotor(
            communication_key,
            rotor_id,
        )
        for rotor_id in range(1, 17)
    ]

    for i in range(16):

        for j in range(i + 1, 16):

            assert rotors[i] != rotors[j]


# ============================================================
# TEST FORWARD / INVERSE
# ============================================================

@pytest.mark.parametrize(
    "value",
    range(256),
)
@pytest.mark.parametrize(
    "position",
    [
        0,
        1,
        2,
        127,
        128,
        254,
        255,
    ],
)
def test_rotor_forward_inverse(
    communication_key,
    value,
    position,
):

    rotor = generate_rotor(
        communication_key,
        1,
    )

    encrypted = rotor_forward(
        value,
        position,
        rotor,
    )

    decrypted = rotor_inverse(
        encrypted,
        position,
        rotor,
    )

    assert decrypted == value


# ============================================================
# TEST DES 16 ROTORS
# ============================================================

@pytest.mark.parametrize(
    "value",
    range(256),
)
def test_all_16_rotors_forward_inverse(
    communication_key,
    value,
):

    for rotor_id in range(1, 17):

        rotor = generate_rotor(
            communication_key,
            rotor_id,
        )

        position = (
            rotor_id * 17
        ) & 0xFF

        encrypted = rotor_forward(
            value,
            position,
            rotor,
        )

        decrypted = rotor_inverse(
            encrypted,
            position,
            rotor,
        )

        assert decrypted == value
