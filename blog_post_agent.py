from openai import OpenAI
import cmd
from dotenv import load_dotenv
from utils import *
from chapter import *
import os

load_dotenv()

client = OpenAI()

TURBO_MODEL ={ "name": "gpt-4-turbo",
               "cmd": "turbo"}
MINI_MODEL = {"name": "gpt-4-mini",
                "cmd": "mini"}

GPT_5_MODEL = {"name": "gpt-5-nano-2025-08-07",
                "cmd": "gpt5"}

models = [TURBO_MODEL, MINI_MODEL, GPT_5_MODEL]

img_example = """
    <img class="slika" src="https://www.kuhinja.net/sk/opis_slike.jpg" alt="Opis slike" />
"""

class BlogPostAgent(cmd.Cmd):
    intro = "Dobrodošli u AI generator blog postova. Unesite 'help' za popis komandi."

    def __init__(self, theme=None, chapters=[], blog_description=None, audience=None):
        super().__init__()
        self.theme = theme
        self.chapters = chapters
        self.prompt = ">> "
        self.blog_description = blog_description
        self.audience = audience

    def do_print(self):
        print(f"Tema: {self.theme}")
        print(f"Opis bloga: {self.blog_description}")
        self.do_list_chapters()
    
    def blog_prompt(self):
        chapters_str = "\n\t".join([chapter.as_string(i) for (i, chapter) in enumerate(self.chapters)])
        return f"""
            ZADATAK
            Napiši opširan HTML blog post na hrvatskom jeziku na temu {self.theme}. Možeš prilagoditi fokus teme ciljanoj publici.

            JEZIK I STIL

            Piši prirodnim hrvatskim (hr-HR), informativno i angažirano.
            Bez fraza tipa “u ovom poglavlju ćemo…”. Nikad ne obećavaj sadržaj koji ne isporučiš.
            Ne koristi riječi “poglavlje”, “tema”, “opis”, “podtema” u naslovima. Naslove piši kao u pravom blogu.
            Uključi bogat vokabular i duge, SEO-prijateljske rečenice, ali bez “keyword stuffing”-a.

            STRUKTURA HTML-a (SAMO `<body>`!)
            Ispiši isključivo element `<body>…</body>` bez `<html>`, `<head>`, `<title>`, CSS-a ili JS-a.

            Unutar `<body>` koristi semantički HTML ovim redoslijedom:

            1. <h1> – glavni naslov članka (privlačan, SEO-orijentiran).
            2. Uvodni odlomak (sažeto postavite kontekst i vrijednost za čitatelja).
            3. Opis bloga (dopunite i prilagodite publici ako postoji; inače za širu publiku) – jedan ili dva odlomka odmah ispod naslova.
            4. Ciljana publika: Cijeli blog post mora biti izričito namijenjen publici {self.audience}; prilagodite ton, razinu detalja, primjere i terminologiju toj publici. Ako {self.audience} nije zadano, pišite za širu publiku.
            5. Glavna tijela članka u sekcijama:
            - Za svaku temu iz {chapters_str} koristite <h2> za naziv sekcije (naslov možete promijeniti ako postoji prikladnija varijanta).
            - Ispod <h2> napišite opis sekcije (možete ga nadopuniti i prilagoditi publici).
            - Ako sekcija ima podpoglede, za svaki koristite <h3> i ispod njega sadržaj.
            - Svaki (pod)odjeljak mora imati najmanje 5 potpunih rečenica.
            - Dodajte dodatne sekcije ako doprinose jasnoći i potpunosti teme.
            6. Zaključak s jasnim “takeaways” (ključni savjeti / koraci).


            DULJINA
            Ciljaj minimalno 1.800 riječi (više je poželjno ako je relevantno).

            SEO ZAHTJEVI

            U tekstu prirodno koristi sinonime i long-tail fraze relevantne za {self.theme}.
            Uključi unutarnje mikro-FAQ odjeljak (2–4 česta pitanja s odgovorima po 3–5 rečenica) ako je prikladno.
            Ne izmišljaj resurse ni reference; ako ih spominješ, sadržaj zaista mora biti prisutan u članku.

            SLIKE (OBAVEZNO)

            U svakoj većoj sekciji dodaj barem jednu relevantnu sliku.
            Format slike mora biti točno kao u primjeru {img_example} – zadrži isti hostname i path, zamijeni samo opis slike temom slike.
            Za svaku sliku koristi `<figure>`, unutar nje `<img>` i `<figcaption>`.
            U `<img>` obavezno stavi `alt` i `title` atribute s deskriptivnim, SEO-prijateljskim tekstom.
            Slike moraju biti konkretno vezane uz sekciju u kojoj se nalaze.

            KVALITETA I ISTINITOST

            Ne ostavljaj prazne ili generičke odlomke; svaki mora dodati novu vrijednost.
            Ne obećavaj vodiče ili popise koje ne isporučiš. Ako nešto spomeneš, napiši.
            Izbjegavaj floskule i općenitosti – koristi praktične savjete, primjere i jasno objašnjenje “zašto” i “kako”.

            IZLAZNI FORMAT (STROGO SE DRŽI REDOSLIJEDA)

            1. Prvo ispiši kompletan HTML sadržaj isključivo u `<body>…</body>`.
            2. Nakon `</body>` ispiši tri SEO linije bez ikakvih tagova ili dodatnog markup-a, točno ovim formatom (jedna stavka po liniji):

            ```
            title - <meta title>
            description - <meta description>
            keywords - <meta keywords>
            ```

            3. Također nakon `</body>`, ispiši sljedeće blokove teksta, bez HTML tagova i bez dodatnog markup-a, redom:

            Proizvodi (prijedlozi za kupnju): navedite 5–10 relevantnih proizvoda povezanih s temom članka. Za svaki proizvod u jednoj liniji upiši:
            `Naziv: …; Kratki opis: …; Za koga/što: …`
            (bez izmišljanja brendova; opisi i namjena moraju logično proizlaziti iz članka)
            Opisi slika (za lakše nalaženje na internetu): za svaku sliku korištenu u članku, u jednoj liniji upiši opis koji precizno opisuje sadržaj slike i kontekst sekcije (npr. “noževi od nehrđajućeg čelika za precizno sjeckanje luka – priprema mirepoixa”). Počni s: `Slika 1: …`, `Slika 2: …`, redom.

            DODATNE NAPOMENE

            Ako je ciljna publika specificirana, ton i primjeri prilagodi njima; inače piši za širu publiku.
            Ako teme iz {chapters_str} nisu dovoljno sveobuhvatne, smiješ ih izmijeniti ili dodati nove da članak bude potpun.
            Ne uključuj nikakve napomene o tome da si AI ili kako generiraš sadržaj.
            Ne uključuj ništa osim traženog: `<body>…</body>`, zatim SEO linije, zatim blok s proizvodima, pa blok s opisima slika.

            ULAZNI PODACI

            Tema: {self.theme}
            Opis bloga (dopuni i prilagodi publici): {self.blog_description}
            Predložene sekcije i podpoglavlja: {chapters_str}
            Primjer formata slike: {img_example}
        """
    
    def do_generate(self, arg):
        if not self.theme or len(self.chapters) == 0:
            print("Greška: Morate prvo postaviti temu, opis i dodati barem jedno poglavlje.")
            return

        model_cmd = arg.strip() 
        if model_cmd not in [model["cmd"] for model in models]:
            print(f"Greška: Model {model_cmd} nije podržan.")
            return
        
        model = [model["name"] for model in models if model["cmd"] == model_cmd][0]

        print("Generating blog post...")
        print(f"Model: {model}")
        print("Theme: ", self.theme)
        self.do_list_chapters()
        print("\n\nFinal prompt:\n", self.blog_prompt())
        print("\n\nThis may take a few minutes.\n")

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": self.blog_prompt()},
            ],
        )
        result = completion.choices[0].message.content 

        win_file_title = win_chars(self.theme)
        folder = os.getenv("RESULTS_FOLDER") or "results"
        if not os.path.exists(folder):
            os.makedirs(folder)
        filename = f"{folder}/blog_post_{win_file_title}.html"
        
        with open(f"{filename}", "w", encoding='utf-8-sig') as f:
            f.write(f"Theme: {self.theme}\n")
            f.write(f"Description: {self.blog_description}\n")
            f.write(f"Audience: {self.audience}\n")
            for (i,chapter) in enumerate(self.chapters):
                f.write(f"{chapter.as_string(i)}\n")
            f.write(result + "\n")
            f.write(f"URL: {win_file_title}\n")

        print(f"Blog post saved to {filename}") 
        print("Done.")
    
    def do_theme(self, arg):
        if not arg.strip():
            print("Greška: Morate unijeti naziv teme.")
            return
        self.theme = arg.strip()
        print(f"Tema postavljena: {self.theme}")

    def do_description(self, arg):
        if not arg.strip():
            print("Greška: Morate unijeti opis bloga.")
            return
        self.blog_description = arg.strip()
        print(f"Opis bloga postavljen: {self.blog_description}")

    def do_chapter(self, ch_name):
        if not ch_name.strip():
            print("Greška: Morate unijeti naziv poglavlja.")
            return
        
        name = ch_name.strip()
        if any(chapter.name == name for chapter in self.chapters):
            print(f"Greška: Poglavlje '{name}' već postoji.")

        print(f"Dodana poglavlja su: {[chapter.name for chapter in self.chapters]}")

        description = input("\tUnesite opis poglavlja: ").strip() or "Dotično podpoglavlje nema opisa."  
        new_chapter = Chapter(name, description=description) # Omogućava unos pod-tema unutar poglavlja
        self.chapters.append(new_chapter)

        print([chapter.name for chapter in self.chapters])
        print(f"\nTema blog post-a: {self.theme}")
        print(f"Ciljana publika: {self.audience}")
        print(f"Opis bloga: {self.blog_description}")
        print(f"Dodano poglavlje: {new_chapter.name}")
        print(f"Opis poglavlja: {new_chapter.description}")
        print(f"Pod-teme u poglavlju '{new_chapter.name}': {new_chapter.sub_themes}")
        
        

        for (i, chapter) in enumerate(self.chapters):
            print(f"{i+1}. {chapter.name} - {chapter.description} - Pod-teme: {chapter.sub_themes}")

    def do_list_chapters(self, arg=""):
        if len(self.chapters) == 0:
            print("Trenutno nema dodanih poglavlja.")
            return
        list_chapters(self.chapters)

    def do_audience(self, arg):
        if not arg.strip():
            print("Greška: Morate unijeti ciljanu publiku.")
            return
        self.audience = arg.strip()
        print(f"Ciljana publika postavljena: {self.audience}")

    def do_exit(self, arg):
        print("Exiting the AI generator...")
        return True

def main():
    new_post = BlogPostAgent()
    new_post.cmdloop()

if __name__ == "__main__":
    main()