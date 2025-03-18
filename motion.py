import random

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

def handle_goto(inputs, sprite_name, variables, blocks):
    destination = get_input_value(inputs["TO"], variables, blocks)
    if destination == "random position":
        return f'setProperty("{sprite_name}.x", getRandomInt(0, 480))\nsetProperty("{sprite_name}.y", getRandomInt(0, 360))'
    elif destination == "mouse-pointer":
        return f'setProperty("{sprite_name}.x", getMouseX("other"))\nsetProperty("{sprite_name}.y", getMouseY("other"))'
    else:
        return f'setProperty("{sprite_name}.x", getProperty("{destination}.x"))\nsetProperty("{sprite_name}.y", getProperty("{destination}.y"))'

def handle_gotoxy(inputs, sprite_name, variables, blocks):
    x_pos = get_input_value(inputs["X"], variables, blocks)
    y_pos = get_input_value(inputs["Y"], variables, blocks)
    return f'setProperty("{sprite_name}.x", {x_pos})\nsetProperty("{sprite_name}.y", {y_pos})'

def handle_glideto(inputs, sprite_name, variables, blocks, line_count):
    secs = get_input_value(inputs["SECS"], variables, blocks)
    destination = get_input_value(inputs["TO"], variables, blocks)
    if destination == "random position":
        x_pos = "getRandomInt(0, 480)"
        y_pos = "getRandomInt(0, 360)"
    elif destination == "mouse-pointer":
        x_pos = 'getMouseX("other")'
        y_pos = 'getMouseY("other")'
    else:
        x_pos = f'getProperty("{destination}.x")'
        y_pos = f'getProperty("{destination}.y")'
    return f'doTweenX("{sprite_name}{line_count}", "{sprite_name}", {x_pos}, {secs}, "linear")\ndoTweenY("{sprite_name}{line_count}", "{sprite_name}", {y_pos}, {secs}, "linear")'

def handle_glidesecstoxy(inputs, sprite_name, variables, blocks, line_count):
    secs = get_input_value(inputs["SECS"], variables, blocks)
    x_pos = get_input_value(inputs["X"], variables, blocks)
    y_pos = get_input_value(inputs["Y"], variables, blocks)
    return f'doTweenX("{sprite_name}{line_count}", "{sprite_name}", {x_pos}, {secs}, "linear")\ndoTweenY("{sprite_name}{line_count}", "{sprite_name}", {y_pos}, {secs}, "linear")'

def handle_pointindirection(inputs, sprite_name, variables, blocks):
    direction = get_input_value(inputs["DIRECTION"], variables, blocks)
    return f'setProperty("{sprite_name}.angle", {direction})'

def handle_pointtowards(inputs, sprite_name, variables, blocks):
    towards = get_input_value(inputs["TOWARDS"], variables, blocks)
    if towards == "mouse-pointer":
        return f'math.atan2(getMouseY("other") - getProperty("{sprite_name}.y"), getMouseX("other") - getProperty("{sprite_name}.x"))'
    else:
        return f'math.atan2(getProperty("{towards}.y") - getProperty("{sprite_name}.y"), getProperty("{towards}.x") - getProperty("{sprite_name}.x"))'

def handle_changexby(inputs, sprite_name, variables, blocks):
    change = get_input_value(inputs["DX"], variables, blocks)
    return f'setProperty("{sprite_name}.x", getProperty("{sprite_name}.x") + {change})'

def handle_setx(inputs, sprite_name, variables, blocks):
    x_pos = get_input_value(inputs["X"], variables, blocks)
    return f'setProperty("{sprite_name}.x", {x_pos})'

def handle_changeyby(inputs, sprite_name, variables, blocks):
    change = get_input_value(inputs["DY"], variables, blocks)
    return f'setProperty("{sprite_name}.y", getProperty("{sprite_name}.y") + {change})'

def handle_sety(inputs, sprite_name, variables, blocks):
    y_pos = get_input_value(inputs["Y"], variables, blocks)
    return f'setProperty("{sprite_name}.y", {y_pos})'