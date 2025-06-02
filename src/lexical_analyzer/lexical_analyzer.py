from .scanner import Scanner
from .token import Token, TokenType

class LexicalAnalyzer:
    """
    Lexical analyzer for RPAL source code.
    It uses a scanner to read characters and produces tokens.
    """

    def __init__(self, source):
        """
        Initialize the lexical analyzer with the source code.

        Args:
            source: The RPAL source code as a string
        """
        self.scanner = Scanner(source)
        self.tokens = []
        self.current_token_index = 0
        self.keywords = {
            "let": TokenType.LET,
            "in": TokenType.IN,
            "fn": TokenType.FN,
            "where": TokenType.WHERE,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "nil": TokenType.NIL,
            "dummy": TokenType.DUMMY,
            "within": TokenType.WITHIN,
            "rec": TokenType.REC,
            "aug": TokenType.AUG,
            "or": TokenType.OR,
            "and": TokenType.AND,
            "not": TokenType.NOT,
            "gr": TokenType.GREATER_THAN,
            "ge": TokenType.GREATER_THAN_OR_EQUAL,
            "ls": TokenType.LESS_THAN,
            "le": TokenType.LESS_THAN_OR_EQUAL,
            "eq": TokenType.EQUAL,
            "ne": TokenType.NOT_EQUAL
        }

    def scan_token(self):
        """
        Scan the next token from the source code.

        Returns:
            Token: The next token found in the source code.
        """
        # if self.scanner.is_at_end():
        #     line, column = self.scanner.current_position
        #     self.tokens.append(Token(TokenType.EOF, "EOF", line, column))
        #     return self.tokens[-1]
        
        char = self.scanner.advance()

        if char is None:
            return None  # End of file reached

        line, column = self.scanner.current_position()
        column -= 1  # Adjust column for the current character

        # Handle whitespaces
        if char.isspace():
            return self.scan_token()
        
        # Handle strings
        if char == '"':
            string_literal = self.consume_string()
            self.tokens.append(Token(TokenType.STRING, string_literal, line, column))
            return self.tokens[-1]
        
        # Handle numbers
        if char.isdigit():
            number = self.consume_number(char)
            self.tokens.append(Token(TokenType.INTEGER , number, line, column))
            return self.tokens[-1]
        
        # Handle identifiers or keywords
        if char.isalpha():
            identifier = self.consume_identifier(char)
            if identifier in self.keywords:
                token_type = self.keywords[identifier]
            else:
                token_type = TokenType.IDENTIFIER
            self.tokens.append(Token(token_type, identifier, line, column))
            return self.tokens[-1]
        
        # Handle operators and other symbols
        if char == '(':
            self.tokens.append(Token(TokenType.LEFT_PAREN, '(', line, column))
            return self.tokens[-1]
        elif char == ')':
            self.tokens.append(Token(TokenType.RIGHT_PAREN, ')', line, column))
            return self.tokens[-1]
        elif char == '>':
            if self.scanner.peek() == '=':
                self.scanner.advance()
                self.tokens.append(Token(TokenType.GREATER_THAN_OR_EQUAL, '>=', line, column))
            else:
                self.tokens.append(Token(TokenType.GREATER_THAN, '>', line, column))
            return self.tokens[-1]
        elif char == '<':
            if self.scanner.peek() == '=':
                self.scanner.advance()
                self.tokens.append(Token(TokenType.LESS_THAN_OR_EQUAL, '<=', line, column))
            else:
                self.tokens.append(Token(TokenType.LESS_THAN, '<', line, column))
            return self.tokens[-1]
        elif char == '+':
            self.tokens.append(Token(TokenType.PLUS, '+', line, column))
            return self.tokens[-1]
        elif char == '-':
            if self.scanner.peek() == '>':
                self.scanner.advance()
                self.tokens.append(Token(TokenType.ARROW, '->', line, column))
            else:
                self.tokens.append(Token(TokenType.MINUS, '-', line, column))
            return self.tokens[-1]
        elif char == '*':
            if self.scanner.peek() == '*':
                self.scanner.advance()
                self.tokens.append(Token(TokenType.POWER, '**', line, column))
            else:
                self.tokens.append(Token(TokenType.MULTIPLY, '*', line, column))
            return self.tokens[-1]
        elif char == '/':
            if self.scanner.peek() == '/':
                # Consume the comment
                while self.scanner.peek() not in (None, '\n'):
                    self.scanner.advance()
                # If we reach a newline, we can continue scanning for tokens
                self.scanner.advance()
                return self.scan_token()
            else:
                self.tokens.append(Token(TokenType.DIVIDE, '/', line, column))
            return self.tokens[-1]
        elif char == '=':
            self.tokens.append(Token(TokenType.EQUALS, '=', line, column))
            return self.tokens[-1]
        elif char == '.':
            self.tokens.append(Token(TokenType.DOT, '.', line, column))
            return self.tokens[-1]
        elif char == ',':
            self.tokens.append(Token(TokenType.COMMA, ',', line, column))
            return self.tokens[-1]
        elif char == '|':
            self.tokens.append(Token(TokenType.BAR, '|', line, column))
            return self.tokens[-1]
        elif char == '&':
            self.tokens.append(Token(TokenType.AMPERSAND, '&', line, column))
            return self.tokens[-1]
        elif char == '@':
            self.tokens.append(Token(TokenType.AT, '@', line, column))
            return self.tokens[-1]
        else:
            # Handle unexpected characters
            raise ValueError(f"Unexpected character '{char}' at line {line}, column {column}")
        
    def consume_string(self):
        """
        Consume a string literal from the source code.

        Returns:
            str: The string literal found.
        """
        string_literal = '"'
        while True:
            char = self.scanner.advance()
            if char == '"':
                string_literal += '"'
                break
            elif char is None:
                raise ValueError("Unterminated string literal")
            else:
                string_literal += char
        return string_literal
    
    def consume_number(self, char):
        """
        Consume a number from the source code.

        Returns:
            str: The number found.
        """
        number = char
        while True:
            char = self.scanner.peek()
            if char is None or not char.isdigit():
                break
            number += self.scanner.advance()
        return number
    
    def consume_identifier(self, char):
        """
        Consume an identifier or keyword from the source code.

        Returns:
            str: The identifier or keyword found.
        """
        identifier = char
        while True:
            char = self.scanner.peek()
            if char is None or not (char.isalnum() or char == '_'):
                break
            identifier += self.scanner.advance()
        return identifier
        
    def get_tokens(self):
        """
        Scan all tokens from the source code until EOF is reached.
        
        Returns:
            list: A list of tokens.
        """
        while not self.scanner.is_at_end():
            print("Scanned so far: %s", [str(x.lexeme) for x in self.tokens])
            self.scan_token()
        
        # Add EOF token at the end
        line, column = self.scanner.current_position()
        self.tokens.append(Token(TokenType.EOF, "EOF", line, column))

        return self.tokens
    


def main():
    # Example usage
    source_code = ""
    
    try:
        # Use a relative path or full path
        with open("./examples/sample.txt", "r") as file:
            print("Reading source code from 'examples/sample.txt'...")
            source_code = file.read().strip()
    except FileNotFoundError:
        # Fallback to a simple example if file not found
        print("File not found. Using example source code instead.")
        source_code = "let x = 5 in x + 3"
    
    print("Source Code:")
    print(source_code)

    analyzer = LexicalAnalyzer(source_code)
    tokens = analyzer.get_tokens()
    
    print("\nTokens:")
    for token in tokens:
        print(token.token_type, end=' ')


if __name__ == "__main__":
    main()
