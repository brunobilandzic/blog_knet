from agent import *
from chapter import *
import sys

DEFAULT_PARAMETERS_FILE = "custom_parameters.json"

def get_parameters_filename():
    filename = sys.argv[1] 
    if not filename:
        return DEFAULT_PARAMETERS_FILE
    return f"{filename}.json"




def generate_blog_posts():
    parameters = utils.load_parameters(get_parameters_filename())
    blog_posts = get_blog_posts(parameters)
    for blog_post in blog_posts:
        blog_post.do_generate(GPT_5_MODEL["cmd"])


def main():
    utils.generate_blog_posts()

if __name__ == "__main__":
    main()