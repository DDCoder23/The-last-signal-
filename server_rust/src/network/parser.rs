pub fn parse_login_payload(
    payload: &[u8],
) -> Result<(String, String), String> {

    let mut offset = 0;

    // -------------------------
    // Email length
    // -------------------------

    if payload.len() < offset + 2 {
        return Err("Email length manquante".into());
    }

    let email_length =
        u16::from_be_bytes([
            payload[offset],
            payload[offset + 1],
        ]) as usize;

    offset += 2;

    // -------------------------
    // Email
    // -------------------------

    if payload.len() < offset + email_length {
        return Err("Email incomplet".into());
    }

    let email = String::from_utf8(
        payload[offset..offset + email_length]
            .to_vec()
    )
    .map_err(|_| "Email UTF-8 invalide")?;

    offset += email_length;

    // -------------------------
    // Password length
    // -------------------------

    if payload.len() < offset + 2 {
        return Err("Password length manquante".into());
    }

    let password_length =
        u16::from_be_bytes([
            payload[offset],
            payload[offset + 1],
        ]) as usize;

    offset += 2;

    // -------------------------
    // Password
    // -------------------------

    if payload.len() < offset + password_length {
        return Err("Password incomplet".into());
    }

    let password = String::from_utf8(
        payload[offset..offset + password_length]
            .to_vec()
    )
    .map_err(|_| "Password UTF-8 invalide")?;

    Ok((email, password))
}
