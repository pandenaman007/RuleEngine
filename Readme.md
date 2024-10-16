# Rule Engine with AST

This project implements a simple 3-tier rule engine that allows determining user eligibility based on attributes such as **age**, **department**, **income**, **experience**, and more. The engine utilizes an **Abstract Syntax Tree (AST)** to represent complex conditional rules. Users can dynamically create, combine, and evaluate rules via a simple API interface.

## Features

- **AST Representation**: Rules are represented as Abstract Syntax Trees to allow easy manipulation, evaluation, and combining of conditions.
- **Dynamic Rule Creation**: Users can define complex eligibility criteria using a rule string in a simple, natural language-like format.
- **Rule Combination**: The engine allows combining multiple rules using logical operators (AND/OR).
- **Rule Evaluation**: The engine evaluates combined rules against provided user data to determine eligibility.
- **MongoDB Integration**: Rules and user data are stored and queried using **MongoDB**.
- **Error Handling**: Built-in validation checks and error handling for invalid rule strings and data formats.

## Objective

The goal of this project is to create an engine capable of determining user eligibility based on various conditions (age, department, income, etc.) represented through complex rules. The engine supports creating, combining, and evaluating rules dynamically using an AST.

## Data Structure

### Node Structure

The AST is represented using a `Node` class where:
- `type`: Specifies whether the node is an "operand" or an "operator" (AND/OR).
- `left`: Reference to the left child node (for operators).
- `right`: Reference to the right child node (for operators).
- `value`: Holds the actual condition or operator string (e.g., "age > 30", "AND", "OR").

Example:
```json
{
  "type": "operator",
  "left": {
    "type": "operand",
    "value": "(age > 30)"
  },
  "right": {
    "type": "operand",
    "value": "(salary > 50000)"
  }
}
```
### Database Schema

Rules and application metadata are stored in MongoDB with the following schema:

- **Database**: `rule_engine`
- **Collection**: `rules`
- **Document**:
```json
{
  "_id": ObjectId,
  "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
}
```

### API Endpoints
- **create_rule**: `rule_string`
- **Description**
- **Input**
```json
{
  "rule_string": "((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)"
}
```
- **Output**
```json
{
  "ast": {
    "type": "operator",
    "left": {
      "type": "operand",
      "value": "(age > 30 AND department = 'Sales')"
    },
    "right": {
      "type": "operand",
      "value": "(age < 25 AND department = 'Marketing')"
    }
  }
}
```
- **combine rule**: `rules`
- **Description**: `Combines multiple rule strings into a single AST.`
- **Input**
```
{
  "rules": [
    "((age > 30 AND department = 'Sales'))",
    "(salary > 20000 OR experience > 5)"
  ]
}
```
- **Output**
```
{
  "ast": {
    "type": "operator",
    "left": {
      "type": "operand",
      "value": "(age > 30 AND department = 'Sales')"
    },
    "right": {
      "type": "operand",
      "value": "(salary > 20000 OR experience > 5)"
    }
  }
}
```
- **evaluate_rule**: `(rules_ast,data)`
- **Description**: `Evaluates the provided rule AST against a user data dictionary.`
- **Input**
```
{
  "rule_ast": {
    "type": "operator",
    "left": {
      "type": "operand",
      "value": "(age > 30)"
    },
    "right": {
      "type": "operand",
      "value": "(salary > 50000)"
    }
  },
  "data": {
    "age": 35,
    "salary": 60000
  }
}
```
**Output**:

json

Copy code

`{
  "result": true
}`

Example Usage
-------------

### 1\. Create Individual Rules

You can create a rule using the `create_rule` function by passing a string representing the condition:

python

Copy code

`rule_ast = create_rule("((age > 30 AND department = 'Sales') OR (age < 25 AND department = 'Marketing')) AND (salary > 50000 OR experience > 5)")`

### 2\. Combine Rules

Combine multiple rules into a single rule using the `combine_rules` function:

python

Copy code

`combined_rule_ast = combine_rules([
  "((age > 30 AND department = 'Sales'))",
  "(salary > 20000 OR experience > 5)"
])`

### 3\. Evaluate Combined Rule

Evaluate the combined rule against a user data dictionary:

python

Copy code

`data = {
  "age": 35,
  "salary": 60000,
  "department": "Sales",
  "experience": 4
}
result = evaluate_rule(combined_rule_ast, data)
print(result)  # Output: True`

Testing
-------

-   **Create Individual Rules**: Test parsing of rule strings into ASTs.
-   **Combine Rules**: Ensure that combining multiple rules into a single AST works correctly.
-   **Evaluate Rules**: Test the engine against sample user data and verify the results.

Dependencies
------------

-   Python 3.x
-   Flask (for API server)
-   MongoDB (for data storage)
-   pymongo (MongoDB driver for Python)
-   re (Regular Expressions for parsing)

Setting Up
----------

### 1\. Clone the repository:

bash

Copy code

`git clone https://github.com/your-username/rule-engine-ast.git`

### 2\. Install dependencies:

bash

Copy code

`pip install -r requirements.txt`

### 3\. Set up MongoDB:

Install MongoDB locally or use Docker to set it up as a container:

bash

Copy code

`docker run -d -p 27017:27017 --name mongodb mongo`

### 4\. Run the application:

bash

Copy code

`python app.py`

You can now use the API to create, combine, and evaluate rules.

Design Choices
--------------

-   **AST Representation**: Chosen for its flexibility in building and manipulating complex logical expressions.
-   **MongoDB**: Provides a simple and scalable storage solution for rules and user data.
-   **Python**: Offers quick development and flexibility with regular expressions and JSON handling.

Bonus Features
--------------

-   **Error Handling**: Handles missing operators, invalid comparisons, and rule syntax errors.
-   **Dynamic Rule Modification**: Allows modifications to existing rules via additional functions.

Future Enhancements
-------------------

-   Support user-defined functions in the rule language for advanced conditions.
-   Extend rule combinations to support more complex logic like NOT.
-   Implement a UI to visualize and manage rules.
