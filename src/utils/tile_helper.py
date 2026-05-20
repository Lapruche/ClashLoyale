TILE_SIZE = 55


def pixel_to_tile(amount) -> int:
    return amount // TILE_SIZE


def tile_to_pixel(amount) -> int:
    return amount * TILE_SIZE
