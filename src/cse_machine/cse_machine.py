from .utils import Environment, Tuple, Closure, BuiltinFunction, ControlStructure
from src.parser.utils import Node
import sys

class CSEMachine:
    """
    Control-Stack-Environment Machine (CSE Machine) for evaluating RPAL programs.
    """
    def __init__(self, st):
        """
        Initialize the CSE machine.
        """
        self.control_stack = []
        self.value_stack = []
        self.control_structures = {}
        self.current_env = Environment(0)
        self.last_env_id = 0

        self.initiate(st) # Set up the initial environment and built-in functions

    def initiate(self, st):
        self.setup_builtin_functions()
        self.setup_control_structures(st)
        self.control_stack.append(self.current_env)
        self.control_stack += (self.control_structures[0].body)  # Start with the main control structure
        print(self.control_stack)
        self.value_stack.append(self.current_env)


    # Builtin Functions ###############
    
    def setup_builtin_functions(self):
        """Set up built-in functions in the initial environment."""
        builtins = {
            'Print': BuiltinFunction('Print', self._builtin_print),
            'Isinteger': BuiltinFunction('Isinteger', self._builtin_isinteger),
            'Istruthvalue': BuiltinFunction('Istruthvalue', self._builtin_istruthvalue),
            'Isstring': BuiltinFunction('Isstring', self._builtin_isstring),
            'Istuple': BuiltinFunction('Istuple', self._builtin_istuple),
            'Isfunction': BuiltinFunction('Isfunction', self._builtin_isfunction),
            'Isdummy': BuiltinFunction('Isdummy', self._builtin_isdummy),
            'Stem': BuiltinFunction('Stem', self._builtin_stem),
            'Stern': BuiltinFunction('Stern', self._builtin_stern),
            'Conc': BuiltinFunction('Conc', self._builtin_conc),
            'ItoS': BuiltinFunction('ItoS', self._builtin_itos),
            'Order': BuiltinFunction('Order', self._builtin_order),
            'Null': BuiltinFunction('Null', self._builtin_null),
        }
        
        for name, func in builtins.items():
            self.current_env.bind(name, func)
    
    def _builtin_print(self, value):
        """Built-in Print function."""
        if value is None:
            print("nil")
        else:
            print(value)
        return value  # Print returns the value it prints
    
    def _builtin_isinteger(self, value):
        """Built-in Isinteger function."""
        return isinstance(value, int)
    
    def _builtin_istruthvalue(self, value):
        """Built-in Istruthvalue function."""
        return isinstance(value, bool)
    
    def _builtin_isstring(self, value):
        """Built-in Isstring function."""
        return isinstance(value, str)
    
    def _builtin_istuple(self, value):
        """Built-in Istuple function."""
        return isinstance(value, Tuple)
    
    def _builtin_isfunction(self, value):
        """Built-in Isfunction function."""
        return isinstance(value, (Closure, BuiltinFunction))
    
    def _builtin_isdummy(self, value):
        """Built-in Isdummy function."""
        return value == 'dummy'
    
    def _builtin_stem(self, value):
        """Built-in Stem function (first element of string)."""
        if isinstance(value, str) and len(value) > 0:
            return value[0]
        else:
            return None
    
    def _builtin_stern(self, value):
        """Built-in Stern function (rest of string)."""
        if isinstance(value, str) and len(value) > 1:
            return value[1:]
        else:
            return None
    
    def _builtin_conc(self, s, t):
        """Built-in Conc function (concatenation)."""
        if isinstance(s, str) and isinstance(t, str):
            return s + t
        else:
            raise TypeError("Conc expects two strings")
    
    def _builtin_itos(self, value):
        """Built-in ItoS function (integer to string)."""
        if isinstance(value, int):
            return str(value)
        else:
            raise TypeError("ItoS expects an integer")
    
    def _builtin_order(self, value):
        """Built-in Order function (length of tuple)."""
        if isinstance(value, Tuple):
            return len(value)
        else:
            return 0
    
    def _builtin_null(self, value):
        """Built-in Null function (check if empty)."""
        if isinstance(value, Tuple):
            return len(value) == 0
        elif value is None:
            return True
        else:
            return False

    
    # Control structures ##############

    def setup_control_structures(self, st):
        """
        Travese the Standardized tree and set up control structures.
        
        Args:
            st (Node): The root node of the standardized tree.
        """
        if st is None:
            return
        
        current_cs = []
        current = st
        
        self.generate_control_structure(current, 0, current_cs)
        self.control_structures[0] = ControlStructure(0, current_cs)

    def generate_control_structure(self, node, cs_id, cs):
        
        if node is None:
            return
        
        if node.value == 'lambda':
            cs.append(Closure(cs_id + 1, [node.left.value], 'lambda', None))
            new_cs = []
            self.generate_control_structure(node.left.right, cs_id + 1, new_cs)
            self.control_structures[cs_id + 1] = ControlStructure(cs_id + 1, new_cs)
            
            if node.right and node.right.value != 'lambda':
                self.generate_control_structure(node.right, cs_id, cs)
            else:
                self.generate_control_structure(node.right, cs_id + 1, cs)
        
        else:
            if node.value == 'tau':
                num_children = 0
                child = node.left
                while child:
                    num_children += 1
                    child = child.right
                cs.append(f"tau_{num_children}")
            else:
                cs.append(node.value)
            self.generate_control_structure(node.left, cs_id, cs)
            self.generate_control_structure(node.right, cs_id, cs)

    
    # Evaluating expressions ##########

    def evaluate(self):
        """
        Evaluate the RPAL program using the CSE machine.
        This method will repeatedly apply rules until no more rules can be applied.
        """
        # Clear the output files before starting evaluation
        with open('src/cse_machine/csem_output/control.txt', 'w') as f:
            f.write('')
        with open('src/cse_machine/csem_output/stack.txt', 'w') as f:
            f.write('')
            
        while self.control_stack:
            self.apply_rule()
            
            # Write current content to files
            with open('src/cse_machine/csem_output/control.txt', 'a') as f:
                f.write(', '.join(str(item) for item in self.control_stack) + '\n\n')
            with open('src/cse_machine/csem_output/stack.txt', 'a') as f:
                f.write(', '.join(str(item) for item in self.value_stack) + '\n\n')
        
        if len(self.value_stack) != 1:
            raise ValueError("Evaluation did not result in a single value on the value stack.")
        
        result = self.value_stack[-1]
        if isinstance(result, Tuple):
            return f"({', '.join(str(v) for v in result.values)})"

        return self.value_stack.pop()

    # CSE Rules #######################

    def apply_rule(self):
        """
        Apply the matching rule considering control stack, value stack, and environment
        """

        control_stack_top = self.control_stack[-1] if self.control_stack else None
        value_stack_top = self.value_stack[-1] if self.value_stack else None
        
        # Rule 1 - Stack a name
        if control_stack_top and isinstance(control_stack_top, str) and control_stack_top.startswith('<ID:'):
            name = control_stack_top[4:-1]
            value = self.current_env.lookup(name)
            self.value_stack.append(value)
            self.control_stack.pop()

        elif control_stack_top and isinstance(control_stack_top, str) and control_stack_top.startswith('<INT:'):
            int_value = int(control_stack_top[5:-1])
            self.value_stack.append(int_value)
            self.control_stack.pop()

        elif control_stack_top and isinstance(control_stack_top, str) and control_stack_top.startswith('<STR:'):
            str_value = control_stack_top[5:-1]
            self.value_stack.append(str_value)
            self.control_stack.pop()

        # Rule 2 - Stack lambda
        elif control_stack_top and isinstance(control_stack_top, Closure):
            control_stack_top.env = self.current_env
            self.value_stack.append(control_stack_top)
            self.control_stack.pop()

        # Rule 3 - Apply (Ope)Rator
        elif control_stack_top and isinstance(control_stack_top, BuiltinFunction):
            # Implement later
            pass

        # Rule 4 (and 11) - Apply lambda
        elif (control_stack_top and isinstance(control_stack_top, str) and control_stack_top == 'gamma' 
            and value_stack_top and isinstance(value_stack_top, Closure)):
            
            closure = value_stack_top
            self.value_stack.pop()
            
            # Preparing new environment
            next_env_id = self.last_env_id + 1
            new_env = Environment(next_env_id, self.current_env)
            
            params = closure.params
            for i in range(len(params)):
                if i < len(self.value_stack):
                    # Param is in the format of <ID:x>
                    param = params[i][4:-1]  # Extract the variable name from <ID:x>
                    print(f"Binding parameter '{param}' to value '{self.value_stack[-1]}' in new environment.")
                    new_env.bind(param, self.value_stack[-1])
                    self.value_stack.pop()

            self.current_env = new_env

            # Preparin control stack
            self.control_stack.pop() # Pop the 'gamma'
            self.control_stack.append(self.current_env)
            self.control_stack += self.control_structures[closure.cs_id].body

            self.value_stack.append(self.current_env)

        # Rule 5 - Exit environment
        elif control_stack_top and isinstance(control_stack_top, Environment):
            self.current_env = control_stack_top.parent
            self.control_stack.pop()
            
            if isinstance(self.value_stack[-2], Environment):
                self.value_stack.pop(-2)
            else:
                raise ValueError("(Rule 5) Expected an environment on the value stack.")
            
        # Rule 6 - binary operations
        elif control_stack_top and control_stack_top in ('gr', 'ge', 'ls', 'le', 'eq', 'ne', '>', '>=', '<', '<=', '+', '-', '*', '/', '**', '&', 'or', 'aug'):
            operator = control_stack_top
            self.control_stack.pop()

            if len(self.value_stack) < 2:
                raise ValueError(f"(Rule 6) Not enough values on the value stack for operator '{operator}'.")
            
            left = self.value_stack.pop()
            right = self.value_stack.pop()

            if operator in ('+', '-', '*', '/', '**'):
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise TypeError(f"(Rule 6) Expected numeric values for operator '{operator}'.")
                if operator == '+':
                    result = left + right
                elif operator == '-':
                    result = left - right
                elif operator == '*':
                    result = left * right
                elif operator == '/':
                    result = left / right
                elif operator == '**':
                    result = left ** right
            
            elif operator in ('gr', 'ge', 'ls', 'le', 'eq', 'ne', '>', '>=', '<', '<='):
                if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
                    raise TypeError(f"(Rule 6) Expected numeric values for operator '{operator}'.")
                if operator == 'gr' or operator == '>':
                    result = left > right
                elif operator == 'ge' or operator == '>=':
                    result = left >= right
                elif operator == 'ls' or operator == '<':
                    result = left < right
                elif operator == 'le' or operator == '<=':
                    result = left <= right
                elif operator == 'eq':
                    result = left == right
                elif operator == 'ne':
                    result = left != right

            elif operator in ('&', 'or'):
                if not (isinstance(left, bool) or left == 'true' or left == 'false') or not (isinstance(right, bool) or right == 'true' or right == 'false'):
                    raise TypeError(f"(Rule 6) Expected boolean values for operator '{operator}'.")
                if operator == '&':
                    result = left and right
                elif operator == 'or':
                    result = left or right

            elif operator == 'aug':
                if not isinstance(left, Tuple) or not isinstance(right, (int, str)):
                    raise TypeError(f"(Rule 6) Expected a tuple and a string or number for operator '{operator}'.")
                
                left.values.append(right)
                result = left
            
            else:
                raise ValueError(f"(Rule 6) Unknown operator '{operator}'.")
            
            self.value_stack.append(result)

        # Rule 7 - Unary operations
        elif control_stack_top and control_stack_top in ('not', 'neg'):
            operator = control_stack_top
            self.control_stack.pop()

            if len(self.value_stack) < 1:
                raise ValueError(f"(Rule 7) Not enough values on the value stack for operator '{operator}'.")

            value = self.value_stack.pop()

            if operator == 'not':
                if not (isinstance(value, bool) or value == 'true' or value == 'false'):
                    raise TypeError(f"(Rule 7) Expected a boolean value for operator '{operator}'.")
                result = not value
            
            elif operator == 'neg':
                if not isinstance(value, (int, float)):
                    raise TypeError(f"(Rule 7) Expected a numeric value for operator '{operator}'.")
                result = -value
            
            else:
                raise ValueError(f"(Rule 7) Unknown operator '{operator}'.")

            self.value_stack.append(result)

        # Rule 8 - Conditionals
        # Will implement later

        # Rule 9 - Tuple formation
        elif control_stack_top and isinstance(control_stack_top, str) and control_stack_top.startswith('tau_'):
            num_children = int(control_stack_top[4:])
            self.control_stack.pop()

            if len(self.value_stack) < num_children:
                raise ValueError(f"(Rule 9) Not enough values on the value stack for tuple formation. Expected {num_children}, found {len(self.value_stack)}.")

            values = [self.value_stack.pop() for _ in range(num_children)]
            new_tuple = Tuple(values)
            self.value_stack.append(new_tuple)

        # Rule 10 - Tuple access
        elif (control_stack_top and isinstance(control_stack_top, str) and control_stack_top == 'gamma'
            and isinstance(self.value_stack[-1], Tuple) and isinstance(self.value_stack[-2], int)):
            
            self.control_stack.pop()
            tuple = self.value_stack.pop()
            index = self.value_stack.pop()

            if index < 0 or index >= len(tuple.values):
                raise IndexError(f"(Rule 10) Tuple index out of range: {index} for tuple of length {len(tuple.values)}.")
            
            result = tuple.values[index]
            self.value_stack.append(result)

        # Rule 11 - n-ary functions params handling
        # Already done under Rule - 4
        # Need to verify later

        # Rule 12 - Applying Y (Related to recursion)
        # Will implement later

        # Rule 13 - Appplying F to YF (Related to recursion)
        # Will implement later

                
        







            
            


    


        








    
