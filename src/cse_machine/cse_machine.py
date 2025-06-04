from .utils import Environment, Tuple, Closure, BuiltinFunction, ControlStructure
from src.parser.utils import Node
import os

class CSEMachine:
    """
    Control-Stack-Environment Machine (CSE Machine) for evaluating RPAL programs.
    """
    def __init__(self, st):
        """
        Initialize the CSE machine.
        """
        self.env_stack = [Environment(0)]  # Start with the initial environment
        self.control_stack = []
        self.value_stack = []
        self.control_structures = {}
        # self.current_env = Environment(0)
        self.last_env_id = 0
        self.last_cs_id = 1

        self.initiate(st) # Set up the initial environment and built-in functions

    def initiate(self, st):
        """
        Set up the initial environment and built-in functions.

        Args:
            st (Node): The root node of the standardized tree.
        """
        if st is None:
            return
        
        self.setup_builtin_functions()
        self.setup_control_structures(st)
        self.control_stack.append(self.env_stack[-1])  # Start with the initial environment on the control stack
        self.control_stack += (self.control_structures[0].body)  # Start with the main control structure
        self.value_stack.append(self.env_stack[-1])  # Push the initial environment onto the value stack


    # Builtin Functions ###############
    
    def setup_builtin_functions(self):
        """Set up built-in functions in the initial environment."""
        builtins = {
            'Print': BuiltinFunction('Print', self._builtin_print, -1),  # -1 indicates variable arity
            'Isinteger': BuiltinFunction('Isinteger', self._builtin_isinteger, 1),
            'Istruthvalue': BuiltinFunction('Istruthvalue', self._builtin_istruthvalue, 1),
            'Isstring': BuiltinFunction('Isstring', self._builtin_isstring, 1),
            'Istuple': BuiltinFunction('Istuple', self._builtin_istuple, 1),
            'Isfunction': BuiltinFunction('Isfunction', self._builtin_isfunction, 1),
            'Isdummy': BuiltinFunction('Isdummy', self._builtin_isdummy, 1),
            'Stem': BuiltinFunction('Stem', self._builtin_stem, 1),
            'Stern': BuiltinFunction('Stern', self._builtin_stern, 1),
            'Conc': BuiltinFunction('Conc', self._builtin_conc, 2),
            'ItoS': BuiltinFunction('ItoS', self._builtin_itos, 1),
            'Order': BuiltinFunction('Order', self._builtin_order, 1),
            'Null': BuiltinFunction('Null', self._builtin_null, 1)
        }
        
        for name, func in builtins.items():
            self.env_stack[-1].bind(name, func)
    
    def _builtin_print(self, value):
        """Built-in Print function."""
        # Pass for now due to submission guidelines.
        # Uncomment print statements within this function otherwise

        if value is None:
            pass
            # print("nil")
        elif isinstance(value, Tuple):
            pass
            # print(f"({', '.join(str(v) for v in value.values)})")
        else:
            pass
            # print(value)
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
        if isinstance(value, str) and len(value) > 0:
            if len(value) == 1:
                return ''  # Return empty string, not None
            else:
                return value[1:]  # Return substring from index 1
        return ''   # Return empty string if no rest exists
    
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
        
        self.generate_control_structure(current, current_cs)
        self.control_structures[0] = ControlStructure(0, current_cs)

    def generate_control_structure(self, node, cs):
        
        if node is None:
            return
        
        if node.value == 'lambda':

            if node.left.value == ',':
                # Lambda with multiple parameters
                params = []
                current = node.left.left
                while current:
                    params.append(current.value)
                    current = current.right
                # print("params: ", params)
                cs.append(Closure(self.last_cs_id, params, 'lambda', None))
            else:
                cs.append(Closure(self.last_cs_id, [node.left.value], 'lambda', None))
            
            lambda_cs_id = self.last_cs_id
            self.last_cs_id += 1
            new_cs = []
            self.generate_control_structure(node.left.right, new_cs)
            self.control_structures[lambda_cs_id] = ControlStructure(lambda_cs_id, new_cs)
            
            self.generate_control_structure(node.right, cs)
        
        elif node.value == '->':
            # B -> E1 | E2  becomes delta_true, delta_false, beta, B
            condition = node.left
            true_branch = node.left.right
            false_branch = node.left.right.right
            node.left.right.right = None  # Disconnect the false part of the condition
            node.left.right = None  # Disconnect the true part of the condition

            # B
            condition_cs = []
            self.generate_control_structure(condition, condition_cs)
            
            # delta_true
            true_cs = []
            self.generate_control_structure(true_branch, true_cs)

            # delta_false
            false_cs = []
            self.generate_control_structure(false_branch, false_cs)

            self.control_structures[self.last_cs_id] = ControlStructure(self.last_cs_id, true_cs)
            cs.append(f"delta_{self.last_cs_id}_t")
            self.last_cs_id += 1
            self.control_structures[self.last_cs_id] = ControlStructure(self.last_cs_id, false_cs)
            cs.append(f"delta_{self.last_cs_id}_f")
            self.last_cs_id += 1

            cs.append('beta')
            cs += condition_cs
            
            self.generate_control_structure(node.right, cs)
        
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
            self.generate_control_structure(node.left, cs)
            self.generate_control_structure(node.right, cs)

    
    # Evaluating expressions ##########

    def evaluate(self):
        """
        Main entry point of the CSE machine.
        Evaluate the RPAL program using the CSE machine.
        This method will repeatedly apply rules until no more rules can be applied.
        """
        # Create a folder to store outputs if not exists
        output_dir = 'src/cse_machine/csem_output'
        os.makedirs(output_dir, exist_ok=True)

        # Clear the output files before starting evaluation
        with open('src/cse_machine/csem_output/control_stack.txt', 'w') as f:
            f.write('')
        with open('src/cse_machine/csem_output/value_stack.txt', 'w') as f:
            f.write('')

        if self.control_stack is None or len(self.control_stack) == 0:
            print("Control stack is empty. Nothing to evaluate.")
            return None
            
        while self.control_stack:
            self.apply_rule()
            
            # Write current content to files
            with open('src/cse_machine/csem_output/control_stack.txt', 'a') as f:
                f.write(', '.join(str(item) for item in self.control_stack) + '\n\n')
            with open('src/cse_machine/csem_output/value_stack.txt', 'a') as f:
                f.write(', '.join(str(item) for item in self.value_stack) + '\n\n')
            
            # print(self.control_structures)
            # self.env_stack[-1].print_parent_stack()
            # print("Env Stack: ", self.env_stack)
        
        if len(self.value_stack) != 1:
            raise ValueError("Evaluation did not result in a single value on the value stack.")
        
        # result = self.value_stack[-1]
        # if isinstance(result, Tuple):
        #     return f"({', '.join(str(v) for v in result.values)})"

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
            value = self.env_stack[-1].lookup(name)
            self.value_stack.append(value)
            self.control_stack.pop()

        elif control_stack_top and isinstance(control_stack_top, str) and control_stack_top.startswith('<INT:'):
            int_value = int(control_stack_top[5:-1])
            self.value_stack.append(int_value)
            self.control_stack.pop()

        elif control_stack_top and isinstance(control_stack_top, str) and control_stack_top.startswith('<STR:'):
            str_value = control_stack_top[6:-2]
            self.value_stack.append(str_value)
            self.control_stack.pop()
        
        elif control_stack_top and isinstance(control_stack_top, str) and (control_stack_top == 'true'):
            self.value_stack.append(True)
            self.control_stack.pop()
        
        elif control_stack_top and isinstance(control_stack_top, str) and (control_stack_top == 'false'):
            self.value_stack.append(False)
            self.control_stack.pop()
        
        elif control_stack_top and isinstance(control_stack_top, bool):
            self.value_stack.append(control_stack_top)
            self.control_stack.pop()
        
        elif control_stack_top and isinstance(control_stack_top, str) and control_stack_top == 'nil':
            self.value_stack.append('nil')
            self.control_stack.pop()

        elif control_stack_top and isinstance(control_stack_top, str) and control_stack_top == 'Y_star':
            self.value_stack.append('Y_star')
            self.control_stack.pop()

        elif control_stack_top and isinstance(control_stack_top, str) and control_stack_top == 'dummy':
            self.value_stack.append('dummy')
            self.control_stack.pop()

        # Rule 2 - Stack lambda
        elif control_stack_top and isinstance(control_stack_top, Closure):
            control_stack_top.env = self.env_stack[-1]
            self.value_stack.append(control_stack_top)
            self.control_stack.pop()

        # Rule 3 - Apply (Ope)Rator
        elif (control_stack_top and isinstance(control_stack_top, str) and control_stack_top == 'gamma' 
            and value_stack_top and isinstance(value_stack_top, BuiltinFunction)):
            
            self.control_stack.pop()  # Pop 'gamma'
            builtin_function = value_stack_top
            self.value_stack.pop()  # Pop the BuiltinFunction from the value stack
            args = []

            if builtin_function.arity == -1:
                # Variable arity function, pop all arguments until we hit a non-argument
                while self.value_stack and isinstance(self.value_stack[-1], (int, str, bool, Tuple, Closure)):
                    args.append(self.value_stack.pop())
            else:
                for _ in range(builtin_function.arity):
                    if not self.value_stack:
                        raise ValueError(f"(Rule 3) Not enough arguments for function '{builtin_function.name}'. Expected {builtin_function.arity}, found {len(args)}.")
                    args.append(self.value_stack.pop())

            result = builtin_function.func(*args)
            self.value_stack.append(result)

        # Rule 4 (and 11) - Apply lambda
        elif (control_stack_top and isinstance(control_stack_top, str) and control_stack_top == 'gamma' 
            and value_stack_top and isinstance(value_stack_top, Closure) and value_stack_top.type == 'lambda'):
            
            closure = value_stack_top
            self.value_stack.pop()
            
            # Preparing new environment
            next_env_id = self.last_env_id + 1
            self.last_env_id += 1
            new_env = Environment(next_env_id, closure.env)
            
            params = closure.params

            if isinstance(self.value_stack[-1], Tuple):
                # If the last value on the stack is a tuple, unpack it
                t = self.value_stack.pop()
                tuple_values = t.values

                if len(params) == 1:
                    # If there's only one parameter, bind the entire tuple
                    param = params[0][4:-1]
                    new_env.bind(param, t)

                elif len(tuple_values) != len(params):
                    raise ValueError(f"(Rule 4) Tuple length {len(tuple_values)} does not match number of parameters {len(params)}.")
                
                else:
                    for i in range(len(tuple_values)):
                        param = params[i][4:-1]  # Extract the variable name from <ID:x>
                        new_env.bind(param, tuple_values[i])

            else:
                for i in range(len(params)):
                    if i < len(self.value_stack):
                        # Param is in the format of <ID:x>
                        param = params[i][4:-1]  # Extract the variable name from <ID:x>
                        new_env.bind(param, self.value_stack[-1])
                        self.value_stack.pop()

            self.env_stack.append(new_env)

            # Preparin control stack
            self.control_stack.pop() # Pop the 'gamma'
            self.control_stack.append(self.env_stack[-1])
            self.control_stack += self.control_structures[closure.cs_id].body

            self.value_stack.append(self.env_stack[-1])

        # Rule 5 - Exit environment
        elif control_stack_top and isinstance(control_stack_top, Environment):
            # self.current_env = control_stack_top.parent
            self.control_stack.pop()
            self.env_stack.pop()
            
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
            
            elif operator in ('gr', 'ge', 'ls', 'le', '>', '>=', '<', '<='):
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
            
            elif operator in ('eq', 'ne'):
                if operator == 'eq':
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
                if not (isinstance(left, Tuple) or (isinstance(left, str) and left == 'nil')) or not isinstance(right, (int, str)):
                    raise TypeError(f"(Rule 6) Expected a tuple and a string or number for operator '{operator}'.")
                
                if isinstance(left, str) and left == 'nil':
                    result = Tuple([right])

                else:
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
        elif control_stack_top and isinstance(control_stack_top, str) and control_stack_top == 'beta':
            self.control_stack.pop() # Pop 'beta'
            value = self.value_stack.pop()

            if value is None:
                raise ValueError(f"(Rule 8) Expected a boolean value for conditional evaluation, got {value}.")
            elif value == True or value == 'true':
                self.control_stack.pop() # Pop the id of false constrol structure
                true_cs_id = self.control_stack.pop() # Pop the id of true control structure
                true_cs_id = int(true_cs_id[6:-2]) # Extract the id from 'delta_<id>_t'
                self.control_stack += self.control_structures[true_cs_id].body
            elif value == False or value == 'false':
                false_cs_id = self.control_stack.pop() # Pop the id of false control structure
                false_cs_id = int(false_cs_id[6:-2]) # Extract the id from 'delta_<id>_f'
                self.control_stack.pop() # Pop the id of true constrol structure
                self.control_stack += self.control_structures[false_cs_id].body
            else:
                raise ValueError(f"(Rule 8) Unexpected error occured while evaluatind conditional.")

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
            index = self.value_stack.pop() - 1 # Convert to 0-based index

            if index < 0 or index >= len(tuple.values):
                raise IndexError(f"(Rule 10) Tuple index out of range: {index} for tuple of length {len(tuple.values)}.")
            
            result = tuple.values[index]
            self.value_stack.append(result)

        # Rule 11 - n-ary functions params handling
        # Already done under Rule - 4

        # Rule 12 - Applying Y (Related to recursion)
        elif (control_stack_top and isinstance(control_stack_top, str) and control_stack_top == 'gamma'
              and value_stack_top and isinstance(value_stack_top, str) and value_stack_top == 'Y_star'):
            self.control_stack.pop() # Pops 'gamma'
            self.value_stack.pop()   # Pops 'Y_star'

            if isinstance(self.value_stack[-1], Closure):
                closure = self.value_stack.pop()
                eta = Closure(closure.cs_id, closure.params, 'eta', closure.env)
                self.value_stack.append(eta)
            else:
                raise ValueError("(Rule 12) Expected a lambda closure on the value stack for Y application.")

        # Rule 13 - Appplying F to YF (Related to recursion)
        elif (control_stack_top and isinstance(control_stack_top, str) and control_stack_top == 'gamma'
              and value_stack_top and isinstance(value_stack_top, Closure) and value_stack_top.type == 'eta'):
            self.control_stack.append('gamma') # Put another 'gamma'
            eta = value_stack_top
            lambda_ = Closure(eta.cs_id, eta.params, 'lambda', eta.env)
            self.value_stack.append(lambda_)

        else:
            raise ValueError(f"Control stack has {control_stack_top}. No CSE Rule to handle this.")
        


def main():
    pass

if __name__ == "__main__":
    main()