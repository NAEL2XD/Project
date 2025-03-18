def handle_keypressed(inputs, blocks):
    key_option_id = inputs["KEY_OPTION"][1]
    if key_option_id in blocks:
        key_option_block = blocks[key_option_id]
        key_option = key_option_block["fields"]["KEY_OPTION"][0]
        key_translation_table = {
            "UP ARROW": "UP",
            "DOWN ARROW": "DOWN",
            "RIGHT ARROW": "RIGHT",
            "LEFT ARROW": "LEFT",
            "0": "ZERO || NUMPADZERO",
            "1": "ONE || NUMPADONE",
            "2": "TWO || NUMPADTWO",
            "3": "THREE || NUMPADTHREE",
            "4": "FOUR || NUMPADFOUR",
            "5": "FIVE || NUMPADFIVE",
            "6": "SIX || NUMPADSIX",
            "7": "SEVEN || NUMPADSEVEN",
            "8": "EIGHT || NUMPADEIGHT",
            "9": "NINE || NUMPADNINE",
            "*": "NUMPADMULTIPLY",
            "-": "MINUS",
            ",": "COMMA",
            ".": "PERIOD || NUMPADPERIOD",
            "[": "LBRACKET",
            "]": "RBRACKET",
            "\\": "BACKSLASH",
            ";": "SEMICOLON",
            "/": "SLASH || NUMPADSLASH",
            "'": "QUOTE"
        }
        
        if key_option in key_translation_table:
            translated_keys = key_translation_table[key_option].split(" || ")
            if len(translated_keys) == 1:
                return f'keyboardPressed("{translated_keys[0]}")'
            else:
                return ' or '.join([f'keyboardPressed("{key}")' for key in translated_keys])
        else:
            return f'keyboardPressed("{key_option}")'
    return 'keyboardPressed("unknown")'

def handle_mousedown(inputs, blocks):
    return 'mousePressed()'

def handle_touchingobject(inputs, sprite_name, blocks):
    object_name = get_input_value(inputs["TOUCHINGOBJECTMENU"], blocks=blocks)
    return f'touchingObject({sprite_name}, {object_name})'

def handle_distanceto(inputs, sprite_name, blocks):
    object_name = get_input_value(inputs["DISTANCETOMENU"], blocks=blocks)
    return f'math.abs((({{if mouse: getMouseX("other"), else: getProperty("{object_name}.x")}} - getProperty("{sprite_name}.x")) + ({{if mouse: getMouseY("other"), else: getProperty("{object_name}.y")}} - getProperty("{sprite_name}.y"))))'

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