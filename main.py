import json
import motion
import looks
import control
import sensing
import operators
import booleans
import os
import shutil
from traceback import format_exc

EXPORT_FOLDER = "export"

def setup_export_folder():
    if os.path.exists(EXPORT_FOLDER):
        shutil.rmtree(EXPORT_FOLDER)
    os.makedirs(EXPORT_FOLDER)

def convert_blocks_to_lua(blocks, variables, sprite_name):
    lua_code = []
    on_update_code = []
    line_count = 0
    wait_function_added = False
    includes = set()
    processed_blocks = set()
    on_create_post_code = []
    on_create_post_header = f"""function onCreatePost()
    makeLuaSprite('stage')
    makeGraphic('stage', 1920, 1080, 'FFFFFF')
    setObjectCamera('stage', 'other')
    addLuaSprite('stage')

    makeLuaSprite('{sprite_name}', '{sprite_name}')
    setObjectCamera('{sprite_name}', 'other')
    addLuaSprite('{sprite_name}')
"""
    on_create_post_footer = "\nend\n"

    block_map = {
        "event_whenflagclicked": lambda inputs, fields: "",
        "motion_movesteps": lambda inputs, fields: f'setProperty("{sprite_name}.x", getProperty("{sprite_name}.x") + {operators.get_input_or_number_value(inputs["STEPS"], variables, blocks, sprite_name)})' if 'STEPS' in inputs else f'setProperty("{sprite_name}.x", getProperty("{sprite_name}.x") + 0)',
        "motion_turnright": lambda inputs, fields: f'setProperty("{sprite_name}.angle", getProperty("{sprite_name}.angle") + {operators.get_input_or_number_value(inputs["DEGREES"], variables, blocks, sprite_name)})' if 'DEGREES' in inputs else f'setProperty("{sprite_name}.angle", getProperty("{sprite_name}.angle") + 0)',
        "motion_turnleft": lambda inputs, fields: f'setProperty("{sprite_name}.angle", getProperty("{sprite_name}.angle") - {operators.get_input_or_number_value(inputs["DEGREES"], variables, blocks, sprite_name)})' if 'DEGREES' in inputs else f'setProperty("{sprite_name}.angle", getProperty("{sprite_name}.angle") - 0)',
        "motion_xposition": lambda inputs, fields: f'getProperty("{sprite_name}.x")',
        "motion_yposition": lambda inputs, fields: f'getProperty("{sprite_name}.y")',
        "motion_goto": lambda inputs, fields: motion.handle_goto(inputs, sprite_name, variables, blocks),
        "motion_gotoxy": lambda inputs, fields: motion.handle_gotoxy(inputs, sprite_name, variables, blocks),
        "motion_glideto": lambda inputs, fields: motion.handle_glideto(inputs, sprite_name, variables, blocks, line_count),
        "motion_glidesecstoxy": lambda inputs, fields: motion.handle_glidesecstoxy(inputs, sprite_name, variables, blocks, line_count),
        "motion_pointindirection": lambda inputs, fields: motion.handle_pointindirection(inputs, sprite_name, variables, blocks),
        "motion_pointtowards": lambda inputs, fields: motion.handle_pointtowards(inputs, sprite_name, variables, blocks),
        "motion_changexby": lambda inputs, fields: motion.handle_changexby(inputs, sprite_name, variables, blocks),
        "motion_setx": lambda inputs, fields: motion.handle_setx(inputs, sprite_name, variables, blocks),
        "motion_changeyby": lambda inputs, fields: motion.handle_changeyby(inputs, sprite_name, variables, blocks),
        "motion_sety": lambda inputs, fields: motion.handle_sety(inputs, sprite_name, variables, blocks),
        "motion_direction": lambda inputs, fields: f'getProperty("{sprite_name}.angle")',
        "looks_say": lambda inputs, fields: looks.handle_say(inputs, sprite_name, line_count, blocks, includes, variables),
        "looks_sayforsecs": lambda inputs, fields: looks.handle_sayforsecs(inputs, sprite_name, line_count, blocks, includes, variables),
        "looks_think": lambda inputs, fields: looks.handle_think(inputs, sprite_name, line_count, blocks, includes, variables),
        "looks_thinkforsecs": lambda inputs, fields: looks.handle_thinkforsecs(inputs, sprite_name, line_count, blocks, includes, variables),
        "looks_changesizeby": lambda inputs, fields: looks.handle_changesizeby(inputs, sprite_name),
        "looks_setsizeto": lambda inputs, fields: looks.handle_setsizeto(inputs, sprite_name),
        "looks_changeeffectby": lambda inputs, fields: looks.handle_changeeffectby(inputs, fields, sprite_name, variables, blocks),
        "looks_seteffectto": lambda inputs, fields: looks.handle_seteffectto(inputs, fields, sprite_name, variables, blocks),
        "looks_show": lambda inputs, fields: looks.handle_show(sprite_name),
        "looks_hide": lambda inputs, fields: looks.handle_hide(sprite_name),
        "looks_gotofrontback": lambda inputs, fields: looks.handle_gotofrontback(fields, sprite_name),
        "looks_goforwardbackwardlayers": lambda inputs, fields: looks.handle_goforwardbackwardlayers(inputs, fields, sprite_name),
        "looks_size": lambda inputs, fields: looks.handle_size(sprite_name),
        "control_wait": lambda inputs, fields: control.handle_wait(inputs, sprite_name, line_count, blocks),
        "control_repeat": lambda inputs, fields: control.handle_repeat(inputs, sprite_name, line_count, blocks, process_block),
        "control_forever": lambda inputs, fields: control.handle_forever(inputs, sprite_name, blocks, process_block),
        "control_if": lambda inputs, fields: control.handle_if(inputs, sprite_name, blocks, process_block),
        "sensing_touchingobject": lambda inputs, fields: sensing.handle_touchingobject(inputs, sprite_name, blocks),
        "sensing_distanceto": lambda inputs, fields: sensing.handle_distanceto(inputs, sprite_name, blocks),
        "sensing_keypressed": lambda inputs, fields: sensing.handle_keypressed(inputs, blocks),
        "sensing_mousedown": lambda inputs, fields: sensing.handle_mousedown(inputs, sprite_name, blocks),
        "sensing_mousex": lambda inputs, fields: sensing.handle_mousex(inputs, sprite_name, blocks),
        "sensing_mousey": lambda inputs, fields: sensing.handle_mousey(inputs, sprite_name, blocks),
        "sensing_of": lambda inputs, fields: sensing.handle_sensing_of(inputs, fields, blocks, variables),
        "sensing_of_object_menu": lambda inputs, fields: sensing.handle_sensing_of_object_menu(inputs, fields, blocks, variables),
        "operator_add": lambda inputs, fields: operators.handle_add(inputs, variables, blocks, sprite_name),
        "operator_subtract": lambda inputs, fields: operators.handle_subtract(inputs, variables, blocks, sprite_name),
        "operator_multiply": lambda inputs, fields: operators.handle_multiply(inputs, variables, blocks, sprite_name),
        "operator_divide": lambda inputs, fields: operators.handle_divide(inputs, variables, blocks, sprite_name),
        "operator_random": lambda inputs, fields: operators.handle_random(inputs, variables, blocks, sprite_name),
        "operator_gt": lambda inputs, fields: operators.handle_gt(inputs, variables, blocks, sprite_name),
        "operator_lt": lambda inputs, fields: operators.handle_lt(inputs, variables, blocks, sprite_name),
        "operator_equals": lambda inputs, fields: operators.handle_equals(inputs, variables, blocks, sprite_name),
        "operator_and": lambda inputs, fields: operators.handle_and(inputs, variables, blocks, sprite_name),
        "operator_or": lambda inputs, fields: operators.handle_or(inputs, variables, blocks, sprite_name),
        "operator_not": lambda inputs, fields: operators.handle_not(inputs, variables, blocks, sprite_name),
        "operator_join": lambda inputs, fields: operators.handle_join(inputs, variables, blocks, sprite_name),
        "operator_mod": lambda inputs, fields: operators.handle_mod(inputs, variables, blocks, sprite_name),
        "operator_round": lambda inputs, fields: operators.handle_round(inputs, variables, blocks, sprite_name),
        "operator_mathop": lambda inputs, fields: operators.handle_mathop(inputs, fields, variables, blocks, sprite_name)
    }

    def process_block(block_id, target_code):
        nonlocal line_count, wait_function_added
        if block_id in processed_blocks:
            return
        processed_blocks.add(block_id)
        
        block = blocks[block_id]
        opcode = block["opcode"]
        if opcode == "control_wait" and not wait_function_added:
            lua_code.append('function wait(n) if n>0 then os.execute("ping -n "..tonumber(n+1).." localhost > NUL") end end\n')
            wait_function_added = True
        
        if opcode in block_map:
            if callable(block_map[opcode]):
                try:
                    if "fields" in block:
                        result = block_map[opcode](block["inputs"], block["fields"])
                    else:
                        result = block_map[opcode](block["inputs"], {})
                    
                    if opcode == "event_whenflagclicked":
                        on_create_post_code.append(result)
                    elif opcode == "control_forever":
                        on_update_code.append(result)
                    else:
                        target_code.append(result + "\n")
                    
                    line_count += 1
                except Exception as e:
                    target_code.append(f"--[[Error processing block {block_id}:\n{str(format_exc())}]]\n")
            else:
                target_code.append(block_map[opcode] + "\n")
                line_count += 1
        
        if block.get("next"):
            process_block(block["next"], target_code)

    # Check for top-level blocks and process them
    has_green_flag = False
    for block_id, block in blocks.items():
        if block["topLevel"]:
            if block["opcode"] == "event_whenflagclicked":
                has_green_flag = True
            process_block(block_id, on_create_post_code)

    if on_create_post_code:
        on_create_post_code.append(on_create_post_footer)

    if on_update_code:
        lua_code.append("function onUpdate(elapsed)\n" + "\n".join(on_update_code) + "\nend\n")

    if not has_green_flag:
        lua_code.append("-- No green flag clicked function! Make sure it has it!\n")

    # Add includes
    includes_code = ""
    if "mouseOverlaps" in includes:
        includes_code += """
function mouseOverlaps(tag)
    addHaxeLibrary('Reflect')
    return runHaxeCode([[
        var obj = game.getLuaObject(']]..tag..[[');
        if (obj == null) obj = Reflect.getProperty(game, ']]..tag..[[');
        if (obj == null) return false;
        return obj.getScreenBounds(null, obj.cameras[0]).containsPoint(FlxG.mouse.getScreenPosition(obj.cameras[0]));
    ]])
end
"""

    return includes_code + on_create_post_header + "".join(on_create_post_code) + "\n".join(lua_code).replace("{sprite_name}", sprite_name)

def convert_project_to_lua(project_path):
    setup_export_folder()
    
    with open(project_path, 'r') as f:
        project = json.load(f)

    for target in project["targets"]:
        if not target["isStage"]:
            sprite_name = target["name"]
            lua_scripts = [f'-- Sprite: {sprite_name}']
            
            # Initialize variables
            variables = {var_id: var_data[0] for var_id, var_data in target["variables"].items()}
            for var_name, var_value in variables.items():
                lua_scripts.append(f'{sprite_name}.{var_value} = 0')  # Assuming initial value is 0
                
            lua_scripts.append(convert_blocks_to_lua(target["blocks"], variables, sprite_name))

            lua_code = "\n".join(lua_scripts)
            with open(f"{EXPORT_FOLDER}/{sprite_name}.lua", "w") as lua_file:
                lua_file.write(lua_code)

# Example usage
project_path = 'project.json'
convert_project_to_lua(project_path)