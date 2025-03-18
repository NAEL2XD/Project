-- Sprite: Sprite1
function onCreatePost()
    makeLuaSprite('stage')
    makeGraphic('stage', 1920, 1080, 'FFFFFF')
    setObjectCamera('stage', 'other')
    addLuaSprite('stage')

    makeLuaSprite('Sprite1', 'Sprite1')
    setObjectCamera('Sprite1', 'other')
    addLuaSprite('Sprite1')
if (((keyboardPressed("ONE") or keyboardPressed("NUMPADONE")) and ((100 > 50)))) then
debugPrint("Sprite1:1: " .. "This works!")end

end
