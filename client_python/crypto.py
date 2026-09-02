import hashlib


MASK_64 = 0xFFFFFFFFFFFFFFFF

ROTOR_COUNT = 16
ROTOR_SIZE = 256
COMMUNICATION_KEY_SIZE = 64

ROTOR_DOMAIN = b"TheLastSignal-Rotor-v1"


'''
============================================================
                   SPLITMIX64
============================================================
'''
class SplitMix64:

    def __init__(self, seed):
        self.state = seed & MASK_64

    def next(self):

        self.state = (
            self.state
            + 0x9E3779B97F4A7C15
        ) & MASK_64

        z = self.state

        z = (
            (z ^ (z >> 30))
            * 0xBF58476D1CE4E5B9
        ) & MASK_64

        z = (
            (z ^ (z >> 27))
            * 0x94D049BB133111EB
        ) & MASK_64

        z ^= z >> 31

        return z & MASK_64



'''
============================================================
                   DERIVATION DES SEEDS
============================================================
'''


def derive_rotor_seed(
    communication_key,
    rotor_id,
):

    if len(communication_key) != COMMUNICATION_KEY_SIZE:
        raise ValueError(
            "Communication_key must be exactly 64 bytes"
        )

    if not 1 <= rotor_id <= ROTOR_COUNT:
        raise ValueError(
            "rotor_id must be between 1 and 16"
        )

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

'''
============================================================
                   FISHER-YATES
============================================================
'''


def fisher_yates(seed):

    rotor = list(range(ROTOR_SIZE))

    rng = SplitMix64(seed)

    for i in range(
        ROTOR_SIZE - 1,
        0,
        -1,
    ):

        j = rng.next() % (i + 1)

        rotor[i], rotor[j] = (
            rotor[j],
            rotor[i],
        )

    return rotor

'''
============================================================
                   GÉNÉRATION D'UN ROTOR
============================================================
'''


def generate_rotor(
    communication_key,
    rotor_id,
):

    seed = derive_rotor_seed(
        communication_key,
        rotor_id,
    )

    return fisher_yates(seed)

'''
============================================================
                   GÉNÉRATION DES 16 ROTORS
============================================================
'''


def generate_rotors(
    communication_key,
):

    if len(communication_key) != COMMUNICATION_KEY_SIZE:
        raise ValueError(
            "Communication_key must be exactly 64 bytes"
        )

    return [
        generate_rotor(
            communication_key,
            rotor_id,
        )
        for rotor_id in range(
            1,
            ROTOR_COUNT + 1,
        )
    ]

'''
============================================================
                   PERMUTATION INVERSE
============================================================
'''


def inverse_permutation(permutation):

    if len(permutation) != ROTOR_SIZE:
        raise ValueError(
            "A rotor must contain exactly 256 values"
        )

    inverse = [0] * ROTOR_SIZE

    for index, value in enumerate(permutation):
        inverse[value] = index

    return inverse

'''
============================================================
                   ROTOR FORWARD
============================================================
'''


def rotor_forward(
    value,
    position,
    permutation,
):

    value = (
        value + position
    ) & 0xFF

    value = permutation[value]

    value = (
        value - position
    ) & 0xFF

    return value

'''
============================================================
                   ROTOR INVERSE
============================================================
'''


def rotor_inverse(
    value,
    position,
    permutation,
):

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