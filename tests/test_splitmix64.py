import pytest


MASK64 = 0xFFFFFFFFFFFFFFFF


class SplitMix64:
    def __init__(self, seed: int):
        self.state = seed & MASK64

    def next(self) -> int:
        self.state = (
            self.state + 0x9E3779B97F4A7C15
        ) & MASK64

        z = self.state

        z = (
            (z ^ (z >> 30))
            * 0xBF58476D1CE4E5B9
        ) & MASK64

        z = (
            (z ^ (z >> 27))
            * 0x94D049BB133111EB
        ) & MASK64

        z = z ^ (z >> 31)

        return z & MASK64


# ============================================================
# DÉTERMINISME
# ============================================================

def test_same_seed_same_sequence():

    a = SplitMix64(123456789)
    b = SplitMix64(123456789)

    sequence_a = [
        a.next()
        for _ in range(100)
    ]

    sequence_b = [
        b.next()
        for _ in range(100)
    ]

    assert sequence_a == sequence_b


# ============================================================
# SEEDS DIFFÉRENTS
# ============================================================

def test_different_seed_different_sequence():

    a = SplitMix64(123456789)
    b = SplitMix64(987654321)

    sequence_a = [
        a.next()
        for _ in range(20)
    ]

    sequence_b = [
        b.next()
        for _ in range(20)
    ]

    assert sequence_a != sequence_b


# ============================================================
# VALEURS 64 BITS
# ============================================================

def test_output_is_u64():

    generator = SplitMix64(42)

    for _ in range(1000):

        value = generator.next()

        assert 0 <= value <= MASK64


# ============================================================
# ÉTAT QUI AVANCE
# ============================================================

def test_state_changes():

    generator = SplitMix64(42)

    first_state = generator.state

    generator.next()

    assert generator.state != first_state


# ============================================================
# SEED ZÉRO
# ============================================================

def test_zero_seed():

    generator = SplitMix64(0)

    values = [
        generator.next()
        for _ in range(10)
    ]

    assert len(values) == 10
    assert len(set(values)) == 10


# ============================================================
# SEED MAXIMUM
# ============================================================

def test_max_seed():

    generator = SplitMix64(MASK64)

    values = [
        generator.next()
        for _ in range(10)
    ]

    assert len(values) == 10
    assert all(
        0 <= value <= MASK64
        for value in values
    )
