import json
import random

DEFAULT_BP_NUM = 2
DEFAULT_CH_NUM = 5
DEFAULT_AUDIENCE = "Osobe koje naručuju kuhinjsku opremu online"

general_parameters_themes = [
    "Kuhinjski pribor i oprema / Ljubitelji kuhanja, domaćice, amateri kuhari",
    "Zdravlje i prehrana / Osobe koje brinu o zdravlju, nutricionisti, sportaši",
    "Recepti i kuhanje / Početnici u kuhanju, iskusni kuhari, studenti",
    "Ekologija i održivost u kuhinji / Ekološki osviješteni pojedinci, obitelji",
    "Psihologija prehrane / Psiholozi, roditelji, osobe koje žele promijeniti prehrambene navike",
    "Sigurnost hrane / Roditelji, ugostitelji, zdravstveni radnici",
    "Organizacija kuhinje / Zaposleni ljudi, male obitelji, studenti",
    "Trendovi u kulinarstvu / Mladi, food blogeri, kulinarski entuzijasti",
    "Domaća izrada i DIY kuhinjski projekti / Kreativci, hobisti, obitelji s djecom",
    "Utjecaj prehrane na zdravlje / Osobe s kroničnim bolestima, starije osobe",
    "Sezonske namirnice / Ljubitelji lokalne hrane, vrtlari, kuhari",
    "Nutricionizam / Nutricionisti, sportaši, roditelji",
    "Zero waste kuhanje / Ekološki aktivisti, mlade obitelji, studenti",
    "Kultura i povijest hrane / Ljubitelji povijesti, putnici, studenti gastronomije",
    "Savjeti za uštedu vremena u kuhinji / Zaposleni ljudi, roditelji, studenti",
    "Tehnologija u kuhinji / Tehno entuzijasti, mladi, profesionalni kuhari",
    "Savjeti za kupovinu namirnica / Obitelji, studenti, osobe s ograničenim budžetom",
    "Vegetarijanska i veganska prehrana / Vegetarijanci, vegani, osobe s posebnim prehrambenim navikama",
    "Prehrana za posebne potrebe / Osobe s alergijama, dijabetičari, sportaši",
    "Dječja prehrana / Roditelji, odgajatelji, pedijatri"
]
DEFAULT_PARAMS_RES_FILENAME = "generated_parameters.json"
DEFAULT_THEMES = random.sample(general_parameters_themes, DEFAULT_BP_NUM)

TURBO_MODEL ={ "name": "gpt-4-turbo",
               "cmd": "turbo"}
MINI_MODEL = {"name": "gpt-4-mini",
                "cmd": "mini"}
GPT_5_MODEL = {"name": "gpt-5-nano-2025-08-07",
                "cmd": "gpt5"}

DEFAULT_MODEL = GPT_5_MODEL["name"]

models = [TURBO_MODEL, MINI_MODEL, GPT_5_MODEL]

img_example = """
    <img class="slika" src="https://www.kuhinja.net/sk/opis_slike.jpg" alt="Opis slike" />
"""

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

def load_parameters(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        parameters = json.load(file)
    return parameters




def print_themes(themes):
    print("Chosen themes:")
    for theme in themes:
        print(f"- {theme}")