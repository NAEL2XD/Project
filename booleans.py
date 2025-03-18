def handle_keypressed(inputs, blocks):
    key_option = get_input_value(inputs["KEY_OPTION"], blocks=blocks)
    return f'keyboardPressed({key_option})'

def handle_mousedown(inputs, blocks):
    return 'mousePressed()'

def handle_touchingobject(inputs, sprite_name, blocks):
    object_name = get_input_value(inputs["TOUCHINGOBJECTMENU"], blocks=blocks)
    return f'touchingObject({sprite_name}, {object_name})'

def handle_distanceto(inputs, sprite_name, blocks):
    object_name = get_input_value(inputs["DISTANCETOMENU"], blocks=blocks)
    return f'distanceTo({sprite_name}, {object_name})'

def handle_sensing_of(inputs, fields, blocks, variables):
    property_name = fields["PROPERTY"][0]
    object_name = get_input_value(inputs["OBJECT"], blocks=blocks)
    return f'{property_name}({object_name})'

def convert_to_number_if_needed(value):
    try:
        return float(value)
    except ValueError:
        return value

boolean_map = {
    "sensing_keypressed": handle_keypressed,
    "sensing_mousedown": handle_mousedown,
    "sensing_touchingobject": handle_touchingobject,
    "sensing_distanceto": handle_distanceto,
    "sensing_of": handle_sensing_of
}

def get_input_value(input_value, blocks=None):
    if isinstance(input_value, list) and len(input_value) > 1:
        value = input_value[1]
        if isinstance(value, list) and len(value) > 1:
            inner_value = value[1]
            if isinstance(inner_value, str):
                return f'"{inner_value}"'
            return str(inner_value)
        return str(value)
    return "0"