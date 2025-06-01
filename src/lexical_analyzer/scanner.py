class Scanner:
    """
    Character-level scanner that reads input and provides functionality
    for examining and consuming characters.
    """

    def __init__(self, source):
        """
        Initialize scanner with source code

        Args:
            source: The RPAL source code as a string
        """
        self.source = source
        self.current_pos = 0
        self.line = 1
        self.column = 1
        self.current_char = self.source[self.current_pos] if self.source and len(self.source) > 0 else None

    def is_at_end(self):
        """Check if reached the end of the source code."""
        return self.current_pos >= len(self.source)
    
    def advance(self):
        """Consume the current character and return it."""
        if self.is_at_end():
            return None
        
        char = self.current_char
        self.current_pos += 1

        # Update line and column numbers
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

        # Update the current character
        if self.current_pos < len(self.source):
            self.current_char = self.source[self.current_pos]
        else:
            self.current_char = None

        return char
    
    def peek(self):
        """Look at the current character without consuming it."""
        if self.is_at_end():
            return None
        return self.current_char
    
    def peek_next(self):
        """Look at the next character without consuming it."""
        if self.current_pos + 1 >= len(self.source):
            return None
        return self.source[self.current_pos + 1]
    
    def consume(self, expected_char):
        """
        Consume the expected character if it matches the current character.

        Args:
            expected_char: The character to consume.

        Returns:
            bool: True if the character was consumed, False otherwise.
        """
        if self.peek() == expected_char:
            self.advance()
            return True
        return False
    
    def current_position(self):
        """
        Get the current position in the source code.

        Returns:
            tuple: (line, column) of the current position.
        """
        return (self.line, self.column)