from flask import Flask, request, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import re

app = Flask(__name__)

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")  # Adjust URI if needed
db = client["rule_engine"]
rules_collection = db["rules"]


# Dummy Node class for AST representation
class Node:
    def __init__(self, node_type, left=None, right=None, value=None):
        self.type = node_type
        self.left = left
        self.right = right
        self.value = value

    def to_dict(self):
        return {
            'type': self.type,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None,
            'value': self.value
        }

    @staticmethod
    def from_dict(data):
        if data['type'] == 'operand':
            return Node(node_type='operand', value=data['value'])
        elif data['type'] == 'operator':
            left = Node.from_dict(data['left']) if data['left'] else None
            right = Node.from_dict(data['right']) if data['right'] else None
            return Node(node_type='operator', left=left, right=right, value=data['value'])


# Helper function to parse an operand (e.g., "age > 30")
def parse_operand(operand):
    operand = operand.strip()

    # Removing outer parentheses if they exist
    if operand.startswith("(") and operand.endswith(")"):
        operand = operand[1:-1].strip()

    if '>' in operand:
        field, value = operand.split('>')
        return field.strip(), '>', int(value.strip())
    elif '<' in operand:
        field, value = operand.split('<')
        return field.strip(), '<', int(value.strip())
    elif '=' in operand:
        field, value = operand.split('=')
        return field.strip(), '=', value.strip().strip("'")
    else:
        raise ValueError("Unsupported operand format")


# Helper function to split complex expressions
def split_expression(expression, operator):
    # First split by the main operator (AND/OR), but not within parentheses
    pattern = re.compile(rf"\s*{operator}\s*")
    parts = pattern.split(expression)
    return [part.strip() for part in parts]


# Function to handle logical AND/OR operators and construct AST
def parse_logical_expression(expression):
    expression = expression.strip()
    if 'AND' in expression:
        parts = split_expression(expression, 'AND')
        return 'AND', parts
    elif 'OR' in expression:
        parts = split_expression(expression, 'OR')
        return 'OR', parts
    else:
        raise ValueError("Unsupported logical expression format")


# Function to handle complex logical expressions with parentheses and operators
def parse_expression(expression):
    # Remove outer parentheses
    expression = expression.strip()
    if expression.startswith("(") and expression.endswith(")"):
        expression = expression[1:-1].strip()

    # Check for logical expressions
    if 'AND' in expression or 'OR' in expression:
        return parse_logical_expression(expression)

    # Else, treat it as a simple operand expression
    return 'operand', [expression]


# Function to recursively build the AST for the rule
def build_ast(expression):
    expression = expression.strip()

    # First, try to handle logical expressions
    if 'AND' in expression or 'OR' in expression:
        operator, subexpressions = parse_logical_expression(expression)
        left_ast = build_ast(subexpressions[0])
        right_ast = build_ast(subexpressions[1])
        return Node(node_type='operator', left=left_ast, right=right_ast, value=operator)

    # Otherwise, it's a simple comparison operand (e.g., "age > 30")
    return Node(node_type='operand', value=expression)


# Function to recursively evaluate a complex AST (logical and comparison)
# Function to recursively evaluate a complex AST (logical and comparison)
def evaluate_rule(ast, data):
    if ast.type == 'operand':
        # Handle both simple and logical expressions
        operand = ast.value
        if 'AND' in operand or 'OR' in operand:
            operator, subexpressions = parse_logical_expression(operand)
            results = [evaluate_rule(Node('operand', value=sub), data) for sub in subexpressions]

            # Combine results based on the logical operator
            if operator == 'AND':
                return all(results)
            elif operator == 'OR':
                return any(results)

        # If it's a simple operand (e.g., "age > 30")
        field, operator, value = parse_operand(operand)

        # Check if the field exists in the data
        if field not in data:
            return False  # Field is missing, returning False

        # Evaluate based on the operator
        if operator == '>':
            return data[field] > value
        elif operator == '<':
            return data[field] < value
        elif operator == '=':
            return data[field] == value
        return False

    elif ast.type == 'operator':
        # Recursively evaluate left and right children
        left_result = evaluate_rule(ast.left, data)
        right_result = evaluate_rule(ast.right, data)

        # Combine results based on the operator
        if ast.value == 'AND':
            return left_result and right_result
        elif ast.value == 'OR':
            return left_result or right_result
        return False



# API to create individual rules and store in MongoDB
@app.route('/create_rule', methods=['POST'])
def create_rule_api():
    try:
        rule_string = request.json.get('rule')
        ast = build_ast(rule_string)

        # Store the rule in MongoDB
        result = rules_collection.insert_one({"rule_string": rule_string})
        return jsonify({"rule_id": str(result.inserted_id), "ast": ast.to_dict()}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API to combine multiple rules into one
@app.route('/combine_rules', methods=['POST'])
def combine_rules_api():
    try:
        rules = request.json.get('rules')  # List of rule strings
        root = None

        for rule in rules:
            rule_node = Node(node_type='operand', value=rule)

            if root is None:
                root = rule_node
            else:
                root = Node(node_type='operator', left=root, right=rule_node, value='AND')

        # Return the combined AST as JSON
        return jsonify(root.to_dict()), 201  # HTTP 201 Created
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# API to evaluate a combined rule
@app.route('/evaluate_combined_rule', methods=['POST'])
def evaluate_combined_rule():
    try:
        rule_ast = request.json.get('rule_ast')
        data = request.json.get('data')

        # Convert JSON rule AST back to Node structure
        ast = Node.from_dict(rule_ast)

        # Evaluate the rule
        result = evaluate_rule(ast, data)
        return jsonify({'result': result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
