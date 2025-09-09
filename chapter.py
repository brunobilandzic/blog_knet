from utils import number_to_letter

class Chapter():
    def __init__(self, name, sub_themes=[], description=None):
        print("Inicijalizacija poglavlja...")
        print(f"Primljeni naziv poglavlja: {name}")
        print(f"Primljeni opis poglavlja: {description}")
        print(f"Primljene pod-teme: {sub_themes}")
        self.name = name
        if len(sub_themes) > 0:
            self.sub_themes = sub_themes
        else:
            self.sub_themes = []
        self.sub_num = 0
        self.description = description 

        

        print(f"sub teme: {self.sub_themes}") 

        if len(sub_themes) > 0:
            return
        
        self.prompt = f"Unesite podtemu {number_to_letter(self.sub_num)}: "
        while True:
            self.prompt = f"\nUnesite pod-temu {number_to_letter(self.sub_num)} za poglavlje '{self.name}' (ili 'exit' za izlaz):"
            sub_theme = input(self.prompt).strip()

            if not sub_theme.strip():
                print("Greška: Morate unijeti naziv pod-teme.")
                continue
            
            if sub_theme.lower() == "exit":
                print("Izlaz iz poglavlja...")
                break

            self.add_sub_theme(sub_theme)


    def add_sub_theme(self, arg):
        """Dodajte pod-temu (primjer: sub_theme Povijest)"""
        
        if not arg.strip():
            print("Greška: Morate unijeti naziv pod-teme.")
            return
        if arg.strip() in self.sub_themes:
            print(f"Greška: Pod-tema '{arg.strip()}' već postoji u poglavlju '{self.name}'.")
            return
        
        self.sub_themes.append(arg.strip())
        print(f"Dodana pod-tema: {arg.strip()} u poglavlje '{self.name}'")
        print(f"Trenutne pod-teme u poglavlju '{self.name}': {self.sub_themes}")
        # Povećaj brojač pod-tema
        self.sub_num += 1
        

    
    def __str__(self):
        return f"Chapter(name={self.name}, sub_themes={self.sub_themes})"
    
    def as_string(self, i=0):
        return f"Poglavlje {self.name}, Opis poglavlja {self.name}: {self.description}, Pod-teme poglavlja {self.name}: {self.sub_themes}"
    
def list_chapters( chapters=[]):
    if not chapters:
        print("Trenutno nema dodanih poglavlja.")
        return
    print("All chapters:")
    for chapter in chapters:
        print(f"\t{chapter.as_string(chapters.index(chapter))}")