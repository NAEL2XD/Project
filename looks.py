import sensing
import booleans
import operators
import vars
import main

def handle_say(inputs, sprite_name, line_count, blocks, includes, variables):
    message = get_input_or_sensing_value(inputs["MESSAGE"], sprite_name, line_count, blocks, variables)
    if len(inputs["MESSAGE"]) == 3:
        listName = main.sanitize_variable_name(inputs["MESSAGE"][1][1])
        message = f"{sprite_name}.{listName}"
    if "mouseOverlaps" in message:
        includes.add("mouseOverlaps")
    return f'debugPrint("{sprite_name}:{line_count}: " .. {message})'

def handle_sayforsecs(inputs, sprite_name, line_count, blocks, includes, variables):
    message = get_input_or_sensing_value(inputs["MESSAGE"], sprite_name, line_count, blocks, variables)
    if "mouseOverlaps" in message:
        includes.add("mouseOverlaps")
    seconds = get_input_value(inputs["SECS"], sprite_name, blocks=blocks, variables=variables)
    return f'debugPrint("{sprite_name}:{line_count}: " .. {message})\nwait({seconds})\ndebugPrint("{sprite_name}:{line_count}: ")'

def handle_think(inputs, sprite_name, line_count, blocks, includes, variables):
    message = get_input_or_sensing_value(inputs["MESSAGE"], sprite_name, line_count, blocks, variables)
    if "mouseOverlaps" in message:
        includes.add("mouseOverlaps")
    return f'debugPrint("{sprite_name}:{line_count}: " .. {message})'

def handle_thinkforsecs(inputs, sprite_name, line_count, blocks, includes, variables):
    message = get_input_or_sensing_value(inputs["MESSAGE"], sprite_name, line_count, blocks, variables)
    if "mouseOverlaps" in message:
        includes.add("mouseOverlaps")
    seconds = get_input_value(inputs["SECS"], sprite_name, blocks=blocks, variables=variables)
    return f'debugPrint("{sprite_name}:{line_count}: " .. {message})\nwait({seconds})\ndebugPrint("{sprite_name}:{line_count}: ")'

def handle_changesizeby(inputs, sprite_name):
    change = get_input_value(inputs["CHANGE"], sprite_name)
    return f'setProperty("{sprite_name}.scale.x", getProperty("{sprite_name}.scale.x") + {change})\nsetProperty("{sprite_name}.scale.y", getProperty("{sprite_name}.scale.y") + {change})'

def handle_setsizeto(inputs, sprite_name):
    size = get_input_value(inputs["SIZE"], sprite_name)
    return f'setProperty("{sprite_name}.scale.x", {size} / 100)\nsetProperty("{sprite_name}.scale.y", {size} / 100)'

def handle_changeeffectby(inputs, fields, sprite_name, variables, blocks):
    effect = fields["EFFECT"][0].lower()
    if effect == "ghost":
        effect = "alpha"
    elif effect == "color":
        effect = "hue"
    change = get_input_value(inputs["CHANGE"], sprite_name, variables, blocks)
    if effect == "alpha":
        current_value = f'getProperty("{sprite_name}.{effect}")'
        new_value = f'1 - (0.01 * ({current_value} + {change}))'
        return f'setProperty("{sprite_name}.{effect}", {new_value})'
    return f'setProperty("{sprite_name}.{effect}", getProperty("{sprite_name}.{effect}") + {change})'

def handle_seteffectto(inputs, fields, sprite_name, variables, blocks):
    effect = fields["EFFECT"][0].lower()
    if effect == "ghost":
        effect = "alpha"
    elif effect == "color":
        effect = "hue"
    value = get_input_value(inputs["VALUE"], sprite_name, variables, blocks)
    if effect == "alpha":
        new_value = f'1 - (0.01 * {value})'
        return f'setProperty("{sprite_name}.{effect}", {new_value})'
    return f'setProperty("{sprite_name}.{effect}", {value})'

