# backend/parser.py

import re
from backend.node import Node


def parse_condition(condition):
    # Parse a single condition into a Node
    # Example: 'age > 30' -> Node(type='operand', value='age > 30')
    return Node('operand', value=condition.strip())


def parse_rule(rule_string):
    # Use regex or string splitting to break down the rule into its components.
    rule_string = rule_string.replace('(', '').replace(')', '')  # Remove parentheses for simplicity
    tokens = re.split(r' (AND|OR) ', rule_string)

    if len(tokens) == 1:
        return parse_condition(tokens[0])

    # Create AST with operators and conditions
    left = parse_condition(tokens[0])
    operator = tokens[1]
    right = parse_condition(tokens[2])

    return Node(node_type='operator', left=left, right=right, value=operator)




def create_rule(rule_string):
    # This is a very basic parser, just as an example
    tokens = rule_string.split()

    if len(tokens) == 3:
        # We assume the rule is of the form 'age > 30'
        field, operator, value = tokens
        node = Node(node_type='operand', value=f'{field} {operator} {value}')
        return node
    else:
        raise ValueError("Invalid rule format")


# Test parsing with a sample rule
if __name__ == "__main__":
    rule = "age > 30 AND department = 'Sales'"
    ast = parse_rule(rule)
    print(ast)
