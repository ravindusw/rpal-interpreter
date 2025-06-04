# RPAL Interpreter

A Python-based interpreter for the Right-reference Pedagogic Algorithmic Language (RPAL) consisting of Lexical Analyzer, Parser, Standardizer, and Control Stack Environment (CSE) Machine.

## Overview

This project implements a complete interpreter for RPAL (Right-reference Pedagogic Algorithmic Language), a functional programming language designed for educational purposes. The interpreter follows the standard compilation pipeline with four main components:

1. **Lexical Analyzer** - Tokenizes the input RPAL program into meaningful symbols
2. **Parser** - Builds an Abstract Syntax Tree (AST) from tokens using recursive descent parsing
3. **Standardizer** - Transforms the AST into a standardized form by applying transformation rules
4. **CSE Machine** - Executes the standardized program using a Control-Stack-Environment model

## Features

### Language Support
- **Arithmetic Operations**: `+`, `-`, `*`, `/`, `**` (exponentiation)
- **Comparison Operations**: `eq`, `ne`, `gr`, `ge`, `ls`, `le` (or `>`, `>=`, `<`, `<=`)
- **Logical Operations**: `&` (and), `or`, `not`
- **Conditional Expressions**: `condition -> expr1 | expr2`
- **Function Definitions**: Lambda expressions and named functions
- **Recursion**: Full recursive function support with `rec` keyword
- **Tuple Operations**: Tuple creation, access, and manipulation
- **String Operations**: String concatenation and manipulation
- **Variable Binding**: `let` expressions and `where` clauses
- **Simultaneous Definitions**: `and` operator for multiple bindings
- **Higher-order Functions**: Functions as first-class values

### Built-in Functions
- **I/O Functions**: `Print` for output
- **Type Checking**: `Isinteger`, `Istruthvalue`, `Isstring`, `Istuple`, `Isfunction`, `Isdummy`
- **String Functions**: `Stem` (first character), `Stern` (rest of string), `Conc` (concatenation)
- **Tuple Functions**: `Order` (length), tuple indexing
- **Utility Functions**: `Null` (empty check), `ItoS` (integer to string)

## Installation and Setup

### Prerequisites
- Python 3.6 or higher
- No external dependencies required (uses only Python standard library)

### Installation Steps
1. Clone or download the project:
```bash
git clone <repository-url>
cd rpal-interpreter
```

2. Verify the project structure:
```
rpal-interpreter/
├── myrpal.py                    # Main interpreter entry point
├── src/
│   ├── lexical_analyzer/
│   │   └── lexical_analyzer.py  # Tokenization module
│   ├── parser/
│   │   ├── parser.py           # AST generation
│   │   └── utils.py            # AST node definitions
│   ├── standardizer/
│   │   └── standardizer.py     # AST standardization
│   └── cse_machine/
│       ├── cse_machine.py      # Program execution engine
│       ├── utils.py            # CSE machine utilities
│       └── csem_output/        # Output directory for stack traces
├── examples/                   # Sample RPAL programs
│   ├── sample1.txt
│   ├── sample2.txt
│   └── ...
├── Makefile                    # Build automation
└── README.md
```

## Usage

### Command Line Interface

#### Basic Usage
```bash
# Run interpreter on a file
python myrpal.py examples/sample1.txt

# Display Abstract Syntax Tree only
python myrpal.py -ast examples/sample1.txt
```

#### Using Makefile (Alternative)
```bash
# Run interpreter
make run FILE=examples/sample1.txt

# Display AST
make ast FILE=examples/sample1.txt

# Run all test files
make test

# Clean generated files
make clean
```

### Sample Programs

The `examples/` directory contains various sample RPAL programs demonstrating different language features:

- `sample1.txt` - Basic variable binding and arithmetic
- `sample3.txt` - String operations and printing
- `sample4.txt` - Function definitions and calls
- `sample5.txt` - Lambda expressions
- `sample7.txt` - Nested let expressions
- `sample8.txt` - Where clauses and function composition
- `sample11.txt` - Conditional expressions
- `sample13.txt` - Tuple operations
- `sample15.txt` - Simultaneous definitions with `and`
- `sample26.txt` - Recursive functions and complex operations

## Language Syntax and Examples

### Basic Variable Binding
```rpal
let x = 5 in
let y = 10 in
Print(x + y)
// Output: 15
```

### Function Definitions
```rpal
// Named function
let Inc x = x + 1 in Print(Inc 5)
// Output: 6

// Lambda function
let Inc = fn x. x + 1 in Print(Inc 5)
// Output: 6

// Multi-parameter function
let Add (x, y) = x + y in Print(Add (3, 4))
// Output: 7
```

### Conditional Expressions
```rpal
let x = 5 in
let result = x > 3 -> "big" | "small" in
Print(result)
// Output: "big"
```

### Recursive Functions
```rpal
rec factorial n = 
    n eq 0 -> 1 | n * factorial (n - 1)
in Print(factorial 5)
// Output: 120
```

### Tuple Operations
```rpal
let tuple = (1, 2, 3) in
Print(Order tuple)  // Print tuple length
// Output: 3

let student = ("John", "Doe", 20) in
Print(student)
// Output: ("John", "Doe", 20)
```

### Where Clauses
```rpal
Print(sqr_sum) where sqr_sum = x**2 + y**2
where x = 3
where y = 4
// Output: 25
```

