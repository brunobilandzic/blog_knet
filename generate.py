from blog_post_agent import *
from chapter import *

chapters = [Chapter("", sub_themes=[""], description="")]

bg = BlogPost(theme="", blog_description="", chapters=chapters)

bg.do_generate(TURBO_MODEL["cmd"])