import unittest
import sys
import os

# Add the src directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from src.lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from src.lexical_analyzer.token import Token, TokenType

class TestLexicalAnalyzer(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass
    
    def test_simple_tokens(self):
        """Test basic token recognition."""
        source = "let x = 5"
        analyzer = LexicalAnalyzer(source)
        tokens = analyzer.get_tokens()
        
        expected_types = [TokenType.LET, TokenType.IDENTIFIER, TokenType.EQUALS, TokenType.INTEGER, TokenType.EOF]
        actual_types = [token.token_type for token in tokens]
        
        self.assertEqual(expected_types, actual_types)
    
    def test_keywords(self):
        """Test keyword recognition."""
        source = "let in fn where rec"
        analyzer = LexicalAnalyzer(source)
        tokens = analyzer.get_tokens()
        
        expected_types = [TokenType.LET, TokenType.IN, TokenType.FN, TokenType.WHERE, TokenType.REC, TokenType.EOF]
        actual_types = [token.token_type for token in tokens]
        
        self.assertEqual(expected_types, actual_types)
    
    def test_operators(self):
        """Test operator recognition."""
        source = "+ - * / ** = -> |"
        analyzer = LexicalAnalyzer(source)
        tokens = analyzer.get_tokens()
        
        expected_types = [
            TokenType.PLUS, TokenType.MINUS, TokenType.MULTIPLY, 
            TokenType.DIVIDE, TokenType.POWER, TokenType.EQUALS,
            TokenType.ARROW, TokenType.BAR, TokenType.EOF
        ]
        actual_types = [token.token_type for token in tokens]
        
        self.assertEqual(expected_types, actual_types)
    
    def test_identifiers(self):
        """Test identifier recognition."""
        source = "myVar _test var123 Print"
        analyzer = LexicalAnalyzer(source)
        tokens = analyzer.get_tokens()
        
        # All should be identifiers (not keywords)
        for i in range(4):  # Skip EOF token
            self.assertEqual(tokens[i].token_type, TokenType.IDENTIFIER)
        
        # Check lexemes
        expected_lexemes = ["myVar", "_test", "var123", "Print"]
        actual_lexemes = [tokens[i].lexeme for i in range(4)]
        self.assertEqual(expected_lexemes, actual_lexemes)
    
    def test_integers(self):
        """Test integer recognition."""
        source = "123 0 999"
        analyzer = LexicalAnalyzer(source)
        tokens = analyzer.get_tokens()
        
        for i in range(3):
            self.assertEqual(tokens[i].token_type, TokenType.INTEGER)
        
        expected_lexemes = ["123", "0", "999"]
        actual_lexemes = [tokens[i].lexeme for i in range(3)]
        self.assertEqual(expected_lexemes, actual_lexemes)
    
    def test_strings(self):
        """Test string recognition."""
        source = '"hello" "world with spaces" ""'
        analyzer = LexicalAnalyzer(source)
        tokens = analyzer.get_tokens()
        
        for i in range(3):
            self.assertEqual(tokens[i].token_type, TokenType.STRING)
        
        expected_lexemes = ['"hello"', '"world with spaces"', '""']
        actual_lexemes = [tokens[i].lexeme for i in range(3)]
        self.assertEqual(expected_lexemes, actual_lexemes)
    
    def test_comments(self):
        """Test comment handling."""
        source = "let x = 5 // this is a comment\nin x"
        analyzer = LexicalAnalyzer(source)
        tokens = analyzer.get_tokens()
        
        # Comments should be ignored
        expected_types = [TokenType.LET, TokenType.IDENTIFIER, TokenType.EQUALS, 
                         TokenType.INTEGER, TokenType.IN, TokenType.IDENTIFIER, TokenType.EOF]
        actual_types = [token.token_type for token in tokens]
        
        self.assertEqual(expected_types, actual_types)
    
    def test_complex_expression(self):
        """Test a complex RPAL expression."""
        source = 'let f x = x + 1 in f 5'
        analyzer = LexicalAnalyzer(source)
        tokens = analyzer.get_tokens()
        
        expected_types = [
            TokenType.LET, TokenType.IDENTIFIER, TokenType.IDENTIFIER, TokenType.EQUALS,
            TokenType.IDENTIFIER, TokenType.PLUS, TokenType.INTEGER, TokenType.IN,
            TokenType.IDENTIFIER, TokenType.INTEGER, TokenType.EOF
        ]
        actual_types = [token.token_type for token in tokens]
        
        self.assertEqual(expected_types, actual_types)
    
    def test_line_column_tracking(self):
        """Test line and column tracking."""
        source = "let\nx = 5"
        analyzer = LexicalAnalyzer(source)
        tokens = analyzer.get_tokens()
        
        # let should be at line 1, column 1
        self.assertEqual(tokens[0].line, 1)
        self.assertEqual(tokens[0].column, 1)
        
        # x should be at line 2, column 1
        self.assertEqual(tokens[1].line, 2)
        self.assertEqual(tokens[1].column, 1)
    
    def test_error_handling(self):
        """Test error handling for invalid characters."""
        source = "let x = 5 $ invalid"
        analyzer = LexicalAnalyzer(source)
        
        with self.assertRaises(ValueError):
            analyzer.get_tokens()

if __name__ == '__main__':
    unittest.main()