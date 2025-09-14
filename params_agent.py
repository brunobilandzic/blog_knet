from openai import OpenAI
from dotenv import load_dotenv
import  utils
import random
import parameters_prompt

load_dotenv()

client = OpenAI()

class ParametersAgent():
    def __init__(self, gen_themes=None, bp_num=utils.DEFAULT_BP_NUM):
        self.bp_num = bp_num
        self.gen_themes = gen_themes or random.sample(utils.general_parameters_themes, self.bp_num)

    def get_prompt(self):
        param_example = parameters_prompt.stringify(parameters_prompt.get_example())
        gen_themes = "\n".join(f"- {theme}" for theme in self.gen_themes)
        return parameters_prompt.prompt.format(
            bp_num=self.bp_num,
            param_example=param_example,
            gen_themes=gen_themes
        )
    
    def generate(self, filename=utils.DEFAULT_PARAMS_RES_FILENAME, model = utils.DEFAULT_MODEL):
        print("Generating parameters...")

        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": self.get_prompt()},
            ],
        )
        result = completion.choices[0].message.content

        return self.save_to_file(filename=filename, content=result)
    
    def save_to_file(self, filename=utils.DEFAULT_PARAMS_RES_FILENAME, content=None):
        if content is None:
            content = self.generate()
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Parameters saved to {filename}")
        
        return filename

