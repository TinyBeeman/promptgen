import promptgen
import argparse

g_test_prompts = {
    "basic":
    {
        "batch_count": 3,
        "batch_size": 4,
        "spans": [
        r'iteration',
        r'update_c(pad(rndi(0,100), 3), 2)',
        r'nexta(rngi(1,5))',
        r'update_b(nexta(list("test_list")))',
        r'foreach(["a", "b", "c", "d"], 2)'
        ],
    },
    "vars": {
        "batch_count": 2,
        "batch_size": 4,
        "spans": [
            r'iteration',
            r'update_c(save_var("sv-test", pad(rndi(0,100), 3)), 2)',
            r'var("sv-test")',
            r'var("test_var_255")'
        ]
    },
    "math": {
        "batch_size": 1,
        "batch_count": 1,
        "spans":
            [
            r'1 + 1',
            r'3 - 4',
            r'10 / 2',
            r'2 * 2',
            r'13 % 5'
            ]
    },
    "precedence": {
        "batch_size": 1,
        "batch_count": 1,
        "spans": [
            r'10 / 2 + 3',
            r'3 + 10 / 2',
            r'(10 / 2) + 3',
            r'10 / (2 + 3)',
            r'10 / -(2 + 3)'
        ]
    }
}


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

def print_prompts(prompts):
    for i in range(0, len(prompts)):
        print(f"{str(i):>04}: {prompts[i]}")

def basic_tests(debug=False):
    handler = TestHandler()       
    for test_name in g_test_prompts.keys():
        test = g_test_prompts[test_name]
        template = ''
        print(f"Running {test_name}")
        for c in test["spans"]:
            template += f'{c}: ' + "{{" + c + "}}; "
        if (debug):
            print(promptgen.debug_template(template, callback_handler=handler))
        else:
            prompts = promptgen.generate_prompts(template, batch_count=test["batch_count"], batch_size=test["batch_size"], callback_handler=handler)
            print_prompts(prompts)
            

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="debug the test prompts", action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-t", "--template", type=str, help="test a custom template")
    parser.add_argument("-bs", "--batch_size", type=int, default = 1, help="Provide a custom batch_size when using -t")
    parser.add_argument("-bc", "--batch_count", type=int, default = 1, help="Provide a custom batch_count when using -t")
    args = parser.parse_args()
    debug = True if args.debug else False
    if (args.template):
        if (debug):
            print(promptgen.debug_template(args.template))
        else:
            print_prompts(promptgen.generate_prompts(args.template, args.batch_count, args.batch_size))
    else:
        basic_tests(debug)