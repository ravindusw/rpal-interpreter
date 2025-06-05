import sys
import argparse
import os
from src.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from src.parser.parser import Parser
from src.standardizer.standardizer import Standardizer
from src.cse_machine.cse_machine import CSEMachine

def print_ast_only(filename):
    """
    Parse the program and print only the AST without any other output.
    """
    try:
        with open(filename, 'r') as file:
            source_code = file.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)
    
    try:
        # Lexical Analysis (silent)
        analyzer = LexicalAnalyzer(source_code)
        tokens = analyzer.tokenize()
        
        # Parsing (silent)
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Print only the AST
        if ast:
            print_tree_clean(ast)
        else:
            print("Error: No AST generated")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def print_st_only(filename):
    """
    Parse and standardize the program, then print only the standardized tree.
    """
    try:
        with open(filename, 'r') as file:
            source_code = file.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)
    
    try:
        # Lexical Analysis (silent)
        analyzer = LexicalAnalyzer(source_code)
        tokens = analyzer.tokenize()
        
        # Parsing (silent)
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Standardization (silent)
        standardizer = Standardizer(ast)
        st = standardizer.standardize()
        
        # Print only the standardized tree
        if st:
            print_tree_clean(st)
        else:
            print("Error: No standardized tree generated")
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def print_tree_clean(node, dots=""):
    """
    Print the AST in the required format (dot notation).
    """
    if node is None:
        return
    
    print(f"{dots}{node.value}")
    
    # Print left child (first child in the tree)
    if node.left:
        print_tree_clean(node.left, dots + ".")
    
    # Print right sibling
    if node.right:
        print_tree_clean(node.right, dots)

def run_full_interpreter(filename):
    """
    Run the complete RPAL interpreter pipeline.
    """
    try:
        with open(filename, 'r') as file:
            source_code = file.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading file '{filename}': {e}")
        sys.exit(1)

    try:
        # Lexical Analysis
        analyzer = LexicalAnalyzer(source_code)
        tokens = analyzer.tokenize()
        
        # Parsing
        parser = Parser(tokens)
        ast = parser.parse()
        
        # Standardization
        standardizer = Standardizer(ast)
        st = standardizer.standardize()
        
        # Evaluation
        cse_machine = CSEMachine(st)
        result = cse_machine.evaluate()
        
        # Print the final result
        if result is not None:
            print("Output of the above program is:")
            print(result)
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='RPAL Interpreter',
        usage='python myrpal.py [-ast] [-st] filename'
    )
    parser.add_argument('filename', help='RPAL source file to process')
    parser.add_argument('-ast', action='store_true', help='Print abstract syntax tree only')
    parser.add_argument('-st', action='store_true', help='Print standardized tree only')
    
    # Parse command line arguments
    args = parser.parse_args()
    
    # Validate file exists
    if not os.path.exists(args.filename):
        print(f"Error: File '{args.filename}' not found.")
        sys.exit(1)

    # Check for mutually exclusive options
    if args.ast and args.st:
        print("Error: Cannot use both -ast and -st options together.")
        sys.exit(1)
    
    # Execute based on flags
    if args.ast:
        print_ast_only(args.filename)
    elif args.st:
        print_st_only(args.filename)
    else:
        run_full_interpreter(args.filename)

if __name__ == "__main__":
    main()