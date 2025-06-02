import re

# letter_regex = r"[a-zA-Z]"
# digit_regex = r"[0-9]"
# operator_regex = r"[+\-*<>&.@/:=`~|$!#%^_\[\]{}\"\'\?]"
# IDENTIFIER = r"[a-zA-Z][a-zA-Z0-9_]*"
# INTEGER = r"[0-9]+"
# STRING = r"\"(\\[tn\\\"']|[();,]|\s|[a-zA-Z0-9+\-*<>&.@/:=`~|$!#%^_\[\]{}\'\?])*\""

class TokenType:
    """Enum-like class for token types in RPAL"""
    # Keywords
    LET = "let"
    IN = "in"
    FN = "fn"
    WHERE = "where"
    TRUE = "true"
    FALSE = "false"
    NIL = "nil"
    DUMMY = "dummy"
    WITHIN = "within"
    REC = "rec"
    LIST = "list"

    # Punction
    LEFT_PAREN = "("
    RIGHT_PAREN = ")"

    # Operators
    AUG = "aug"
    OR = "or"
    AND = "and"
    NOT = "not"
    GREATER_THAN = "gr"
    GREATER_THAN_OR_EQUAL = "ge"
    LESS_THAN = "ls"
    LESS_THAN_OR_EQUAL = "le"
    EQUAL = "eq"
    NOT_EQUAL = "ne"
    PLUS = "+"
    MINUS = "-"
    MULTIPLY = "*"
    DIVIDE = "/"
    POWER = "**"
    EQUALS = "="
    
    # Symbols
    DOT = "."
    COMMA = ","
    ARROW = "->"
    BAR = "|"
    AMPERSAND = "&"
    AT = "@"
    
    # Identifiers and literals
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    STRING = "STRING"
    
    # Other
    DELETE = "DELETE"
    EOF = "EOF"


class Token:
    """Represent a token in the RPAL language."""
    def __init__(self, token_type, lexeme, line, column):
        """
        Initialize a new token
        
        Args:
            token_type (str): The type of the token.
            lexeme (str): The actual text of the token.
            line (int): The line number where the token was found.
            column (int): The column number where the token was found.
        """
        self.token_type = token_type
        self.lexeme = lexeme
        self.line = line
        self.column = column

    def __repr__(self):
        """Return a string representation of the token."""
        return f"Token(type={self.token_type}, lexeme='{self.lexeme}', line={self.line}, column={self.column})"