from src.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from src.parser.parser import Parser

def main():
    with open("./examples/sample.txt", "r") as file:
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

if __name__ == "__main__":
    main()
