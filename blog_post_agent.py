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

    def __init__(self, theme=None, chapters=[], blog_description=None):
        super().__init__()
        self.theme = theme
        self.chapters = chapters
        self.prompt = ">> "
        self.blog_description = blog_description

    def do_print(self):
        print(f"Tema: {self.theme}")
        print(f"Opis bloga: {self.blog_description}")
        self.do_list_chapters()
    
    def blog_prompt(self):
        chapters_str = "\n\t".join([chapter.as_string(i) for (i, chapter) in enumerate(self.chapters)])
        return f"""
            Pišeš HTML blog post na temu {self.theme}. Temu bloga možeš slobodno prilagoditi publici. Blog post mora biti u HTML formatu (samo <body> tag), pisan na hrvatskom jeziku i što opširniji, dug za čitanje, svako podpoglavlje treba imati bar 5 rečenica, treba biti informativan i zanimljiv, treba sadržavati što više riječi koje će mu pomoći u SEO pretrazi. Nemoj reći da nešto u članku publika može pronaći ako toga nema ili napiši to što kažeš. Dakle nemoj pisati "u ovom poglavlju ćemo ..." i potom to ne napišeš. U naslovima i opisima bloga i poglavlja nemoj koristiti riječi kao što su "poglavlje", "tema", "opis", "podtema" i slično. Napiši ih kao da pišeš pravi blog post.
            Opis bloga je: {self.blog_description}, molim te da ga nadopuniš i prilagodiš publici. Napiši ga ispod naslova i prilagodi publici ako postoji. Ako nema, napiši ga kao da pišeš za širu publiku.
            Teme poglavlja sa pod poglavljima (sam odaberi moguće zamjenske naslove ako misliš da su prikladniji) su:
            {chapters_str}. Opise poglavlja također možeš nadopuniti i prilagoditi publici. Napiši ih ispod naslova poglavlja i prilagodi publici ako postoji.
            Možeš slobodno izmijeniti poglavlja ili dodati nova ako misliš da su prikladnija.
            Blog post mora sadržavati slike u formatu kao u ovome primjeru:  
                    {img_example} samo zamijeni opis slike s temom slike. Ništa drugo, isti je hostname i path. 
            Slike trebaju biti relevantne temi blog post-a i određenom poglavlju u kojem se nalaze.  
            Nakon što završiš s pisanjem blog post-a, izvad <body> tag-a napiši SEO elemente bez tagova i markup-a samo u ovom formatu:  
            title - meta title  
            description - meta description  
            keywords - meta keywords  

            te isto izvan <body> tag-a predloži proizvode koje bi čitatelji mogli kupiti na temelju teme blog post-a tenapiši sve opise slika koje si predložio u blog postu za lakše nalazenje slika na internetu.
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
        folder = os.getenv("RESULTS_FOLDER")
        filename = f"{folder}/blog_post_{win_file_title}.html"
        with open(f"{filename}", "w", encoding='utf-8-sig') as f:
            f.write(f"Theme: {self.theme}\n")
            f.write(f"Description: {self.blog_description}\n")
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

    def do_exit(self, arg):
        print("Exiting the AI generator...")
        return True

def main():
    new_post = BlogPostAgent()
    new_post.cmdloop()

if __name__ == "__main__":
    main()