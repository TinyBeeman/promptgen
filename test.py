import promptgen
import argparse
import difflib
import json
import unittest


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

def combine_strings(prompts):
    return "\n".join(prompts)


def basic_tests(debug=False, output_tests=False):
    with open('test.json') as test_file:
        file_contents = test_file.read()
    
    test_prompts = json.loads(file_contents)

    handler = TestHandler()
    errors = ""
    for test_name in test_prompts.keys():
        test = test_prompts[test_name]
        template = ''
        print(f"Running {test_name}")
        for c in test["spans"]:
            template += f'{c}: ' + "{{" + c + "}}; "
        if (debug):
            print(promptgen.debug_template(template, callback_handler=handler))
        else:
            prompts = promptgen.generate_prompts(template, batch_count=test["batch_count"], batch_size=test["batch_size"], callback_handler=handler)
            actual = combine_strings(prompts)
            if (output_tests):
                test_prompts[test_name]["expected"] = actual
            else:
                # print(actual)
                # print("DIFF")
                expected = test["expected"]
                if (expected == actual):
                    print(f"{test_name} test succeeded.")
                else:
                    print(f"{test_name} failed:")
                    d = difflib.Differ()
                    diffs = list(difflib.unified_diff(actual.splitlines(keepends=True), test["expected"].splitlines(keepends=True)))
                    dstr = '\n'.join(diffs) # "!" + diffs[0] + "!" #''.join(d.compare(actual, test["expected"]))
                    print(dstr)
                
    if (output_tests):
        with open('test_output.json', 'w') as out_file:
            json.dump(test_prompts, out_file, indent=4)
        print("test_output.json written to disk.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", help="debug the test prompts", action="store_true")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument("-st", "--save_tests", help="Outputs the contents of the basic tests with expected results.", action="store_true")
    parser.add_argument("-t", "--template", type=str, help="test a custom template")
    parser.add_argument("-bs", "--batch_size", type=int, default = 1, help="Provide a custom batch_size when using -t")
    parser.add_argument("-bc", "--batch_count", type=int, default = 1, help="Provide a custom batch_count when using -t")
    args = parser.parse_args()
    debug = True if args.debug else False
    if (args.save_tests):
        basic_tests(debug=False, output_tests=True)
    elif (args.template):
        if (debug):
            print(promptgen.debug_template(args.template))
        else:
            print(combine_strings(promptgen.generate_prompts(args.template, args.batch_count, args.batch_size)))
    else:
        basic_tests(debug)