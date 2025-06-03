from src.parser.utils import Node

class Standardizer:
    """
    Standardizer for RPAL Abstract Syntax Tree (AST).
    Transforms the AST to a standard form.
    """

    def __init__(self, ast):
        """
        Initializes the Standardizer with an AST.

        Args: 
            ast (Node): The root node of the AST to be standardized.
        """
        self.ast = ast
        self.standardized_tree = None

    def standardize(self):
        """
        Main entry point for standardization.
        
        Returns:
            Node: The standardized AST.
        """
        if self.ast is None:
            return None
        
        self.standardized_tree = self.standardize_bottom_up(self.ast)
        if self.standardized_tree is None:
            print("Standardization failed: The AST is empty or invalid.")
            return None
        else:
            print("Standardization completed successfully.")
            return self.standardized_tree
    
    def standardize_bottom_up(self, node):
        """
        Travel the AST in bottom up and standardize each node.

        Args:
            node (Node): The root node of the AST.

        Returns:
            Node: The standardized node.
        """
        if node is None:
            return None
        
        if node.left is not None:
            node.left = self.standardize_bottom_up(node.left)
        if node.right is not None:
            node.right = self.standardize_bottom_up(node.right)
        
        return self.standardize_node(node)
    
    def print_standardized_tree(self):
        """
        Prints the standardized tree in a readable format.
        """
        if self.standardized_tree is None:
            print("The standardized tree is empty.")
            return
        
        def print_node(node, prefix=""):
            if node is None:
                return
            print(f"{prefix}{node.value}")
            if node.left is not None:
                print_node(node.left, prefix + ".")
            if node.right is not None:
                print_node(node.right, prefix)
        
        print("Standardized Tree:")
        print_node(self.standardized_tree)

    def get_child(self, node, index):
        """
        Retrieves a child node at a specific index.

        Args:
            node (Node): The parent node.
            index (int): The index of the child node to retrieve.

        Returns:
            Node: The child node at the specified index.
        """
        # Tree is a first-child next-sibling tree
        current_child = node.left
        for _ in range(index):
            if current_child is None:
                return None
            current_child = current_child.right
        return current_child

    def get_all_children(self, node):
        """
        Retrieves all children of the node

        Args:
            node (Node): The parent node.

        Returns:
            list: A list of all child nodes.
        """
        children = []
        current_child = node.left
        while current_child is not None:
            children.append(current_child)
            current_child = current_child.right
        return children
    
    def standardize_node(self, node):
        """
        Standardize a node and its children.
        
        Args:
            node (Node): Node to standardize
            
        Return:
            Node: Standardized node
        """
        if node is None:
            return None
        
        if node.value == 'let':
            return self.standardize_let(node)
        elif node.value == 'where':
            return self.standardize_where(node)
        elif node.value == 'function_form':
            return self.standardize_function_form(node)
        elif node.value == 'lambda':
            return self.standardize_multi_param_function(node)
        elif node.value == 'within':
            return self.standardize_within(node)
        elif node.value == '@':
            return self.standardize_at(node)
        elif node.value == 'and':
            return self.standardize_simultaneous_defs(node)
        elif node.value == 'rec':
            return self.standardize_rec(node)
        else:
            # If the node is not one of the standardizable types, return it as is
            return node

    def standardize_let(self, node):
        """
        Standardize a 'let' node.

        Args:
            node (Node): The 'let' node to standardize.

        Returns:
            Node: The standardized 'let' node.
        """
        # Implement standardization logic for 'let' nodes
        #       let                 gamma
        #       / \                 /   \
        #      =   P    =>      lambda   E
        #     / \               /   \
        #    x   E             x     P

        if node is None or node.left is None or node.left.right is None or node.left.left is None or node.left.left.right is None:
            print("Invalid 'let' node structure")
            return node
        
        if node.value != 'let':
            print("Node is not a 'let' node")
            return node
        
        if node.left.value != '=':
            print("Left child of 'let' node is not an '=' node")
            return node
        
        x_node = node.left.left
        e_node = node.left.left.right
        p_node = node.left.right

        lambda_node = Node('lambda', x_node, e_node)
        gamma_node = Node('gamma', lambda_node, node.right)

        x_node.right = p_node

        return gamma_node
    
    def standardize_where(self, node):
        """
        Standardize a 'where' node.

        Args:
            node (Node): The 'where' node to standardize.

        Returns:
            Node: The standardized 'where' node.
        """
        # Implement standardization logic for 'where' nodes
        #      where                gamma
        #      /  \                 /   \
        #      P   =      =>    lambda   E
        #         / \            /   \
        #        x   E          x     P

        if node is None or node.left is None or node.left.right is None or node.left.right.left is None or node.left.right.left.right is None:
            print("Invalid 'where' node structure")
            return node
        
        if node.value != 'where':
            print("Node is not a 'where' node")
            return node
        
        if node.left.right.value != '=':
            print("Right child of 'where' node is not an '=' node")
            return node
        
        x_node = node.left.right.left
        e_node = node.left.right.left.right
        p_node = node.left

        lambda_node = Node('lambda', x_node, e_node)
        gamma_node = Node('gamma', lambda_node, node.right)

        x_node.right = p_node
        p_node.right = None

        return gamma_node
    
    def standardize_function_form(self, node):
        """
        Standardize a function form node.
        
        Args:
            node (Node): The function form node to standardize.
            
        Returns:
            Node: The standardized function form node.
        """
        # Implement standardization logic for function form nodes
        #       function_form                =
        #      /      |     \               / \
        #     P       V+     E    =>       P   +lambda
        #                                       / \
        #                                       V  .E

        if node is None or node.left is None or node.left.right is None or node.left.right.right is None:
            print("Invalid function form node structure")
            return node
        
        if node.value != 'function_form':
            print("Node is not a 'function_form' node")
            return node
        
        children = self.get_all_children(node)
        
        p_node = children[0]
        e_node = children[-1]
        v_nodes = children[1:-1] 

        last_v_node = v_nodes.pop()
        last_v_node.right = e_node
        lambda_node = Node('lambda', last_v_node, None)

        for v_node in reversed(v_nodes):
            v_node.right = lambda_node
            lambda_node = Node('lambda', v_node, None)

        p_node.right = lambda_node

        eq_node = Node('=', p_node, node.right)
        return eq_node
    
    def standardize_multi_param_function(self, node):
        """
        Standardize a multi-parameter function node.

        Args:
            node (Node): The multi-parameter function node to standardize.

        Returns:
            Node: The standardized multi-parameter function node.
        """
        # Implement standardization logic for multi-parameter function nodes
        #       lambda                 ++lambda
        #      /      \               /       \
        #     V++       E    =>      V         .E

        if node is None or node.left is None or node.left.right is None or node.left.right.right is None:
            print("Invalid multi-parameter function node structure")
            return node
        
        if node.value != 'lambda':
            print("Node is not a 'multi_param_function' node")
            return node
        
        children = self.get_all_children(node)
        
        e_node = children[-1]
        v_nodes = children[:-1]

        last_v_node = v_nodes.pop()
        last_v_node.right = e_node
        lambda_node = Node('lambda', last_v_node, None)

        for v_node in reversed(v_nodes):
            v_node.right = lambda_node
            lambda_node = Node('lambda', v_node, None)

        lambda_node.right = node.right  # Attach the right child of the original node
        return lambda_node
    
    def standardize_within(self, node):
        """
        Standardize a 'within' node.

        Args:
            node (Node): The 'within' node to standardize.

        Returns:
            Node: The standardized 'within' node.
        """
        # Implement standardization logic for 'within' nodes
        #       within                      =
        #      /      \                    / \
        #     =        =      =>          x2  gamma
        #    / \      / \                    /     \
        #   x1  E1   x2  E2               lambda    E1
        #                                 /    \
        #                                x1    E2

        if (node is None or node.left is None or node.left.right is None 
            or node.left.left is None or node.left.left.right is None or
            node.left.right.left is None or node.left.right.left.right is None):
            print("Invalid 'within' node structure")
            return node
        
        if node.value != 'within':
            print("Node is not a 'within' node")
            return node
        
        if node.left.value != '=' or node.left.right.value != '=':
            print("Children of 'within' node are not '=' nodes")
            return node
        
        x1_node = node.left.left
        e1_node = node.left.left.right
        x2_node = node.left.right.left
        e2_node = node.left.right.left.right

        x1_node.right = e2_node
        lambda_node = Node('lambda', x1_node, e1_node)
        gamma_node = Node('gamma', lambda_node, None)
        x2_node.right = gamma_node

        eq_node = Node('=', x2_node, node.right)
        return eq_node
    
    def standardize_at(self, node):
        """
        Standardize an '@' node.

        Args:
            node (Node): The '@' node to standardize.

        Returns:
            Node: The standardized '@' node.
        """
        # Implement standardization logic for '@' nodes
        #        @                   gamma
        #      / | \                 /   \
        #    E1  N  E2     =>    gamma    E2
        #                        /   \
        #                        N    E1

        if node is None or node.left is None or node.left.right is None or node.left.right.right is None:
            print("Invalid '@' node structure")
            return node
        
        if node.value != '@':
            print("Node is not an '@' node")
            return node
        
        e1_node = node.left
        n_node = node.left.right
        e2_node = node.left.right.right

        n_node.right = e1_node
        gamma_node = Node('gamma', n_node, e2_node)
        gamma_node = Node('gamma', gamma_node, node.right)

        e1_node.right = None

        return gamma_node
    
    def standardize_simultaneous_defs(self, node):
        """
        Standardize a simultaneous definitions node.

        Args:
            node (Node): The simultaneous definitions node to standardize.

        Returns:
            Node: The standardized simultaneous definitions node.
        """
        # Implement standardization logic for simultaneous definitions nodes
        #       and                   =
        #        |                   / \
        #       =++        =>       ,   tau
        #       / \                 |    |         
        #      x   E               x++  E++           

        if (node is None or node.left is None or node.left.right is None 
           or node.left.left is None or node.left.left.right is None
           or node.left.right.left is None or node.left.right.left.right is None):
            print("Invalid simultaneous definitions node structure")
            return node
        
        if node.value != 'and':
            print("Node is not a 'simultaneous_defs' node")
            return node
        
        children = self.get_all_children(node)

        x_nodes = []
        e_nodes = []

        for child in children:
            if child.value != '=':
                print("Child of 'and' node is not an '=' node")
                return node     
            x_nodes.append(child.left)
            e_nodes.append(child.left.right)

        for i in range(len(x_nodes) - 1):
            x_nodes[i].right = x_nodes[i + 1]
            e_nodes[i].right = e_nodes[i + 1]

        x_nodes[-1].right = None

        tau_node = Node('tau', e_nodes[0], None)
        comma_node = Node(',', x_nodes[0], tau_node)
        eq_node = Node('=', comma_node, node.right)
        return eq_node
    
    def standardize_rec(self, node):
        """
        Standardize a 'rec' node.

        Args:
            node (Node): The 'rec' node to standardize.

        Returns:
            Node: The standardized 'rec' node.
        """
        # Implement standardization logic for 'rec' nodes
        #       rec                =
        #        |                / \
        #        =      =>       x   gamma
        #       / \                  /   \
        #      x   E                Y     lambda
        #                                 /    \
        #                                x      E

        if node is None or node.left is None or node.left.left is None or node.left.left.right is None:
            print("Invalid 'rec' node structure")
            return node
        
        if node.value != 'rec':
            print("Node is not a 'rec' node")
            return node
        
        if node.left.value != '=':
            print("Left child of 'rec' node is not an '=' node")
            return node
        
        x_node = node.left.left
        e_node = node.left.left.right

        x_node.right = e_node
        lambda_node = Node('lambda', x_node, None)
        y_node = Node('Y', None, lambda_node)
        gamma_node = Node('gamma', y_node, None)

        x_node_copy = Node(x_node.value, None, None)
        x_node_copy.right = gamma_node
        
        eq_node = Node('=', x_node_copy, node.right)
        return eq_node
        



def main():
    pass

if __name__ == "__main__":
    main()
