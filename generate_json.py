from blog_post_agent import *
from chapter import *
import json
import sys

def get_parameters_filename():
    filename = sys.argv[1] 
    if not filename:
        return None
    return f"{filename}.json"

def load_parameters(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        parameters = json.load(file)
    return parameters

def get_blog_posts(parameters):
    blog_posts = []

    for blog_post_params in parameters["blog_posts"]:
        print()
        print(f"Tema blog posta: {blog_post_params['theme']}")
        print(f"Opis blog posta: {blog_post_params['blog_description']}")
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
            blog_description=blog_post_params["blog_description"]
        )
        blog_posts.append(blog_post)

    return blog_posts


def generate_blog_posts():
    parameters = load_parameters(get_parameters_filename())
    blog_posts = get_blog_posts(parameters)
    for blog_post in blog_posts:
        blog_post.do_generate(GPT_5_MODEL["cmd"])


def main():
    generate_blog_posts()

if __name__ == "__main__":
    main()