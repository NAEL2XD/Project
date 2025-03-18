import sensing

def handle_gt(inputs, variables, blocks):
    operand1 = get_input_value(inputs["OPERAND1"], variables, blocks)
    operand2 = get_input_value(inputs["OPERAND2"], variables, blocks)
    operand1 = convert_to_number_if_needed(operand1)
    operand2 = convert_to_number_if_needed(operand2)
    return f'({operand1} > {operand2})'

def handle_lt(inputs, variables, blocks):
    operand1 = get_input_value(inputs["OPERAND1"], variables, blocks)
    operand2 = get_input_value(inputs["OPERAND2"], variables, blocks)
    operand1 = convert_to_number_if_needed(operand1)
    operand2 = convert_to_number_if_needed(operand2)
    return f'({operand1} < {operand2})'

def handle_equals(inputs, variables, blocks):
    operand1 = get_input_value(inputs["OPERAND1"], variables, blocks)
    operand2 = get_input_value(inputs["OPERAND2"], variables, blocks)
    operand1 = convert_to_number_if_needed(operand1)
    operand2 = convert_to_number_if_needed(operand2)
    return f'({operand1} == {operand2})'

def handle_and(inputs, variables, blocks):
    operand1 = get_input_or_boolean_value(inputs["OPERAND1"], variables, blocks)
    operand2 = get_input_or_boolean_value(inputs["OPERAND2"], variables, blocks)
    operand1 = convert_to_boolean_or_variable(operand1)
    operand2 = convert_to_boolean_or_variable(operand2)
    return f'({operand1} and {operand2})'

def handle_or(inputs, variables, blocks):
    operand1 = get_input_or_boolean_value(inputs["OPERAND1"], variables, blocks)
    operand2 = get_input_or_boolean_value(inputs["OPERAND2"], variables, blocks)
    operand1 = convert_to_boolean_or_variable(operand1)
    operand2 = convert_to_boolean_or_variable(operand2)
    return f'({operand1} or {operand2})'

def handle_not(inputs, variables, blocks):
    operand = get_input_or_boolean_value(inputs["OPERAND"], variables, blocks)
    operand = convert_to_boolean_or_variable(operand)
    return f'(not {operand})'

def get_input_or_boolean_value(input_value, variables, blocks):
    if isinstance(input_value, list) and len(input_value) > 1:
        block_id = input_value[1]
        if block_id in blocks:
            block = blocks[block_id]
            if block["opcode"] in boolean_map:
                return boolean_map[block["opcode"]](block["inputs"], variables, blocks)
            elif block["opcode"] == "sensing_mousedown":
                return "mousePressed()"
            elif block["opcode"] == "sensing_keypressed":
                key_option = block["inputs"]["KEY_OPTION"]
                key_value = get_input_value(key_option, variables, blocks)
                key_translated = sensing.translate_key_option(key_value.strip('"'))
                keys = key_translated.split(" || ")
                if len(keys) == 1:
                    return f'keyboardPressed("{keys[0]}")'
                else:
                    return " or ".join([f'keyboardPressed("{key}")' for key in keys])
            else:
                return get_input_value(input_value, variables, blocks)
    return get_input_value(input_value, variables, blocks)

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
                if block["opcode"] == "sensing_keypressed":
                    key_option = block["inputs"]["KEY_OPTION"]
                    key_value = get_input_value(key_option, variables, blocks)
                    key_translated = sensing.translate_key_option(key_value.strip('"'))
                    keys = key_translated.split(" || ")
                    if len(keys) == 1:
                        return f'keyboardPressed("{keys[0]}")'
                    else:
                        return " or ".join([f'keyboardPressed("{key}")' for key in keys])
            return convert_to_number_if_needed(inner_value)
        return convert_to_number_if_needed(value)
    return "0"

def convert_to_number_if_needed(value):
    if "tonumber" in value:
        return value
    if value.isdigit():
        return f'tonumber("{value}")'
    elif value.lower() in ["true", "false"]:
        return value.lower()
    return f'"{value}"'

def convert_to_boolean_or_variable(value):
    if value in ["true", "false"]:
        return value
    if '"' not in value:
        return f'keyboardPressed({value})'
    return value

boolean_map = {
    "operator_gt": handle_gt,
    "operator_lt": handle_lt,
    "operator_equals": handle_equals,
    "operator_and": handle_and,
    "operator_or": handle_or,
    "operator_not": handle_not
}