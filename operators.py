def handle_add(inputs, variables, blocks):
    operand1 = get_input_value(inputs["NUM1"], variables, blocks)
    operand2 = get_input_value(inputs["NUM2"], variables, blocks)
    return f'({operand1} + {operand2})'

def handle_subtract(inputs, variables, blocks):
    operand1 = get_input_value(inputs["NUM1"], variables, blocks)
    operand2 = get_input_value(inputs["NUM2"], variables, blocks)
    return f'({operand1} - {operand2})'

def handle_multiply(inputs, variables, blocks):
    operand1 = get_input_value(inputs["NUM1"], variables, blocks)
    operand2 = get_input_value(inputs["NUM2"], variables, blocks)
    return f'({operand1} * {operand2})'

def handle_divide(inputs, variables, blocks):
    operand1 = get_input_value(inputs["NUM1"], variables, blocks)
    operand2 = get_input_value(inputs["NUM2"], variables, blocks)
    return f'({operand1} / {operand2})'

def handle_random(inputs, variables, blocks):
    from_num = get_input_value(inputs["FROM"], variables, blocks)
    to_num = get_input_value(inputs["TO"], variables, blocks)
    if "." in from_num or "." in to_num:
        return f'getRandomFloat({from_num}, {to_num})'
    else:
        return f'getRandomInt({from_num}, {to_num})'

def get_input_value(input_value, variables, blocks):
    if isinstance(input_value, list) and len(input_value) > 1:
        value = input_value[1]
        if isinstance(value, list) and len(value) > 1:
            inner_value = value[1]
            if isinstance(inner_value, str) and inner_value in variables:
                return f'[{variables[inner_value]}]'
            if isinstance(inner_value, str) and inner_value in blocks:
                block = blocks[inner_value]
                if block["opcode"] == "sensing_mousedown":
                    return "mousePressed()"
            return str(inner_value)
        return str(value)
    return "0"

operator_map = {
    "operator_add": handle_add,
    "operator_subtract": handle_subtract,
    "operator_multiply": handle_multiply,
    "operator_divide": handle_divide,
    "operator_random": handle_random
}