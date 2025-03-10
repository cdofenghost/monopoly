def hex_to_rgb(hex_rgb: str) -> tuple[int, int, int]:
    length = len(hex_rgb)

    if "#" in hex_rgb and length != 7 or "#" not in hex_rgb and length != 6:
        raise Exception(f"{hex_rgb} consists of {length} chars out of 7 needed (template: #XXXXXX). Check the value and try again.")
    
    first = 1 if length == 7 else 0

    r = int(hex_rgb[first:2+first], 16)
    g = int(hex_rgb[2+first:4+first], 16)
    b = int(hex_rgb[4+first:6+first], 16)

    return (r, g, b)
