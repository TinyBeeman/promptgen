import promptgen

def test():
    template = r'Iter {{iteration}}, update_c(rndi(10,20),2): {{update_c(rndi(10,20),2)}}, nexta: {{nexta(["  one","  two","three"])}}, update_b: {{update_b(nexta(["  one","  two","three"]))}}, foreach(repeat twice): {{foreach(["a", "b", "c", "d"], 2)}}'
    prompts = promptgen.generate_prompts(template, 3, 4)
    for i in range(0, len(prompts)):
        print(f"{str(i):>04}: {prompts[i]}")

if __name__ == "__main__":
    test()