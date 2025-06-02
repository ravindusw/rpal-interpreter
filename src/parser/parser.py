from src.lexical_analyzer.token import Token, TokenType
from .utils import Node, Stack

class Parser:
    """
    Parser for the RPAL language.
    Converts a stream of tokens into an abstract syntax tree.
    """
    
    def __init__(self, tokens):
        """
        Initializes the parser with a list of tokens.
        
        Args:
            tokens (list[Token]): List of tokens to parse.
        """
        self.tokens = tokens
        self.current_token_index = 0
        self.token_stack = Stack() # Stack to hold nodes of the abstract syntax tree

    def get_current_token(self):
        """
        Retrieves the current token from the token stream.
        
        Returns:
            Token: The current token in the stream.
        """
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None
    
    def consume_token(self):
        """
        Consume the current token and update the current_token_index
        """
        print(self.get_current_token())
        self.current_token_index += 1

    def build_tree(self, value, num_children):
        """
        Build the abstract syntax tree node with the given value and number of children.
        
        Args:
            value (str): The value of the node.
            num_children (int): The number of children for this node.
        """
        # First child next sibling tree
        p = None
        for _ in range(num_children):
            child = self.token_stack.pop()
            child.right = p
            p = child
        self.token_stack.push(Node(value, p, None))

    def preorder_traversal(self, node, dots=""):
        """
        Perform a preorder traversal of the abstract syntax tree and print the nodes.
        
        Args:
            node (Node): The root node of the tree.
        """
        if node is None:
            return
        print(dots+node.value)
        self.preorder_traversal(node.left, dots+".")
        self.preorder_traversal(node.right, dots)

    def parse(self):
        """
        Parse the token stream and build a derivation tree.
        """
        self.E()
        self.preorder_traversal(self.token_stack.peek())

    
    # Expressions #####################
    
    # ---------------------------------
    # E -> let D in E       => let
    # E -> fn Vb+ . E       => lambda
    # E -> Ew
    # ---------------------------------

    def E(self):
        token = self.get_current_token()

        if token is None:
            return None
        
        if token.token_type == TokenType.LET:
            self.consume_token()
            self.D()
            token = self.get_current_token()
            if token and token.token_type == TokenType.IN:
                self.consume_token()
            elif token:
                raise SyntaxError(f"Expected 'in' but got '{token.token_type}' at line {token.line} column {token.column}.")
            else:
                raise SyntaxError("Expected 'in' but reached end of input.")
            self.E()
            print("E -> let D in E")
            self.build_tree("let", 2)

        elif token.token_type == TokenType.FN:
            self.consume_token()
            n = 1 # Count the number of Vb
            self.Vb()
            token = self.get_current_token()
            while token and token.token_type != TokenType.DOT:
                self.Vb()
                n += 1
                token = self.get_current_token()
            if token is None:
                raise SyntaxError(f"Expected '.' after function parameters but reached end of input.")
            elif token.token_type == TokenType.DOT:
                self.consume_token()
            else:
                raise SyntaxError(f"Expected '.' after function parameters but got {token.token_type} at line {token.line} column {token.column}.")
            self.E()
            print("E -> fn Vb+ . E")
            self.build_tree("lambda", n+1)

        else:
            self.Ew()
            print("E -> Ew")

    # ---------------------------------
    # Ew -> T where Dr      => where
    # Ew -> T
    # ---------------------------------
    
    def Ew(self):
        self.T()
        token = self.get_current_token()
        if token and token.token_type == TokenType.WHERE:
            self.consume_token()
            self.Dr()
            print("Ew -> T where Dr")
            self.build_tree("where", 2)

    
    # Tuple Expressions ###############

    # ---------------------------------
    # T -> Ta ( , Ta )+      => tau
    # T -> Ta
    # ---------------------------------

    def T(self):
        self.Ta()
        token = self.get_current_token()
        n = 1  # Count the number of Ta
        while token and token.token_type == TokenType.COMMA:
            self.consume_token()
            self.Ta()
            n += 1
            token = self.get_current_token()
            print("T -> Ta ( , Ta )+")
        if n > 1:
            self.build_tree("tau", n)
        else:
            print("T -> Ta")

    # ---------------------------------
    # Ta -> Ta aug Tc           => aug
    # Ta -> Tc
    # This is left recursive, so
    # Replace with
    # Ta -> Tc ( aug Tc )*      => aug
    # ---------------------------------
    
    def Ta(self):
        self.Tc()
        token = self.get_current_token()
        while token and token.token_type == TokenType.AUG:
            self.consume_token()
            self.Tc()
            print("Ta -> Ta aug Tc")
            self.build_tree("aug", 2)
            token = self.get_current_token()

    # ---------------------------------
    # Tc -> B -> Tc | Tc        => ->
    # Tc -> B
    # ---------------------------------
    
    def Tc(self):
        self.B()
        token = self.get_current_token()
        if token and token.token_type == TokenType.ARROW:
            self.consume_token()
            self.Tc()
            token = self.get_current_token()
            if token and token.token_type == TokenType.BAR:
                self.consume_token()
            elif token is None:
                raise SyntaxError("Expected '|' after '->' but reached end of input.")
            else:
                raise SyntaxError(f"Expected '|' after '->' but got {token.token_type} at line {token.line} column {token.column}.")
            self.Tc()
            print("Tc -> B -> Tc | Tc")
            self.build_tree("->", 3)

    
    # Boolean Expressions #############

    # ---------------------------------
    # B -> B or Bt              => or
    # B -> Bt
    # This is left recursive, so
    # Replace with
    # B -> Bt ( or Bt )*        => or
    # ---------------------------------

    def B(self):
        self.Bt()
        token = self.get_current_token()
        while token and token.token_type == TokenType.OR:
            self.consume_token()
            self.Bt()
            print("B -> B or Bt")
            self.build_tree("or", 2)
            token = self.get_current_token()

    # ---------------------------------
    # Bt -> Bt & Bs             => &
    # Bt -> Bs
    # This is left recursive, so
    # Replace with
    # Bt -> Bs ( & Bs )*        => &
    # ---------------------------------

    def Bt(self): 
        self.Bs()
        token = self.get_current_token()
        while token and token.token_type == TokenType.AMPERSAND:
            self.consume_token()
            self.Bs()
            print("Bt -> Bs & Bs")
            token = self.get_current_token()
            self.build_tree("&", 2)

    # ---------------------------------
    # Bs -> not Bp              => not
    # Bs -> Bp
    # ---------------------------------

    def Bs(self):
        token = self.get_current_token()
        if token and token.token_type == TokenType.NOT:
            self.consume_token()
            self.Bp()
            print("Bs -> not Bp")
            self.build_tree("not", 1)
        else:
            self.Bp()
            print("Bs -> Bp")

    # ---------------------------------
    # Bp -> A op A              => op
    # Bp -> A
    # where op can be one of:
    # gr, ge, ls, le, eq, ne
    # ---------------------------------

    def Bp(self):
        self.A()
        token = self.get_current_token()
        if token and token.token_type in [TokenType.GREATER_THAN, TokenType.GREATER_THAN_OR_EQUAL, 
                                     TokenType.LESS_THAN, TokenType.LESS_THAN_OR_EQUAL, 
                                     TokenType.EQUAL, TokenType.NOT_EQUAL]:
            self.consume_token()
            self.A()
            print(f"Bp -> A {token.lexeme} A")
            self.build_tree(token.token_type, 2)

    
    # Arithmetic Expressions ##########
    
    # ---------------------------------
    # A -> A + At           => +
    # A -> A - At           => -
    # A -> + At
    # A -> - At             => neg
    # A -> At
    # This is left recursive, so
    # Replace with,
    # A -> + At ( + At | - At )* => +/-
    # A -> - At ( + At | - At )* => neg +/-
    # A -> At ( + At | - At )*   => +/-
    # ---------------------------------
 
    def A(self):
        token = self.get_current_token()   
        if token.token_type == TokenType.PLUS:
            self.consume_token()
            self.At()
            print("A -> + At")
        elif token.token_type == TokenType.MINUS:
            self.consume_token()
            self.At()
            print("A -> - At")
            self.build_tree("neg", 1)       
        else:
            self.At()

        token = self.get_current_token()
        while token and token.token_type in [TokenType.PLUS, TokenType.MINUS]:
            self.consume_token()
            self.At()
            print(f"A -> A {token.lexeme} At")
            if token.token_type == TokenType.PLUS:
                self.build_tree("+", 2)
            else:
                self.build_tree("-", 2)
            token = self.get_current_token()

    # ---------------------------------
    # At -> At * Af             => *
    # At -> At / Af             => /
    # At -> Af
    # This is left recursive, so
    # Replace with,
    # At -> Af ( * Af | / Af)*
    # ---------------------------------

    def At(self): 
        self.Af()
        token = self.get_current_token()
        while token and token.token_type in [TokenType.MULTIPLY, TokenType.DIVIDE]:
            self.consume_token()
            self.Af()
            print(f"At -> At {token.lexeme} Af")
            self.build_tree(token.token_type, 2)
            token = self.get_current_token()

    # ---------------------------------
    # Af -> Ap ** Af            => **
    # Af -> Ap
    # ---------------------------------

    def Af(self):
        self.Ap()   
        token = self.get_current_token()
        if token.token_type == TokenType.POWER:
            self.consume_token()
            self.Af()
            print("Af -> Ap ** Af")
            self.build_tree("**", 2)
        else:
            print("Af -> Ap")

    # ---------------------------------
    # Ap -> Ap @ IDENTIFIER R       => @
    # Ap -> R
    # This is left recursive, so
    # Replace with,
    # Ap -> R ( @ IDENTIFIER R )*   => @
    # ---------------------------------

    def Ap(self): 
        self.R()
        token = self.get_current_token()
        while token and token.token_type == TokenType.AT:
            self.consume_token()
            token = self.get_current_token()
            if token and token.token_type != TokenType.IDENTIFIER:
                raise SyntaxError(f"Expected IDENTIFIER after '@' but got '{token.token_type}' at line {token.line} column {token.column}.")
            elif token is None:
                raise SyntaxError("Expected IDENTIFIER after '@' but reached end of input.")
            self.consume_token()
            self.token_stack.push(Node(f"<ID:{token.lexeme}>", None, None))  # Push IDENTIFIER node
            self.R()
            self.build_tree("@", 3)
            print("Ap -> Ap @ IDENTIFIER R")
            token = self.get_current_token()

    # (Ope)Rators and (Ope)Rands ######

    # ---------------------------------
    # R -> R Rn                 => gamma
    # R -> Rn
    # This is left recursive, so
    # Replace with,
    # R -> Rn ( Rn )*           => gamma
    # ---------------------------------

    def R(self):
        self.Rn()
        token = self.get_current_token()
        while token and token.token_type in [TokenType.LEFT_PAREN, TokenType.IDENTIFIER,
                                              TokenType.INTEGER, TokenType.STRING,
                                              TokenType.TRUE, TokenType.FALSE, TokenType.NIL,
                                              TokenType.DUMMY]:
            self.Rn()
            print("R -> R Rn")
            self.build_tree("gamma", 2)
            token = self.get_current_token()

    # ---------------------------------
    # Rn -> ( E )
    # Rn -> IDENTIFIER
    # Rn -> INTEGER
    # Rn -> STRING
    # Rn -> true            => true
    # Rn -> false           => false
    # Rn -> nil             => nil
    # Rn -> dummy           => dummy
    # ---------------------------------

    def Rn(self):
        token = self.get_current_token()
        
        if token is None:
            return None

        if token.token_type == TokenType.LEFT_PAREN:
            # Rn -> ( E )
            self.consume_token()
            self.E()
            token = self.get_current_token()
            if token and token.token_type == TokenType.RIGHT_PAREN:
                self.consume_token()
                print("Rn -> ( E )")
            elif token is None:
                raise SyntaxError("Expected ')' after expression but reached end of input.")
            else:
                raise SyntaxError(f"Expected ')' after expression but got '{token.token_type}' at line {token.line} column {token.column}.")
        elif token.token_type == TokenType.IDENTIFIER:
            # Rn -> IDENTIFIER
            self.consume_token()
            print("Rn -> IDENTIFIER")
            self.token_stack.push(Node(f"<ID:{token.lexeme}>", None, None))  # Push IDENTIFIER node
        elif token.token_type == TokenType.INTEGER:
            # Rn -> INTEGER
            self.consume_token()
            print("Rn -> INTEGER")
            self.token_stack.push(Node(f"<INT:{token.lexeme}>", None, None))  # Push INTEGER node
        elif token.token_type == TokenType.STRING:
            # Rn -> STRING
            self.consume_token()
            print("Rn -> STRING")
            self.token_stack.push(Node(f"<STR:{token.lexeme}>", None, None))  # Push STRING node
        elif token.token_type == TokenType.TRUE:
            # Rn -> true
            self.consume_token()
            print("Rn -> true")
            self.build_tree("true", 0)
        elif token.token_type == TokenType.FALSE:
            # Rn -> false
            self.consume_token()
            print("Rn -> false")
            self.build_tree("false", 0)
        elif token.token_type == TokenType.NIL:
            # Rn -> nil
            self.consume_token()
            print("Rn -> nil")
            self.build_tree("nil", 0)
        elif token.token_type == TokenType.DUMMY:
            # Rn -> dummy
            self.consume_token()
            print("Rn -> dummy")
            self.build_tree("dummy", 0)
        else:
            raise SyntaxError(f"Unexpected token: {token} at line {token.line} column {token.column}.")
        

    # Definitions #####################

    # ---------------------------------
    # D -> Da within D      => within
    # D -> Da
    # ---------------------------------    
        
    def D(self):
        self.Da()
        token = self.get_current_token()
        if token and token.token_type == TokenType.WITHIN:
            self.consume_token()
            self.D()
            print("D -> Da within D")
            self.build_tree("within", 2)

    # ---------------------------------
    # Da -> Dr ( and Dr )+      => and
    # Da -> Dr
    # ---------------------------------

    def Da(self):
        self.Dr()
        token = self.get_current_token()
        n = 1  # Count the number of Dr
        while token and token.token_type == TokenType.AND:
            self.consume_token()
            self.Dr()
            n += 1
            print("Da -> Dr ( and Dr )+")
            token = self.get_current_token()
        if n > 1:
            self.build_tree("and", n)

    # ---------------------------------
    # Dr -> rec Db              => rec
    # Dr -> Db
    # ---------------------------------

    def Dr(self):
        token = self.get_current_token()
        
        if token and token.token_type == TokenType.REC:
            self.consume_token()
            self.Db()
            print("Dr -> rec Db")
            self.build_tree("rec", 1)
        else:
            self.Db()
            print("Dr -> Db")

    # ---------------------------------
    # Db -> IDENTIFIER Vb+ = E  => function_form
    # Db -> ( D )
    # Db -> Vl = E              => =
    # ---------------------------------

    def Db(self):
        token = self.get_current_token()

        if token is None:
            return None
        
        if token.token_type == TokenType.IDENTIFIER:
            # Can be either a function definition or a variable assignment
            # Db -> IDENTIFIER Vb+ = E or 
            # Db -> Vl = E
            if self.tokens[self.current_token_index + 1] and (self.tokens[self.current_token_index + 1].token_type == TokenType.IDENTIFIER or self.tokens[self.current_token_index + 1].token_type == TokenType.LEFT_PAREN):
                # This is a function definition
                # Db -> IDENTIFIER Vb+ = E
                self.consume_token()
                self.token_stack.push(Node(f"<ID:{token.lexeme}>", None, None))  # Push IDENTIFIER node
                self.Vb()
                n = 2 # Count the number of Vb and identifier
                token = self.get_current_token()
                while token and token.token_type != TokenType.EQUALS:
                    self.Vb()
                    n += 1
                    token = self.get_current_token()
                if token is None:
                    raise SyntaxError("Expected '=' after variable but reached end of input.")
                elif token.token_type == TokenType.EQUALS:
                    self.consume_token()
                    self.E()
                    print("Db -> IDENTIFIER Vb+ = E")
                    self.build_tree("function_form", n + 1)
                else:
                    raise SyntaxError(f"Expected '=' after variable but got '{token.token_type}' at line {token.line} column {token.column}.")

            else:
                # This is a variable assignment
                # Db -> Vl = E
                self.Vl()
                token = self.get_current_token()
                if token and token.token_type != TokenType.EQUALS:
                    raise SyntaxError(f"Expected '=' after variable but got '{token.token_type}' at line {token.line} column {token.column}.")
                elif token is None:
                    raise SyntaxError("Expected '=' after variable but reached end of input.")
                self.consume_token()
                self.E()
                print("Db -> Vl = E")
                self.build_tree("=", 2)
        
        elif token.token_type == TokenType.LEFT_PAREN:
            # Db -> ( D )
            self.consume_token()
            self.D()
            token = self.get_current_token()
            if token and token.token_type != TokenType.RIGHT_PAREN:
                raise SyntaxError(f"Expected ')' but got '{token.token_type}' at line {token.line} column {token.column}.")
            elif token is None:
                raise SyntaxError("Expected ')' but reached end of input.")
            self.consume_token()
            print("Db -> ( D )")
               
 
    # Variables #######################

    # ---------------------------------
    # Vb -> IDENTIFIER
    # Vb -> ( Vl )
    # Vb -> ( )                 => ()
    # ---------------------------------

    def Vb(self):
        token = self.get_current_token()
        
        if token is None:
            return None
        
        if token.token_type == TokenType.IDENTIFIER:
            # Vb -> IDENTIFIER
            self.consume_token()
            print("Vb -> IDENTIFIER")
            self.token_stack.push(Node(f"<ID:{token.lexeme}>", None, None))  # Push IDENTIFIER node
        elif token.token_type == TokenType.LEFT_PAREN:
            # Vb -> ( Vl ) | ()
            self.consume_token()
            token = self.get_current_token()
            if token and token.token_type == TokenType.RIGHT_PAREN:
                self.consume_token()
                print("Vb -> ( )")
                self.build_tree("()", 0)
            elif token is None:
                raise SyntaxError("Expected ')' after '(' but reached end of input.")
            else:
                self.Vl()
                token = self.get_current_token()
                if token and token.token_type != TokenType.RIGHT_PAREN:
                    raise SyntaxError(f"Expected ')' after variable list but got '{token.token_type}' at line {token.line} column {token.column}.")
                elif token is None:
                    raise SyntaxError("Expected ')' after variable list but reached end of input.")
                self.consume_token()
                print("Vb -> ( Vl )")

    # ---------------------------------
    # Vl -> IDENTIFIER ( , IDENTIFIER )*  => ,
    # ---------------------------------

    def Vl(self):
        token = self.get_current_token()
        
        if token is None:
            return None
        
        if token.token_type == TokenType.IDENTIFIER:
            self.consume_token()
            n = 1
            self.token_stack.push(Node(f"<ID:{token.lexeme}>", None, None))
            print("Vl -> IDENTIFIER")
            token = self.get_current_token()
            while token and token.token_type == TokenType.COMMA:
                self.consume_token()
                token = self.get_current_token()
                if token and token.token_type != TokenType.IDENTIFIER:
                    raise SyntaxError(f"Expected IDENTIFIER after ',' but got '{token.token_type}' at line {token.line} column {token.column}.")
                elif token is None:
                    raise SyntaxError("Expected IDENTIFIER after ',' but reached end of input.")
                self.token_stack.push(Node(f"<ID:{token.lexeme}>", None, None))
                self.consume_token()
                n += 1
                token = self.get_current_token()
            if n > 1:
                self.build_tree(",", n)
                print("Vl -> IDENTIFIER ( , IDENTIFIER )*")
        else:
            raise SyntaxError(f"Unexpected token: {token}")
    

def main():
    # Example usage of the Parser
    tokens = [
        Token(TokenType.LET, "let", 1, 1),
        Token(TokenType.IDENTIFIER, "x", 1, 5),
        Token(TokenType.EQUALS, "=", 1, 6),
        Token(TokenType.INTEGER, "42", 1, 7),
        Token(TokenType.IN, "in", 1, 7),
        Token(TokenType.IDENTIFIER, "x", 1, 10),
        Token(TokenType.PLUS, "+", 1, 11),
        Token(TokenType.INTEGER, "1", 1, 12),
        Token(TokenType.EOF, "", 1, 11)
    ]
    
    parser = Parser(tokens)
    parser.parse()

if __name__ == "__main__":
    main()
        

        


        

            

        






    