### Simultaneous Definitions
```rpal
let x = 1 and y = 2 and z = 3 in
Print((x, y, z))
// Output: (1, 2, 3)
```

## Implementation Details

### Lexical Analysis
- Tokenizes RPAL source code into symbols
- Handles keywords, identifiers, literals, operators, and delimiters
- Supports both single and double quotes for strings
- Manages whitespace and comments

### Parsing
- Implements recursive descent parser
- Builds Abstract Syntax Tree (AST) using first-child next-sibling representation
- Handles operator precedence and associativity
- Supports complex nested expressions

### Standardization
The standardizer applies transformation rules to convert the AST into a standard form:

1. **Let expressions**: `let x = E in P` → `(λx.P) E`
2. **Where expressions**: `P where x = E` → `(λx.P) E`
3. **Function forms**: `f x y = E` → `f = λx.λy.E`
4. **Multi-parameter functions**: `λ(x,y).E` → `λx.λy.E`
5. **Within expressions**: Handles nested scoping
6. **At expressions**: `E1 @N E2` → `N E1 E2`
7. **Simultaneous definitions**: `and` expressions with tau tuples
8. **Recursive definitions**: `rec f = E` → `f = Y λf.E`

### CSE Machine Evaluation

The Control-Stack-Environment (CSE) Machine executes the standardized program using 13 evaluation rules:

1. **Rule 1**: Stack identifiers and literals
2. **Rule 2**: Stack lambda closures
3. **Rule 3**: Apply built-in operators
4. **Rule 4**: Apply lambda functions
5. **Rule 5**: Exit environments
6. **Rule 6**: Binary operations
7. **Rule 7**: Unary operations
8. **Rule 8**: Conditional evaluation (beta rule)
9. **Rule 9**: Tuple formation (tau rule)
10. **Rule 10**: Tuple selection
11. **Rule 11**: Multi-parameter functions
12. **Rule 12**: Y combinator for recursion
13. **Rule 13**: Eta conversion for recursion

#### CSE Machine Output
The CSE machine writes detailed execution traces to external files:
- `src/cse_machine/csem_output/control_stack.txt` - Control stack states during execution
- `src/cse_machine/csem_output/value_stack.txt` - Value stack states during execution

These files are useful for debugging and understanding program execution flow.

## Built-in Functions Reference

| Function | Arity | Description | Example |
|----------|-------|-------------|---------|
| `Print` | 1+ | Print values to output | `Print("Hello", 42)` |
| `Isinteger` | 1 | Check if value is integer | `Isinteger(42)` → `true` |
| `Istruthvalue` | 1 | Check if value is boolean | `Istruthvalue(true)` → `true` |
| `Isstring` | 1 | Check if value is string | `Isstring("hi")` → `true` |
| `Istuple` | 1 | Check if value is tuple | `Istuple((1,2))` → `true` |
| `Isfunction` | 1 | Check if value is function | `Isfunction(fn x.x)` → `true` |
| `Isdummy` | 1 | Check if value is dummy | `Isdummy(dummy)` → `true` |
| `Stem` | 1 | First character of string | `Stem("hello")` → `"h"` |
| `Stern` | 1 | Rest of string | `Stern("hello")` → `"ello"` |
| `Conc` | 2 | String concatenation | `Conc("hi", "there")` → `"hithere"` |
| `Order` | 1 | Tuple length | `Order((1,2,3))` → `3` |
| `Null` | 1 | Check if empty/nil | `Null(nil)` → `true` |
| `ItoS` | 1 | Integer to string | `ItoS(42)` → `"42"` |

## **Important Usage Notes**

### String Literals
- Both single (`'`) and double (`"`) quotes are supported for strings
- Recommended to use double quotes for consistency
- Avoid mixing quote types in the same program

### Function Definitions
- Always include space between function name and parameters:
  - ✅ Correct: `f (x) = x + 1` or `f x = x + 1`
  - ❌ Incorrect: `f(x) = x + 1` or `fx = x + 1`

### Negative Parameters
- Use parentheses around negative parameters in function definitions and calls:
  - ✅ Correct: `f (-2)` or `f (-x)`
  - ❌ Incorrect: `f -2` (interpreted as `f minus 2`)

### Operator Precedence
- Use parentheses to ensure correct evaluation order
- Function application has higher precedence than operators

## Debugging and Troubleshooting

### Common Issues
1. **Syntax Errors**: Check for proper spacing in function definitions
2. **Undefined Variables**: Ensure all variables are properly bound
3. **Type Mismatches**: Verify operator usage with correct types
4. **Stack Traces**: Check `src/cse_machine/csem_output/` files for execution details

### Debugging Tips
- Use `-ast` flag to examine the generated Abstract Syntax Tree
- Check control and value stack files for execution flow
- Start with simple examples and gradually increase complexity
- Verify parentheses placement in complex expressions

## Testing

### Run All Tests
```bash
make test          # Run all example files
make test-ast      # Generate AST for all files
```

### Individual File Testing
```bash
python myrpal.py examples/sample1.txt
python myrpal.py -ast examples/sample5.txt
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes with proper documentation
4. Add test cases for new features
5. Ensure all existing tests pass
6. Submit a pull request with detailed description

## License

This project is developed for educational purposes as part of CS3513 Programming Languages course at University of Moratuwa.

## References

- RPAL Language Specification
- Functional Programming Language Implementation
- Control-Stack-Environment Machine Architecture
- Recursive Descent Parsing Techniques
- Lambda Calculus and Combinatory Logic
