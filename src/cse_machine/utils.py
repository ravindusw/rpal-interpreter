class Environment:
    """
    Represent an environement in the CSE machine.
    An environment maps variable names to their values.
    """
    def __init__(self, id, parent=None):
        """
        Initialize a new environment.

        Args:
            id (int): The unique identifier for the environment.
            parent (Environment, optional): The parent environment. Defaults to None.
        """
        self.bindings = {} # Dictionary to hold variable bindings
        self.parent = parent # Parent environment for scoping
        self.env_id = id # Unique identifier for the environment

    def __repr__(self):
        # return f"Environment(id={self.env_id}, bindings={self.bindings})"
        return f"e_{self.env_id}"
    
    def __str__(self):
        return f"e_{self.env_id}"
    
    def bind(self, name, value):
        """
        Bind a variable name to a value in this environment.
        
        Args:
            name (str): The variable name to bind.
            value: The value to bind to the variable name.
        """
        if name in self.bindings:
            raise ValueError(f"Variable '{name}' is already bound in this environment.")
        self.bindings[name] = value

    def lookup(self, name):
        """
        Look up a variable name in this environment or its parent environments.
        
        Args:
            name (str): The variable name to look up.
        
        Returns:
            The value bound to the variable name.
        """
        if name in self.bindings:
            return self.bindings[name]
        elif self.parent is not None:
            return self.parent.lookup(name)
        else:
            raise NameError(f"Variable '{name}' is not defined.")
        
    def contains(self, name):
        """
        Check if a variable name is bound in this environment or its parent environments.
        
        Args:
            name (str): The variable name to check.
        
        Returns:
            bool: True if the variable is bound, False otherwise.
        """
        if name in self.bindings:
            return True
        elif self.parent is not None:
            return self.parent.contains(name)
        else:
            return False
        
    def print_parent_stack(self):
        """
        Print the parent environment stack for debugging purposes.
        """
        env = self
        stack = []
        while env is not None:
            stack.append(env.env_id)
            env = env.parent
        print("Parent Environment Stack:", " -> ".join(map(str, reversed(stack))))


class Closure:
    """
    Represents a closure in the CSE machine.
    Can be a lambda closure or a eta closure (used in recursive functions).
    """
    def __init__(self, cs_id, params, type, env=None):
        """
        Initialize a new closure.
        
        Args:
            env (Environment): The environment in which the closure was created.
            cs_id (int): The identifier of the control structure that contains the body.
            params (list): The parameters of the closure.
        """
        self.env = env
        self.cs_id = cs_id
        self.params = params
        self.type = type  # Type of the closure ('lambda', 'eta')

    def __str__(self):
        return f"<{self.env.env_id if self.env else None} {self.type} {self.cs_id} {self.params}>"
    
    def __repr__(self):
        return self.__str__()
    

class Tuple:
    """
    Represents a tuple in the CSE machine.
    """
    def __init__(self, values):
        """
        Initialize a new tuple.
        
        Args:
            values (list): The values in the tuple.

        """
        self.values = values

    def __str__(self):
        return f"({', '.join(map(str, self.values))})"
        # return "tau_{self.__len__()}"
    
    def __repr__(self):
        return self.__str__()
    
    def __len__(self):
        """
        Get the length of the tuple.
        
        Returns:
            int: The number of values in the tuple.
        """
        return len(self.values)
    
    def __getitem__(self, index):
        """
        Get an item from the tuple by index.
        
        Args:
            index (int): The index of the item to retrieve.
        
        Returns:
            The value at the specified index.
        """
        return self.values[index] if 0 <= index < len(self.values) else None
    
class BuiltinFunction:
    """
    Represents a built-in function.
    """
    def __init__(self, name, func, arity):
        """
        Initialize a new built-in function.
        
        Args:
            name (str): The name of the built-in function.
            func (callable): The function to be executed.
            arity (int): The number of arguments the function expects.
        """
        self.name = name
        self.func = func
        self.arity = arity

    def __str__(self):
        return f"F_{self.name}"
    
    def __repr__(self):
        return self.__str__()
    
    def __call__(self, *args):
        """
        Call the built-in function with the provided arguments.
        
        Args:
            *args: The arguments to pass to the function.
        
        Returns:
            The result of the function call.
        """
        return self.func(*args)
    
class ControlStructure:
    """
    Represents a control structure in the CSE machine.
    """
    def __init__(self, cs_id, body):
        """
        Initialize a new control structure.
        
        Args:
            cs_id (int | str): The identifier of the control structure. (str for '->' (i.e.conditions))
            body (list): The body of the control structure.
        """
        self.cs_id = cs_id
        self.body = body

    def __str__(self):
        return f"delta_{self.cs_id}({self.body})"
    
    def __repr__(self):
        return self.__str__()
    