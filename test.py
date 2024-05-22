import promptgen

def test():
    test_chunks = [
        r'iteration',
        r'update_c(pad(rndi(0,100), 3),2)',
        r'nexta(rngi(1,5))',
        r'update_b(nexta(["a","b","c"]))',
        r'foreach(["a", "b", "c", "d"], 2)'
    ]
    template = ''
    for c in test_chunks:
        template += f'{c}: ' + "{{" + c + "}}; "
    prompts = promptgen.generate_prompts(template, 3, 4)
    for i in range(0, len(prompts)):
        print(f"{str(i):>04}: {prompts[i]}")

if __name__ == "__main__":
    test()