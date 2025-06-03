from .utils import Environment, Tuple, Closure, BuiltinFunction, ControlStructure
from src.parser.utils import Node
import sys

class CSEMachine:
    """
    Control-Stack-Environment Machine (CSE Machine) for evaluating RPAL programs.
    """
    def __init__(self):
        """
        Initialize the CSE machine.
        """
        # self.env_stack = []
        self.control_stack = []
        self.value_stack = []
        self.control_structures = {}
        self.current_env = Environment(0)

        self.setup_builtin_functions()
        self.setup_control_structures()

    
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

        # Rule 2 - Stack lambda
        if control_stack_top and isinstance(control_stack_top, Closure):
            control_stack_top.env = self.current_env
            self.value_stack.append()
            


    


        








    
