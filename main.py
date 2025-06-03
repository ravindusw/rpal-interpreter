from src.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from src.parser.parser import Parser
from src.standardizer.standardizer import Standardizer
from src.cse_machine.cse_machine import CSEMachine

def main():
    with open("./examples/sample1.txt", "r") as file:
        print("Reading source code from 'examples/sample.txt'...")
        source_code = file.read().strip()
    print("Source code read successfully.")
    print("Source Code:")
    print(source_code)

    analyzer = LexicalAnalyzer(source_code)
    tokens = analyzer.get_tokens()
    print("Tokens:")
    for token in tokens:
        print(token)
    
    parser = Parser(tokens)
    parser.parse()

    print("Parsing completed successfully.")

    standardizer = Standardizer(parser.token_stack.peek())
    standardizer.standardize()
    standardizer.print_standardized_tree()

    print("Standardization completed successfully.")

    cse_machine = CSEMachine(standardizer.standardized_tree)
    result = cse_machine.evaluate()
    print("CSE Machine evaluation result:")
    print(result)

if __name__ == "__main__":
    main()
