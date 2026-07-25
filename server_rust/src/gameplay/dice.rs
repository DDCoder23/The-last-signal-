use rand::Rng;

pub fn jet_de_des(face: u32, nb: u32) -> u32 {
    let mut rng = rand::thread_rng();

    (0..nb)
        .map(|_| rng.gen_range(1..=face))
        .sum()
}
