def generate_map(
    size=128,
    style="island",        # "island", "mountains", "dungeon"
    height_scale=1.0,
    seed=None,
    output_prefix="map"
):
    """
    Génère :
    - map_height.png     (relief)
    - map_color.png      (texture)
    - map_collision.png  (collisions)
    """

    import numpy as np
    from PIL import Image, ImageDraw

    if seed is not None:
        np.random.seed(seed)

    # ======================
    # BASE HEIGHTMAP
    # ======================
    x, y = np.meshgrid(
        np.linspace(-1, 1, size),
        np.linspace(-1, 1, size)
    )

    noise = np.random.rand(size, size) * 0.2

    if style == "island":
        dist = np.sqrt(x**2 + y**2)
        height = 1 - dist
        height = np.clip(height, 0, 1)

    elif style == "mountains":
        height = np.sin(5 * x) * np.cos(5 * y)
        height = (height - height.min()) / (height.max() - height.min())

    elif style == "dungeon":
        height = np.zeros((size, size))

        # salles
        for _ in range(10):
            cx, cy = np.random.randint(10, size-10, 2)
            w, h = np.random.randint(5, 15, 2)
            height[cy-h:cy+h, cx-w:cx+w] = 0.4

    else:
        raise ValueError("Style inconnu")

    height = np.clip(height + noise, 0, 1)
    height *= height_scale

    # ======================
    # HEIGHTMAP IMAGE
    # ======================
    height_img = Image.fromarray((height * 255).astype(np.uint8))
    height_img.save(f"{output_prefix}_height.png")

    # ======================
    # TEXTURE COULEUR
    # ======================
    color = np.zeros((size, size, 3), dtype=np.uint8)

    for y0 in range(size):
        for x0 in range(size):
            h = height[y0, x0]
            if h < 0.2:
                color[y0, x0] = (20, 50, 150)     # eau
            elif h < 0.4:
                color[y0, x0] = (50, 120, 50)    # plaine
            elif h < 0.7:
                color[y0, x0] = (100, 100, 100)  # roche
            else:
                color[y0, x0] = (240, 240, 240)  # neige

    Image.fromarray(color).save(f"{output_prefix}_color.png")

    # ======================
    # COLLISION MAP
    # ======================
    collision = np.zeros((size, size), dtype=np.uint8)

    # Eau + sommets = collision
    collision[height < 0.2] = 255
    collision[height > 0.85] = 255

    Image.fromarray(collision).save(f"{output_prefix}_collision.png")

    print("✅ Map générée :")
    print(f" - {output_prefix}_height.png")
    print(f" - {output_prefix}_color.png")
    print(f" - {output_prefix}_collision.png")