# backend/evaluator.py

def evaluate_rule(ast, data):
    # If it's an operand, compare the value with data
    if ast.type == 'operand':
        field, operator, value = ast.value.split()
        if operator == '>':
            return data[field] > int(value)
        elif operator == '<':
            return data[field] < int(value)
        elif operator == '=':
            return data[field] == value
        # Add more comparison operators as needed

    # If it's an operator, evaluate left and right sides
    elif ast.type == 'operator':
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)

        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result
    return False


# Test evaluation
if __name__ == "__main__":
    from backend.parser import parse_rule

    rule = parse_rule("age > 30 AND department = 'Sales'")
    data = {"age": 35, "department": "Sales", "salary": 60000}

    result = evaluate_rule(rule, data)
    print("User matches rule:", result)
