from src.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from src.parser.parser import Parser
from src.standardizer.standardizer import Standardizer
from src.cse_machine.cse_machine import CSEMachine

def main():
    
    try:
        # Source Code Reading
        with open("./examples/sample26.txt", "r") as file:
            print("--------------------------------------------------")
            print("\nReading source code from 'examples/sample.txt'...")
            source_code = file.read().strip()
        print("Source code read successfully.")
        # print("Source Code:-")   
        # print(source_code)

        # Lexical Analysis
        print("--------------------------------------------------")
        print("\nStarting Lexical Analysis...")
        analyzer = LexicalAnalyzer(source_code)
        tokens = analyzer.tokenize()
        print("Lexical Analysis completed successfully.")
        
        # Parsing
        print("--------------------------------------------------")
        print("\nStarting Parsing...")
        parser = Parser(tokens)
        ast = parser.parse()
        # parser.print_abstract_syntax_tree()
        print("Parsing completed successfully.")

        # Standardizing
        print("--------------------------------------------------")
        print("\nStarting Standardization...")
        standardizer = Standardizer(ast)
        st = standardizer.standardize()
        # standardizer.print_standardized_tree()

        print("Standardization completed successfully.")

        # Evaluation
        print("--------------------------------------------------")
        print("\nStarting CSE Machine...")
        cse_machine = CSEMachine(st)
        result = cse_machine.evaluate()
        print("CSE Machine evaluation completed successfully.")

        print("--------------------------------------------------")

        print("\nFinal output Of RPAL program:", result)
        print()
    
    except Exception as e:
        print(f"Error: {e}")
        print("An error occurred during the RPAL interpreter pipeline execution.")
        print("Please check the source code and try again.")

if __name__ == "__main__":
    main()
