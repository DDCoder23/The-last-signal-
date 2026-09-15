
const MASK_64: u64 = 0xFFFF_FFFF_FFFF_FFFF;

pub struct SplitMix64 {
    state: u64,
}

impl SplitMix64 {
    pub fn new(seed: u64) -> Self {
        Self {
            state: seed & MASK_64,
        }
    }

    pub fn next(&mut self) -> u64 {
        self.state = self
            .state
            .wrapping_add(0x9E37_79B9_7F4A_7C15);

        let mut z = self.state;

        z = (z ^ (z >> 30))
            .wrapping_mul(0xBF58_476D_1CE4_E5B9);

        z = (z ^ (z >> 27))
            .wrapping_mul(0x94D0_49BB_1331_11EB);

        z ^= z >> 31;

        z & MASK_64
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn splitmix64_same_seed_same_sequence() {
        let mut rng1 = SplitMix64::new(0);
        let mut rng2 = SplitMix64::new(0);

        for _ in 0..100 {
            assert_eq!(rng1.next(), rng2.next());
        }
    }

    #[test]
    fn splitmix64_different_seed_different_sequence() {
        let mut rng1 = SplitMix64::new(0);
        let mut rng2 = SplitMix64::new(1);

        let sequence1: Vec<u64> = (0..100).map(|_| rng1.next()).collect();
        let sequence2: Vec<u64> = (0..100).map(|_| rng2.next()).collect();

        assert_ne!(sequence1, sequence2);
    }

    #[test]
    fn splitmix64_state_changes() {
        let mut rng = SplitMix64::new(0);

        let first = rng.next();
        let second = rng.next();

        assert_ne!(first, second);
    }

    #[test]
    fn splitmix64_zero_seed() {
        let mut rng = SplitMix64::new(0);

        assert_eq!(
            rng.next(),
            0xE220_A839_7B1D_CDAFu64
        );
    }

    #[test]
    fn splitmix64_max_seed() {
        let mut rng = SplitMix64::new(u64::MAX);

        let first = rng.next();
        let second = rng.next();

        assert_ne!(first, second);
    }
}

