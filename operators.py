from booleans import boolean_map

def handle_add(inputs, variables, blocks, sprite_name):
    operand1 = get_input_or_number_value(inputs["NUM1"], variables, blocks, sprite_name)
    operand2 = get_input_or_number_value(inputs["NUM2"], variables, blocks, sprite_name)
    return f'({operand1} + {operand2})'

def handle_subtract(inputs, variables, blocks, sprite_name):
    operand1 = get_input_or_number_value(inputs["NUM1"], variables, blocks, sprite_name)
    operand2 = get_input_or_number_value(inputs["NUM2"], variables, blocks, sprite_name)
    return f'({operand1} - {operand2})'

def handle_multiply(inputs, variables, blocks, sprite_name):
    operand1 = get_input_or_number_value(inputs["NUM1"], variables, blocks, sprite_name)
    operand2 = get_input_or_number_value(inputs["NUM2"], variables, blocks, sprite_name)
    return f'({operand1} * {operand2})'

def handle_divide(inputs, variables, blocks, sprite_name):
    operand1 = get_input_or_number_value(inputs["NUM1"], variables, blocks, sprite_name)
    operand2 = get_input_or_number_value(inputs["NUM2"], variables, blocks, sprite_name)
    return f'({operand1} / {operand2})'

def handle_equals(inputs, variables, blocks, sprite_name):
    operand1 = get_input_or_number_value(inputs["OPERAND1"], variables, blocks, sprite_name)
    operand2 = get_input_or_number_value(inputs["OPERAND2"], variables, blocks, sprite_name)
    return f'({operand1} == {operand2})'

def handle_random(inputs, variables, blocks, sprite_name):
    num1 = get_input_or_number_value(inputs["FROM"], variables, blocks, sprite_name)
    num2 = get_input_or_number_value(inputs["TO"], variables, blocks, sprite_name)
    if "." in num1 or "." in num2:
        return f'getRandomFloat(tonumber({num1}), tonumber({num2}))'
    return f'getRandomInt(tonumber({num1}), tonumber({num2}))'

def handle_and(inputs, variables, blocks, sprite_name):
    operand1 = get_input_or_number_value(inputs["OPERAND1"], variables, blocks, sprite_name)
    operand2 = get_input_or_number_value(inputs["OPERAND2"], variables, blocks, sprite_name)
    return f'(({operand1}) and ({operand2}))'

def handle_or(inputs, variables, blocks, sprite_name):
    operand1 = get_input_or_number_value(inputs["OPERAND1"], variables, blocks, sprite_name)
    operand2 = get_input_or_number_value(inputs["OPERAND2"], variables, blocks, sprite_name)
    return f'(({operand1}) or ({operand2}))'

def handle_not(inputs, variables, blocks, sprite_name):
    operand = get_input_or_number_value(inputs["OPERAND"], variables, blocks, sprite_name)
    return f'(not ({operand}))'

def handle_gt(inputs, variables, blocks, sprite_name):
    operand1 = get_input_or_number_value(inputs["OPERAND1"], variables, blocks, sprite_name)
    operand2 = get_input_or_number_value(inputs["OPERAND2"], variables, blocks, sprite_name)
    return f'({operand1} > {operand2})'

def handle_lt(inputs, variables, blocks, sprite_name):
    operand1 = get_input_or_number_value(inputs["OPERAND1"], variables, blocks, sprite_name)
    operand2 = get_input_or_number_value(inputs["OPERAND2"], variables, blocks, sprite_name)
    return f'({operand1} < {operand2})'

def handle_join(inputs, variables, blocks, sprite_name):
    string1 = get_input_or_number_value(inputs["STRING1"], variables, blocks, sprite_name)
    string2 = get_input_or_number_value(inputs["STRING2"], variables, blocks, sprite_name)
    return f'({string1} .. {string2})'

def handle_mod(inputs, variables, blocks, sprite_name):
    num1 = get_input_or_number_value(inputs["NUM1"], variables, blocks, sprite_name)
    num2 = get_input_or_number_value(inputs["NUM2"], variables, blocks, sprite_name)
    return f'tonumber({num1}) % tonumber({num2})'

def handle_round(inputs, variables, blocks, sprite_name):
    num = get_input_or_number_value(inputs["NUM"], variables, blocks, sprite_name)
    return f'math.floor(tonumber({num}))'

def handle_mathop(inputs, fields, variables, blocks, sprite_name):
    num = get_input_or_number_value(inputs["NUM"], variables, blocks, sprite_name)
    operator = fields["OPERATOR"][0]
    if operator == "abs":
        return f'math.abs(tonumber({num}))'
    elif operator == "floor":
        return f'math.floor(tonumber({num}))'
    elif operator == "ceiling":
        return f'math.ceil(tonumber({num}))'
    elif operator == "sqrt":
        return f'math.sqrt(tonumber({num}))'
    elif operator == "sin":
        return f'math.sin(tonumber({num}))'
    elif operator == "cos":
        return f'math.cos(tonumber({num}))'
    elif operator == "tan":
        return f'math.tan(tonumber({num}))'
    elif operator == "asin":
        return f'math.asin(tonumber({num}))'
    elif operator == "acos":
        return f'math.acos(tonumber({num}))'
    elif operator == "atan":
        return f'math.atan(tonumber({num}))'
    elif operator == "ln":
        return f'{num} --[["LN" are not supported at this moment, check back later.]]'
    elif operator == "log":
        return f'math.log(tonumber({num}))'
    elif operator == "e ^":
        return f'math.exp(tonumber({num}))'
    elif operator == "10 ^":
        return f'tonumber({num})^10'
    else:
        return f'--[[Unknown operator: {operator}]]'

def get_input_value(input_value, variables, blocks, sprite_name):
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
                if block["opcode"] in operator_map:
                    return operator_map[block["opcode"]](block["inputs"], variables, blocks, sprite_name)
            return str(inner_value)
        return str(value)
    return "0"

def get_input_or_number_value(input_value, variables, blocks, sprite_name):
    if isinstance(input_value, list) and len(input_value) > 1:
        block_id = input_value[1]
        if isinstance(block_id, str) and block_id in blocks:
            block = blocks[block_id]
            if block["opcode"] in boolean_map:
                return boolean_map[block["opcode"]](block["inputs"], blocks)
            if block["opcode"] in operator_map:
                return operator_map[block["opcode"]](block["inputs"], variables, blocks, sprite_name)
            if block["opcode"].startswith("motion_"):
                if block["opcode"] == "motion_xposition":
                    return f'getProperty("{sprite_name}.x")'
                if block["opcode"] == "motion_yposition":
                    return f'getProperty("{sprite_name}.y")'
    value = get_input_value(input_value, variables, blocks, sprite_name)
    return f'"{value}"' if not value.isdigit() else value

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