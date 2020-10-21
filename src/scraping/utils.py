from cyrtranslit import to_latin


def from_cyrrilic_to_eng(text: str):
    # trasnliterate cyrillic to english for slug
    text = to_latin(text)
    return text.replace(' ', '_').lower()