use sha2::{Digest, Sha256};
const MASK_64: u64 = 0xFFFF_FFFF_FFFF_FFFF;
const COMMUNICATION_KEY_SIZE: usize = 64;
const ROTOR_COUNT: usize = 16;
const ROTOR_DOMAIN: &[u8] = b"TheLastSignal-Rotor-v1";
const ROTOR_SIZE: usize = 256;


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


pub fn derive_rotor_seed(
    communication_key: &[u8],
    rotor_id: u8,
) -> Result<u64, &'static str> {
    if communication_key.len() != COMMUNICATION_KEY_SIZE {
        return Err("Communication_key must be exactly 64 bytes");
    }

    if !(1..=ROTOR_COUNT as u8).contains(&rotor_id) {
        return Err("rotor_id must be between 1 and 16");
    }

    let mut hasher = Sha256::new();

    hasher.update(communication_key);
    hasher.update(ROTOR_DOMAIN);
    hasher.update((rotor_id as u32).to_be_bytes());

    let digest = hasher.finalize();

    let seed = u64::from_be_bytes(
        digest[..8]
            .try_into()
            .expect("SHA-256 digest is at least 8 bytes"),
    );

    Ok(seed)
}

pub fn fisher_yates(seed: u64) -> [u8; ROTOR_SIZE] {
    let mut rotor = [0u8; ROTOR_SIZE];

    for (index, value) in rotor.iter_mut().enumerate() {
        *value = index as u8;
    }

    let mut rng = SplitMix64::new(seed);

    for i in (1..ROTOR_SIZE).rev() {
        let j = (rng.next() % (i as u64 + 1)) as usize;

        rotor.swap(i, j);
    }

    rotor
}


pub fn generate_rotor(
    communication_key: &[u8],
    rotor_id: u8,
) -> Result<[u8; ROTOR_SIZE], &'static str> {
    let seed = derive_rotor_seed(communication_key, rotor_id)?;

    Ok(fisher_yates(seed))
}

pub fn generate_rotors(
    communication_key: &[u8],
) -> Result<[[u8; ROTOR_SIZE]; ROTOR_COUNT], &'static str> {
    if communication_key.len() != COMMUNICATION_KEY_SIZE {
        return Err("Communication_key must be exactly 64 bytes");
    }

    let mut rotors = [[0u8; ROTOR_SIZE]; ROTOR_COUNT];

    for rotor_id in 1..=ROTOR_COUNT {
        rotors[rotor_id - 1] =
            generate_rotor(communication_key, rotor_id as u8)?;
    }

    Ok(rotors)
}
pub fn rotor_forward(
    value: u8,
    position: u8,
    permutation: &[u8; ROTOR_SIZE],
) -> u8 {
    let shifted = value.wrapping_add(position);
    let permuted = permutation[shifted as usize];
    permuted.wrapping_sub(position)
}

pub fn inverse_permutation(
    permutation: &[u8; ROTOR_SIZE],
) -> [u8; ROTOR_SIZE] {
    let mut inverse = [0u8; ROTOR_SIZE];

    for (index, &value) in permutation.iter().enumerate() {
        inverse[value as usize] = index as u8;
    }

    inverse
}

pub fn rotor_inverse(
    value: u8,
    position: u8,
    permutation: &[u8; ROTOR_SIZE],
) -> u8 {
    let inverse = inverse_permutation(permutation);
    let shifted = value.wrapping_add(position);
    let permuted = inverse[shifted as usize];

    permuted.wrapping_sub(position)
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
    #[test]
fn derive_rotor_seed_rejects_invalid_key_length() {
    let key = [0u8; 63];

    assert!(
        derive_rotor_seed(&key, 1).is_err()
    );
}

#[test]
fn derive_rotor_seed_rejects_invalid_rotor_id() {
    let key = [0u8; 64];

    assert!(
        derive_rotor_seed(&key, 0).is_err()
    );

    assert!(
        derive_rotor_seed(&key, 17).is_err()
    );
}

#[test]
fn derive_rotor_seed_is_deterministic() {
    let key = [0u8; 64];

    let seed1 = derive_rotor_seed(&key, 1).unwrap();
    let seed2 = derive_rotor_seed(&key, 1).unwrap();

    assert_eq!(seed1, seed2);
}

#[test]
fn derive_rotor_seed_differs_between_rotors() {
    let key = [0u8; 64];

    let seed1 = derive_rotor_seed(&key, 1).unwrap();
    let seed2 = derive_rotor_seed(&key, 2).unwrap();

    assert_ne!(seed1, seed2);
}
    #[test]
fn fisher_yates_contains_all_values() {
    let rotor = fisher_yates(0);

    let mut sorted = rotor;

    sorted.sort_unstable();

    let expected: [u8; ROTOR_SIZE] =
        core::array::from_fn(|i| i as u8);

    assert_eq!(sorted, expected);
}

#[test]
fn fisher_yates_is_deterministic() {
    let rotor1 = fisher_yates(123456789);
    let rotor2 = fisher_yates(123456789);

    assert_eq!(rotor1, rotor2);
}

#[test]
fn fisher_yates_changes_with_seed() {
    let rotor1 = fisher_yates(0);
    let rotor2 = fisher_yates(1);

    assert_ne!(rotor1, rotor2);
}
#[test]
fn generate_rotor_is_deterministic() {
    let key = [0u8; COMMUNICATION_KEY_SIZE];

    let rotor1 = generate_rotor(&key, 1).unwrap();
    let rotor2 = generate_rotor(&key, 1).unwrap();

    assert_eq!(rotor1, rotor2);
}

#[test]
fn generate_rotors_creates_sixteen_rotors() {
    let key = [0u8; COMMUNICATION_KEY_SIZE];

    let rotors = generate_rotors(&key).unwrap();

    assert_eq!(rotors.len(), ROTOR_COUNT);
}

#[test]
fn generate_rotors_are_permutations() {
    let key = [0u8; COMMUNICATION_KEY_SIZE];

    let rotors = generate_rotors(&key).unwrap();

    for rotor in rotors {
        let mut sorted = rotor;

        sorted.sort_unstable();

        let expected: [u8; ROTOR_SIZE] =
            core::array::from_fn(|i| i as u8);

        assert_eq!(sorted, expected);
    }
}

#[test]
fn generate_rotors_are_different() {
    let key = [0u8; COMMUNICATION_KEY_SIZE];

    let rotors = generate_rotors(&key).unwrap();

    for i in 0..ROTOR_COUNT {
        for j in (i + 1)..ROTOR_COUNT {
            assert_ne!(rotors[i], rotors[j]);
        }
    }
}
#[test]
fn rotor_forward_inverse_round_trip_all_values_and_positions() {
    let key = [0u8; COMMUNICATION_KEY_SIZE];
    let rotor = generate_rotor(&key, 1).unwrap();

    for position in 0..=u8::MAX {
        for value in 0..=u8::MAX {
            let encrypted = rotor_forward(value, position, &rotor);
            let decrypted = rotor_inverse(encrypted, position, &rotor);

            assert_eq!(
                decrypted, value,
                "Échec pour value={value}, position={position}"
            );
        }
    }
}

#[test]
fn inverse_permutation_restores_original_values() {
    let key = [0u8; COMMUNICATION_KEY_SIZE];
    let rotor = generate_rotor(&key, 1).unwrap();
    let inverse = inverse_permutation(&rotor);

    for value in 0..=u8::MAX {
        assert_eq!(inverse[rotor[value as usize] as usize], value);
    }
}
}

