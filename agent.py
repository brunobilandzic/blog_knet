from openai import OpenAI
import params_agent 
import cmd
from dotenv import load_dotenv
import utils
from chapter import *
import os
import argparse
import blog_prompt
import random

load_dotenv()

client = OpenAI()

def get_blog_posts(parameters):
    blog_posts = []

    for blog_post_params in parameters["blog_posts"]:
        print()
        print(f"Tema blog posta: {blog_post_params['theme']}")
        print(f"Opis blog posta: {blog_post_params['blog_description']}")
        print(f"Blog post je namijenjen za: {blog_post_params["audience"]}")
        print("Poglavlja:")
        print("\n".join(
            f"- {ch['name']} | {ch['description']} | sub_themes: {', '.join(ch['sub_themes'])}"
            for ch in blog_post_params["chapters"]
        ))
        
        chapter_list = []
        for chapter_params in blog_post_params["chapters"]:
            chapter = Chapter(
                name=chapter_params["name"],
                description=chapter_params["description"],
                sub_themes=chapter_params["sub_themes"]
            )
            chapter_list.append(chapter)
        
        blog_post = BlogPostAgent(
            theme=blog_post_params["theme"],
            chapters=chapter_list,
            blog_description=blog_post_params["blog_description"],
            audience=blog_post_params["audience"]
        )
        blog_posts.append(blog_post)

    return blog_posts

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
        return blog_prompt.prompt.format(self=self, chapters_str=chapters_str, img_example=utils.img_example)

    def do_generate(self, arg):
        if not self.theme or len(self.chapters) == 0:
            print("Greška: Morate prvo postaviti temu, opis i dodati barem jedno poglavlje.")
            return

        model_cmd = arg.strip() 
        if model_cmd not in [model["cmd"] for model in utils.models]:
            print(f"Greška: Model {model_cmd} nije podržan.")
            return
        
        model = [model["name"] for model in utils.models if model["cmd"] == model_cmd][0]

        print("Generating blog post...")
        print(f"Model: {model}")
        print("Theme: ", self.theme)
        self.do_list_chapters()
        print("\n\nThis may take a few minutes.\n")
        
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": self.blog_prompt()},
            ],
        )
        result = completion.choices[0].message.content 

        win_file_title = utils.win_chars(self.theme)
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
    print("Welcome to the AI Blog Post Generator!\n")

    parser = argparse.ArgumentParser(description="Parsiranje argumenata komandne linije.")

    parser.add_argument('-f', '--file', help="Naziv JSON datoteke s parametrima")
    parser.add_argument('-g', '--generate', action='store_true', help="Generiraj nove parametre")
    parser.add_argument('-n', '--bp_num', type=int,  help="Broj blog postova za generiranje")
    parser.add_argument('-t', '--themes', help="Tema blog postova") # može biti više tema odvojene zarezom
    parser.add_argument('-a', '--audience', help="Ciljana publika")
    parser.add_argument('-d', '--default',action='store_true', help="Generiraj s default parametrima")

    args = parser.parse_args()

    
    if args.default:
        if not args.bp_num or args.bp_num <= 0:
            bp_num = int(input(f"Unesite broj blog postova za generiranje (default {utils.DEFAULT_BP_NUM}): ")) or utils.DEFAULT_BP_NUM
        generate_params_blogs(bp_num=bp_num)

    if args.file:
        generate_blog_posts_from_file(args.file)
    
    if args.generate:
        filename = input("Unesite naziv JSON datoteke za spremanje parametara (bez ekstenzije .json): ").strip() 
        gen_themes = []
        if filename:
            filename =f"{filename}.json"
        else:
            filename = utils.DEFAULT_PARAMS_RES_FILENAME

        bp_num = args.bp_num
        if not bp_num or bp_num <= 0:
            bp_num = int(input(f"Unesite broj blog postova za generiranje (default {utils.DEFAULT_BP_NUM}): ") or utils.DEFAULT_BP_NUM)

        get_themes = input("Da li želite unijeti teme za generiranje? (y/n): ").strip().lower()

        if get_themes == 'y':
            i = 0
            while True:
                theme = input(f"Unesite temu {i+1} (ili pritisnite Enter za kraj unosa): ").strip() 
                if not theme:
                    gen_themes[len(gen_themes):] = random.sample(utils.general_parameters_themes, bp_num - len(gen_themes))
                    break
                audience = input(f"Unesite ciljanu publiku za temu {i+1} (default: {utils.DEFAULT_AUDIENCE}): ").strip() or utils.DEFAULT_AUDIENCE
                theme = f"{theme} / {audience}"
                gen_themes.append(theme)
                i += 1
                if i >= bp_num:
                    break
        else:
            gen_themes = random.sample(utils.general_parameters_themes, bp_num)

        utils.print_themes(gen_themes)   
        agent = generate_params_blogs(filename, gen_themes)

    return
    gen_parameters = input("Do you want to generate parameters? (y/n): ").strip().lower()

    if gen_parameters=='y':
        gen_themes = None
        audience = None
        bp_num = None

        while True:
            gen_themes = input("""Unesite generalnu tamu svih parametara novih blog postova
                                Ukoliko ne želite zadati temu, pritisnite Enter:
                            """).strip(',')
            if not gen_themes:
                gen_themes = 2
            gen_themes = [theme.strip() for theme in gen_themes]
            if not gen_themes:
                continue


            audience = input("""Unesite ciljanu publiku (npr. početnici, profesionalci, šira publika):
                                Ukoliko ne želite zadati publiku, pritisnite Enter:
                            """).strip()
            bp_num = input("Unesite broj blog postova za generiranje (default 1): ").strip()
            try:
                bp_num = int(bp_num)
            except ValueError:
                bp_num = 1

                agent = params_agent.ParametersAgent(gen_theme=utils.gen_theme, audience=audience, bp_num=bp_num)

    else:
        theme = input("Unesite temu blog posta: ").strip()
        audience = input("Unesite ciljanu publiku (npr. početnici, profesionalci, šira publika): ").strip()
        blog_description = input("Unesite opis blog posta: ").strip()            
        agent = BlogPostAgent(theme=theme, audience=audience, blog_description=blog_description)
        agent.cmdloop()

def generate_params_blogs(filename=None, gen_themes=None, bp_num=utils.DEFAULT_BP_NUM):
    if not filename:
        filename = utils.DEFAULT_PARAMS_RES_FILENAME

    if not gen_themes or len(gen_themes) == 0:
        gen_themes = random.sample(utils.general_parameters_themes, bp_num)

    utils.print_themes(gen_themes)

    agent = params_agent.ParametersAgent(gen_themes=gen_themes, bp_num=bp_num)
    agent.generate(filename=filename)
        
    generate_blog_posts_from_file(filename)

    return agent
    
def generate_blog_posts_from_file(filename):
    params = utils.load_parameters(filename)
    if not params:
        print(f"Greška: Ne mogu učitati parametre iz datoteke {filename}.")
        return
    blog_posts = get_blog_posts(params)
    for blog_post in blog_posts:
        blog_post.do_generate(utils.GPT_5_MODEL["cmd"])
    return

if __name__ == "__main__":
    main()