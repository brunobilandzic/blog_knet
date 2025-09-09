from openai import OpenAI
import cmd
from dotenv import load_dotenv
from utils import *
from chapter import *

load_dotenv()

client = OpenAI(

    
)

TURBO_MODEL ={ "name": "gpt-4-turbo",
               "cmd": "turbo"}
MINI_MODEL = {"name": "gpt-4-mini",
                "cmd": "mini"}

SEO_SEGMENTS = ["meta title", "meta description", "meta keywords"]

models = [TURBO_MODEL, MINI_MODEL]


img_example = """
    <img class="slika" src="https://www.kuhinja.net/sk/opis_slike.jpg" alt="Opis slike" />
"""



class BlogPost(cmd.Cmd):
    intro = "Dobrodošli u AI generator blog postova. Unesite 'help' za popis komandi."
    

    def __init__(self, theme=None, chapters=[], blog_description=None):
        super().__init__()
        self.theme = theme
        self.chapters = chapters
        self.prompt = ">> "
        self.blog_description = blog_description
    
    def blog_prompt(self):
        chapters_str = "\n\t".join([chapter.as_string(i) for (i, chapter) in enumerate(self.chapters)])
        return f"""
            Pišeš HTML blog post na temu {self.theme}. Temu bloga možeš slobodno prilagoditi publici. Blog post mora biti u HTML formatu (samo <body> tag), pisan na hrvatskom jeziku. Opis bloga: {self.blog_description}, molim te da ga nadopuniš i prilagodiš publici. Napiši ga ispod naslova i prilagodi publici ako postoji. Ako nema, napiši ga kao da pišeš za širu publiku.
            Teme poglavlja sa pod poglavljima (sam odaberi moguće zamjenske naslove ako misliš da su prikladniji) su:
            {chapters_str}. Opise poglavlja također možeš nadopuniti i prilagoditi publici. Napiši ih ispod naslova poglavlja i prilagodi publici ako postoji.

            Možeš slobodno izmijeniti poglavlja ili dodati nova ako misliš da su prikladnija.
            Blog post mora sadržavati slike u formatu kao u ovome primjeru:  
                    {img_example} samo zamijeni opis slike s temom slike. Ništa drugo, isti je hostname i path. 

            Slike trebaju biti relevantne temi blog post-a i određenom poglavlju u kojem se nalaze.  

            Nakon što završiš s pisanjem blog post-a, napiši SEO elemente bez tagova i markup-a samo u ovom formatu:  
            title - meta title  
            description - meta description  
            keywords - meta keywords  
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

        filename = replace_cro_letters(f"html_results/blog_post_{self.theme.replace(" ", "_").lower()}.html")
        with open(f"{filename}", "w", encoding='utf-8-sig') as f:
            f.write(f"Theme: {self.theme}\n")
            f.write(f"Description: {self.blog_description}\n")
            for (i,chapter) in enumerate(self.chapters):
                f.write(f"{chapter.as_string(i)}\n")
            f.write(result + "\n")

        print(f"Blog post saved to {filename}") 

     
    
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
    


    # def prompt_blog_post_and_seo(self):
    #     return f"""
    #         Tema blog post-a je {self.theme}. Poglavlja blog post-a su {self.chapters}. Možeš slobodno izmijeniti poglavlja ili dodati nova. Blog post mora sadržavati slike u formatu kao u ovome primjeru: {self.img_example}. Slike trebaju biti relevantne temi blog post-a i određenom poglavlju u kojem se nalaze.

    #         Također, napiši prijedlog za SEO elemente:
    #         - Meta title: Mora sadržavati ključne riječi koje korisnici pretražuju na Google.
    #         - Meta description: Kratki opis koji privlači korisnike i sadrži ključne riječi.
    #         - Keywords: Popis ključnih riječi relevantnih za temu blog post-a.
    #         """


# blog_posts = [
#     BlogPost("Češnjak", ["Povijest", "Okus češnjaka", "Kako ga koristiti", "Kako odabrati najbolji češnjak", "Recepti s češnjakom"]),
#     BlogPost("San", ["Zašto ljudi spavaju", "Kako san utječe na zdravlje", "Kako poboljšati san", "San i prehrana"]),
#     BlogPost("Kava", ["Povijest kave", "Kako se pravi kava", "Industrija kave", "Kako odabrati najbolju kavu", "Kava i zdravlje"]),
#     BlogPost("Čokolada", ["Povijest čokolade", "Kako se pravi čokolada", "Vrste čokolade", "Čokolada i zdravlje"]),
#     BlogPost("Jagode", ["Zanimljivosti o jagodama", "Zdrastveni benefiti" "Kako odabrati najbolje jagode", "Recepti s jagodama"]),    
# ]


# cesnjak = BlogPost("Češnjak", ["Povijest", "Zdravlje", "Okus", "Savjeti"])


def main():
    new_post = BlogPost()
    new_post.cmdloop()

if __name__ == "__main__":
    main()