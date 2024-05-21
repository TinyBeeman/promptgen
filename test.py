import promptgen

def test():
    template = r'A {{foreach(list("artist"))}} by {{foreach(["a","b"])}}, {{iteration}}/{{prompt_count}}.'
    prompts = promptgen.generate_prompts(template, 3, 4)
    for i in range(0, len(prompts)):
        print(f"{str(i):>04}: {prompts[i]}")

if __name__ == "__main__":
    test()