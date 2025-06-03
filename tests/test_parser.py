import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from lexical_analyzer.lexical_analyzer import LexicalAnalyzer
from lexical_analyzer.token import Token, TokenType
from parser.parser import Parser
from parser.utils import Node

class TestParser(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        pass
    
    def parse_source(self, source):
        """Helper method to parse source code."""
        analyzer = LexicalAnalyzer(source)
        tokens = analyzer.get_tokens()
        parser = Parser(tokens)
        # Capture output to avoid printing during tests
        import io
        import contextlib
        
        with contextlib.redirect_stdout(io.StringIO()):
            parser.E()
        
        return parser.token_stack.peek()
    
    def test_simple_identifier(self):
        """Test parsing a simple identifier."""
        source = "x"
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        self.assertEqual(root.value, "<ID:x>")
    
    def test_simple_integer(self):
        """Test parsing a simple integer."""
        source = "42"
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        self.assertEqual(root.value, "<INT:42>")
    
    def test_simple_string(self):
        """Test parsing a simple string."""
        source = '"hello"'
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        self.assertEqual(root.value, '<STR:"hello">')
    
    def test_let_expression(self):
        """Test parsing a let expression."""
        source = "let x = 5 in x"
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        self.assertEqual(root.value, "let")
        
        # Should have two children: assignment and body
        self.assertIsNotNone(root.left)
    
    def test_function_definition(self):
        """Test parsing a function definition."""
        source = "fn x . x + 1"
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        self.assertEqual(root.value, "lambda")
    
    def test_arithmetic_expression(self):
        """Test parsing arithmetic expressions."""
        source = "1 + 2 * 3"
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        # Should respect operator precedence
        self.assertEqual(root.value, "+")
    
    def test_parentheses(self):
        """Test parsing expressions with parentheses."""
        source = "(1 + 2) * 3"
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        self.assertEqual(root.value, "*")
    
    def test_conditional_expression(self):
        """Test parsing conditional expressions."""
        source = "true -> 1 | 2"
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        self.assertEqual(root.value, "->")
    
    def test_function_application(self):
        """Test parsing function application."""
        source = "f x"
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        self.assertEqual(root.value, "gamma")
    
    def test_complex_expression(self):
        """Test parsing a complex expression."""
        source = "let f x = x + 1 in f 5"
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        self.assertEqual(root.value, "let")
    
    def test_nested_let(self):
        """Test parsing nested let expressions."""
        source = "let x = let y = 1 in y in x"
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        self.assertEqual(root.value, "let")
    
    def test_tuple_expression(self):
        """Test parsing tuple expressions."""
        source = "1, 2, 3"
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        self.assertEqual(root.value, "tau")
    
    def test_where_expression(self):
        """Test parsing where expressions."""
        source = "f x where f y = y + 1"
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        self.assertEqual(root.value, "where")
    
    def test_recursive_function(self):
        """Test parsing recursive functions."""
        source = "let rec f x = f x in f 1"
        root = self.parse_source(source)
        
        self.assertIsNotNone(root)
        self.assertEqual(root.value, "let")
    
    def test_syntax_error(self):
        """Test syntax error handling."""
        source = "let x = in y"  # Missing expression after =
        
        with self.assertRaises(SyntaxError):
            self.parse_source(source)
    
    def test_missing_parenthesis(self):
        """Test missing parenthesis error."""
        source = "(1 + 2"  # Missing closing parenthesis
        
        with self.assertRaises(SyntaxError):
            self.parse_source(source)

if __name__ == '__main__':
    unittest.main()