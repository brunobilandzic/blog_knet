import json

def get_example():
    with open('parameters.json', 'r') as f:
        data = json.load(f)
    return data

def stringify(obj):
    return json.dumps(obj, indent=4, ensure_ascii=False)


prompt = """
        Ignoriraj sve prethodne upute. Ti si stručnjak za generiranje parametara za blog postove.
        tvoj zadatak je generirati JSON objekt koji sadrži parametre za generiranje {bp_num} blog postova.
        Ovo je primjer JSON objekta koji trebaš generirati: {param_example}
        Teme i publika su u formatu: tema / publika i imaju sljedeće vrijednosti:
        {gen_themes}
        Moraš vratiti samo JSON objekt, bez dodatnog teksta ili objašnjenja, tako da se moze spremiti u .json datoteku.
    """
