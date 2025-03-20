from booleans import boolean_map

def handle_add(inputs, variables, blocks):
    operand1 = get_input_or_number_value(inputs["NUM1"], variables, blocks)
    operand2 = get_input_or_number_value(inputs["NUM2"], variables, blocks)
    return f'({operand1} + {operand2})'

def handle_subtract(inputs, variables, blocks):
    operand1 = get_input_or_number_value(inputs["NUM1"], variables, blocks)
    operand2 = get_input_or_number_value(inputs["NUM2"], variables, blocks)
    return f'({operand1} - {operand2})'

def handle_multiply(inputs, variables, blocks):
    operand1 = get_input_or_number_value(inputs["NUM1"], variables, blocks)
    operand2 = get_input_or_number_value(inputs["NUM2"], variables, blocks)
    return f'({operand1} * {operand2})'

def handle_divide(inputs, variables, blocks):
    operand1 = get_input_or_number_value(inputs["NUM1"], variables, blocks)
    operand2 = get_input_or_number_value(inputs["NUM2"], variables, blocks)
    return f'({operand1} / {operand2})'

def handle_equals(inputs, variables, blocks):
    operand1 = get_input_or_number_value(inputs["OPERAND1"], variables, blocks)
    operand2 = get_input_or_number_value(inputs["OPERAND2"], variables, blocks)
    return f'({operand1} == {operand2})'

def handle_random(inputs, variables, blocks):
    num1 = get_input_or_number_value(inputs["FROM"], variables, blocks)
    num2 = get_input_or_number_value(inputs["TO"], variables, blocks)
    if "." in num1 or "." in num2:
        return f'getRandomFloat(tonumber("{num1}"), tonumber("{num2}"))'
    return f'getRandomInt(tonumber("{num1}"), tonumber("{num2}"))'

def handle_and(inputs, variables, blocks):
    operand1 = get_input_or_number_value(inputs["OPERAND1"], variables, blocks)
    operand2 = get_input_or_number_value(inputs["OPERAND2"], variables, blocks)
    return f'(({operand1}) and ({operand2}))'

def handle_or(inputs, variables, blocks):
    operand1 = get_input_or_number_value(inputs["OPERAND1"], variables, blocks)
    operand2 = get_input_or_number_value(inputs["OPERAND2"], variables, blocks)
    return f'(({operand1}) or ({operand2}))'

def handle_not(inputs, variables, blocks):
    operand = get_input_or_number_value(inputs["OPERAND"], variables, blocks)
    return f'(not ({operand}))'

def handle_gt(inputs, variables, blocks):
    operand1 = get_input_or_number_value(inputs["OPERAND1"], variables, blocks)
    operand2 = get_input_or_number_value(inputs["OPERAND2"], variables, blocks)
    return f'({operand1} > {operand2})'

def handle_lt(inputs, variables, blocks):
    operand1 = get_input_or_number_value(inputs["OPERAND1"], variables, blocks)
    operand2 = get_input_or_number_value(inputs["OPERAND2"], variables, blocks)
    return f'({operand1} < {operand2})'

def handle_join(inputs, variables, blocks):
    string1 = get_input_or_number_value(inputs["STRING1"], variables, blocks)
    string2 = get_input_or_number_value(inputs["STRING2"], variables, blocks)
    return f'({string1} .. {string2})'

def handle_mod(inputs, variables, blocks):
    num1 = get_input_or_number_value(inputs["NUM1"], variables, blocks)
    num2 = get_input_or_number_value(inputs["NUM2"], variables, blocks)
    return f'tonumber("{num1}") % tonumber("{num2}")'

def handle_round(inputs, variables, blocks):
    num = get_input_or_number_value(inputs["NUM"], variables, blocks)
    return f'math.floor(tonumber("{num}"))'

def handle_mathop(inputs, fields, variables, blocks):
    num = get_input_or_number_value(inputs["NUM"], variables, blocks)
    operator = fields["OPERATOR"][0]
    if operator == "abs":
        return f'math.abs(tonumber("{num}"))'
    elif operator == "floor":
        return f'math.floor(tonumber("{num}"))'
    elif operator == "ceiling":
        return f'math.ceil(tonumber("{num}"))'
    elif operator == "sqrt":
        return f'math.sqrt(tonumber("{num}"))'
    elif operator == "sin":
        return f'math.sin(tonumber("{num}"))'
    elif operator == "cos":
        return f'math.cos(tonumber("{num}"))'
    elif operator == "tan":
        return f'math.tan(tonumber("{num}"))'
    elif operator == "asin":
        return f'math.asin(tonumber("{num}"))'
    elif operator == "acos":
        return f'math.acos(tonumber("{num}"))'
    elif operator == "atan":
        return f'math.atan(tonumber("{num}"))'
    elif operator == "ln":
        return f'{num} --[["LN" are not supported at this moment, check back later.]]'
    elif operator == "log":
        return f'math.log(tonumber("{num}"))'
    elif operator == "e ^":
        return f'math.exp(tonumber("{num}"))'
    elif operator == "10 ^":
        return f'tonumber("{num}")^10'
    else:
        return f'--[[Unknown operator: {operator}]]'

def get_input_value(input_value, variables, blocks):
    if isinstance(input_value, list) and len(input_value) > 1:
        value = input_value[1]
        if isinstance(value, list) and len(value) > 1:
            inner_value = value[1]
            if isinstance(inner_value, str) and inner_value in variables:
                return f'{variables[inner_value]}'
            if isinstance(inner_value, str) and inner_value in blocks:
                block = blocks[inner_value]
                if block["opcode"] == "sensing_mousedown":
                    return "mousePressed()"
            return str(inner_value)
        return str(value)
    return "0"

def get_input_or_number_value(input_value, variables, blocks):
    if isinstance(input_value, list) and len(input_value) > 1:
        block_id = input_value[1]
        if isinstance(block_id, str) and block_id in blocks:
            block = blocks[block_id]
            if block["opcode"] in boolean_map:
                return boolean_map[block["opcode"]](block["inputs"], blocks)
            if block["opcode"] in operator_map:
                return operator_map[block["opcode"]](block["inputs"], variables, blocks)
    value = get_input_value(input_value, variables, blocks)
    return f'{value}' if not value.isdigit() else value

operator_map = {
    "operator_add": handle_add,
    "operator_subtract": handle_subtract,
    "operator_multiply": handle_multiply,
    "operator_divide": handle_divide,
    "operator_equals": handle_equals,
    "operator_random": handle_random,
    "operator_and": handle_and,
    "operator_or": handle_or,
    "operator_not": handle_not,
    "operator_gt": handle_gt,
    "operator_lt": handle_lt,
    "operator_join": handle_join,
    "operator_mod": handle_mod,
    "operator_round": handle_round,
    "operator_mathop": handle_mathop
}