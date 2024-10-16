# backend/combine_rules.py

from backend.node import Node


def combine_rules(rule_asts, operator):
    if len(rule_asts) < 2:
        raise ValueError("Need at least two rules to combine")

    combined = rule_asts[0]
    for rule in rule_asts[1:]:
        combined = Node(node_type='operator', left=combined, right=rule, value=operator)
    return combined


# Example usage:
if __name__ == "__main__":
    from backend.parser import parse_rule

    rule1 = parse_rule("age > 30 AND department = 'Sales'")
    rule2 = parse_rule("experience > 5 OR salary > 50000")

    combined_ast = combine_rules([rule1, rule2])
    print(combined_ast)
