def number_to_letter(i):
    return chr(97 + i)


def win_chars(text):
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
        'Ž': 'Z',
        "/": "_",
        " ": "_",
        "<": "_",
        ">": "_",
        ":": "_",
        "\\": "_",
        "|": "_",
        "?": "_",
        "*": "_"
    }
    for char, win_char in replacements.items():
        text = text.replace(char, win_char)

        while "__" in text:
            text = text.replace("__", "_")
    return text.lower()


print(win_chars("Kuhinja: putovanje kroz osnove kuhanja i svjetske okuse"))