def handle_show(sprite_name):
    return f'setProperty("{sprite_name}.visible", true)'

def handle_hide(sprite_name):
    return f'setProperty("{sprite_name}.visible", false)'

def handle_gotofrontback(fields, sprite_name):
    position = fields["FRONT_BACK"][0]
    if position == "front":
        return f'goToFront("{sprite_name}")'
    else:
        return f'goToBack("{sprite_name}")'

def handle_goforwardbackwardlayers(inputs, fields, sprite_name):
    direction = fields["FORWARD_BACKWARD"][0]
    layers = get_input_value(inputs["NUM"], sprite_name)
    if direction == "forward":
        return f'goForwardLayers("{sprite_name}", {layers})'
    else:
        return f'goBackwardLayers("{sprite_name}", {layers})'

def handle_size(sprite_name):
    return f'getProperty("{sprite_name}.scale.x") * 100'

def get_input_value(input_value, sprite_name, variables=None, blocks=None):
    if isinstance(input_value, list) and len(input_value) > 1:
        value = input_value[1]
        if isinstance(value, list) and len(value) > 1:
            inner_value = value[1]
            if isinstance(inner_value, str) and variables and inner_value in variables:
                return f'{variables[inner_value]}'
            if isinstance(inner_value, str) and inner_value in blocks:
                block = blocks[inner_value]
                if block["opcode"] == "sensing_mousedown":
                    return "mousePressed()"
                if block["opcode"] in operators.operator_map:
                    return operators.operator_map[block["opcode"]](block["inputs"], variables, blocks, sprite_name)
            return str(inner_value)
        return str(value)
    return "0"

def get_input_or_sensing_value(input_value, sprite_name, line_count, blocks, variables):
    if isinstance(input_value, list) and len(input_value) > 2:
        block_id = input_value[1]
        if isinstance(block_id, str) and block_id in blocks:
            block = blocks[block_id]
            if block["opcode"] == "sensing_touchingobject":
                return sensing.handle_touchingobject(block["inputs"], sprite_name, blocks)
            if block["opcode"] == "sensing_touchingobjectmenu" or block["opcode"] == "sensing_distancetomenu":
                return block["fields"]["KEY_OPTION"][0]
            if block["opcode"] == "sensing_keypressed":
                return sensing.handle_keypressed(block["inputs"], blocks)
            if block["opcode"] == "sensing_distanceto":
                return sensing.handle_distanceto(block["inputs"], sprite_name, blocks)
            if block["opcode"] == "sensing_of":
                return sensing.handle_sensing_of(block["inputs"], block["fields"], blocks, variables)
            if block["opcode"] == "operator_random":
                return operators.handle_random(block["inputs"], variables, blocks, sprite_name)
            if block["opcode"] == "operator_join":
                return operators.handle_join(block["inputs"], variables, blocks, sprite_name)
            if block["opcode"] == "operator_mod":
                return operators.handle_mod(block["inputs"], variables, blocks, sprite_name)
            if block["opcode"] == "operator_round":
                return operators.handle_round(block["inputs"], variables, blocks, sprite_name)
            if block["opcode"] == "operator_mathop":
                return operators.handle_mathop(block["inputs"], block["fields"], variables, blocks, sprite_name)
            if block["opcode"] in booleans.boolean_map:
                return booleans.boolean_map[block["opcode"]](block["inputs"], blocks)
            if block["opcode"] in operators.operator_map:
                return operators.operator_map[block["opcode"]](block["inputs"], variables, blocks, sprite_name)
            if block["opcode"] in vars.var_map:
                return vars.var_map[block["opcode"]](block["inputs"], block["fields"], sprite_name, variables, blocks)
    value = get_input_value(input_value, sprite_name, blocks=blocks, variables=variables)
    return f'"{escape_quotes(value)}"'

def escape_quotes(value):
    if isinstance(value, str):
        value = value.replace('"', '\\"')
    return value