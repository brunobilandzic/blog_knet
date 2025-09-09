def number_to_letter(i):
    return chr(97 + i)


def replace_cro_letters(text):
    replacements = {
        'č': 'c',
        'ć': 'c',
        'đ': 'dj',
        'š': 's',
        'ž': 'z',
        'Č': 'C',
        'Ć': 'C',
        'Đ': 'Dj',
        'Š': 'S',
        'Ž': 'Z'
    }
    for cro_char, eng_char in replacements.items():
        text = text.replace(cro_char, eng_char)
    return text