import promptgen

class TestHandler(promptgen.CallbackHandler):
    m_artist = [ "Van Gogh", "Norman Rockwell", "Alphonse Mucha", "Edward Hopper" ]
    m_medium = [ "Oil Painting", "Sculpture", "Photo", "Watercolor", "Acrylic"]
    m_test_list = [ "item-a", "item-b", "item-c", "item-d" ]
            
    def get_list(self, list_name):
        match list_name:
            case "artist":
                return self.m_artist
            case "medium":
                return self.m_medium
            case "test_list":
                return self.m_test_list
            
        return []

    def get_list_count(self, list_name):
        match list_name:
            case "artist":
                return len(self.m_artist)
            case "medium":
                return len(self.m_medium)
            case "test_list":
                return len(self.m_test_list)
            
        return 0

    
    def get_variable(self, var_name):
        match var_name:
            case "test_var_255":
                return 255
        return None


def test():
    test_prompts = {
        "basic": [
            r'iteration',
            r'update_c(pad(rndi(0,100), 3), 2)',
            r'nexta(rngi(1,5))',
            r'update_b(nexta(list("test_list")))',
            r'foreach(["a", "b", "c", "d"], 2)',
        ],
        "vars": [
            r'iteration',
            r'update_c(save_var("sv-test", pad(rndi(0,100), 3)), 2)',
            r'var("sv-test")',
            r'var("test_var_255")'
        ],
        "math": [
            r'1 + 1',
            r'3 - 4',
            r'10 / 5',
            r'2 * 2',
            r'iteration % 5'
        ]
    }
        
    for test_name in test_prompts.keys():
        template = ''
        print(f"Running {test_name}")
        for c in test_prompts[test_name]:
            template += f'{c}: ' + "{{" + c + "}}; "
   
        prompts = promptgen.generate_prompts(template, batch_count=3, batch_size=4, callback_handler=TestHandler())
        for i in range(0, len(prompts)):
            print(f"{str(i):>04}: {prompts[i]}")

if __name__ == "__main__":
    test()