def handle_sensing_of(inputs, fields, blocks, variables):
    property = fields["PROPERTY"][0]
    object_block = blocks[inputs["OBJECT"][1]]
    object_name = object_block["fields"]["OBJECT"][0]
    
    if object_name == "_stage_":
        return '0 --[[Stage are not supported]]'
    
    if property == "x position":
        return f'getProperty("{object_name}.x")'
    elif property == "y position":
        return f'getProperty("{object_name}.y")'
    elif property == "direction":
        return f'getProperty("{object_name}.angle")'
    elif property == "size":
        return f'getProperty("{object_name}.scale.x")'
    else:
        return '0 --[[Variables are not supported]]'

def handle_sensing_of_object_menu(inputs, fields, blocks, variables):
    return handle_sensing_of(inputs, fields, blocks, variables)

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

def translate_key_option(key_option):
    if key_option in key_translation_table:
        return key_translation_table[key_option]
    return key_option.upper()

def handle_keypressed(inputs, blocks):
    key_option = inputs["KEY_OPTION"]
    key_value = get_input_value(key_option, blocks).split(' || ')
    print(len(key_value))
    if len(key_value) == 1:
        return f'(keyboardPressed("{translate_key_option(key_value[0])}"))'
    else:
        return " or ".join([f'(keyboardPressed("{key}")' for key in key_value]) + "))"

def handle_mousedown(inputs, sprite_name, blocks):
    return 'mousePressed()'

def handle_mousex(inputs, sprite_name, blocks):
    return 'getMouseX("other")'

def handle_mousey(inputs, sprite_name, blocks):
    return 'getMouseY("other")'

def handle_distanceto(inputs, sprite_name, blocks):
    target_block = blocks[inputs["DISTANCETOMENU"][1]]
    target = target_block["fields"]["DISTANCETOMENU"][0]
    if target == "_mouse_":
        return f'math.abs((getMouseX("other") - getProperty("{sprite_name}.x")) + (getMouseY("other") - getProperty("{sprite_name}.y")))'
    else:
        return f'math.abs((getProperty("{target}.x") - getProperty("{sprite_name}.x")) + (getProperty("{target}.y") - getProperty("{sprite_name}.y")))'

def handle_touchingobject(inputs, sprite_name, blocks):
    touching_object_block = blocks[inputs["TOUCHINGOBJECTMENU"][1]]
    touching_object = touching_object_block["fields"]["TOUCHINGOBJECTMENU"][0]
    if touching_object == "_mouse_":
        return f'mouseOverlaps("{sprite_name}")'
    elif touching_object == "_edge_":
        return 'true --[[touching edge is not supported, default to true]]'
    else:
        return f'objectsOverlap("{sprite_name}", "{touching_object}")'

def get_input_value(input_value, blocks):
    if isinstance(input_value, list) and len(input_value) > 1:
        value = input_value[1]
        if value in blocks:
            block = blocks[value]
            if block["opcode"] == "sensing_keyoptions":
                return translate_key_option(block["fields"]["KEY_OPTION"][0])
        return value
    return "0"

def escape_quotes(value):
    return value.replace('"', '\\"')