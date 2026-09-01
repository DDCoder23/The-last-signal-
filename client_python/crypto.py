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

        z ^= z >> 31

        return z & MASK64
