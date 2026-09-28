# Applies NavcorX mobile changes to an upstream Adventure Mode checkout (run from the project root).
p='scripts/cam_gantry_playerFollow.gd'
s=open(p).read()
a="""\tif event is InputEventMouseMotion:
\t\t#mouse movement will always reset timer"""
assert a in s; s=s.replace(a,"""\tif event is InputEventMouseMotion and not TouchControls.active:
\t\t#mouse movement will always reset timer""")
b="""\tlook_rotation_vel = disLook * delta * camLookAccell
\tvar default_angle = -20"""
assert b in s; s=s.replace(b,"""\tlook_rotation_vel = disLook * delta * camLookAccell
\t# NavcorX mobile: finger drag on right side of screen turns camera
\tvar touch_look : Vector2 = TouchControls.consume_look()
\tif touch_look != Vector2.ZERO:
\t\tcamTimer = 12.0
\t\tlook_rotation_vel += touch_look * 0.004
\tvar default_angle = -20""",1)
open(p,'w').write(s)
p='project.godot'
s=open(p).read()
reps=[('config/features=PackedStringArray("4.7", "Forward Plus")','config/features=PackedStringArray("4.7", "GL Compatibility")'),
('FAM="*uid://br1uu1gltkc33"','FAM="*uid://br1uu1gltkc33"\nTouchControls="*res://scripts/mobile/touch_controls.gd"'),
('window/stretch/mode="viewport"','window/stretch/mode="canvas_items"'),
('window/size/always_on_top=true\n',''),
('[rendering]\n','[rendering]\n\nrenderer/rendering_method="gl_compatibility"\nrenderer/rendering_method.mobile="gl_compatibility"\nscaling_3d/scale=0.75\nlights_and_shadows/directional_shadow/size=1024\nlights_and_shadows/directional_shadow/size.mobile=1024\nlights_and_shadows/positional_shadow/atlas_size=1024\nlights_and_shadows/positional_shadow/atlas_size.mobile=1024\n'),
# Phones: stream audio instead of decoding every sound fully into memory (the web default); this was crashing iPad Safari.
('buses/default_bus_layout="res://art/audio/default_bus_layout.tres"\n','buses/default_bus_layout="res://art/audio/default_bus_layout.tres"\ngeneral/default_playback_type.web=0\n')]
for x,y in reps:
    assert x in s, x
    s=s.replace(x,y)
# NavcorX mobile: translate the game's own menu text to Chinese.
p='prefabs/UI/menu_rest.tscn'
s=open(p).read()
reps=[('text = "[font_size=30]Adventure Mode[/font_size]"','text = "[font_size=30]冒險模式[/font_size]"'),
('text = "Equipment"','text = "裝備"'),
('text = "Inventory"','text = "物品欄"'),
('text = "Crafting"','text = "合成"'),
('text = "Online"','text = "連線"'),
('text = "Bonfire Ascetic"','text = "營火苦行"'),
('text = "resyoom :)"','text = "返回"')]
for x,y in reps:
    assert x in s, x
    s=s.replace(x,y)
open(p,'w').write(s)

p='prefabs/UI/menu_play_start.tscn'
s=open(p).read()
reps=[('text = "[font_size=30]Adventure Mode[/font_size]"','text = "[font_size=30]冒險模式[/font_size]"'),
('text = "Return"','text = "返回"'),
('text = "Inventory"','text = "物品欄"'),
('text = "Equipment"','text = "裝備"'),
('text = "Crafting"','text = "合成"'),
('text = "Online"','text = "連線"'),
('text = "Messages"','text = "訊息"'),
('text = "Options"','text = "設定"'),
('text = "Quit to Menu"','text = "回主選單"'),
('text = "Quit to Desktop"','text = "結束遊戲"')]
for x,y in reps:
    assert x in s, x
    s=s.replace(x,y)
open(p,'w').write(s)

p='prefabs/UI/menu_crafting.tscn'
s=open(p).read()
reps=[('text = "[font_size=30][i]Crafting[/i][/font_size]"','text = "[font_size=30][i]合成[/i][/font_size]"'),
('text = "resyoom :)"','text = "返回"')]
for x,y in reps:
    assert x in s, x
    s=s.replace(x,y)
open(p,'w').write(s)

p='prefabs/UI/menu_player_equip.tscn'
s=open(p).read()
reps=[('text = "[font_size=30][i]Player Equipment[/i][/font_size]"','text = "[font_size=30][i]裝備[/i][/font_size]"'),
('text = "resyoom :)"','text = "返回"')]
for x,y in reps:
    assert x in s, x
    s=s.replace(x,y)
open(p,'w').write(s)

p='prefabs/UI/menu_player_inventory.tscn'
s=open(p).read()
reps=[('text = "[font_size=30][i]Inventory[/i][/font_size]"','text = "[font_size=30][i]物品欄[/i][/font_size]"'),
('text = "resyoom :)"','text = "返回"'),
('text = "(A) / [Space] : Drop Item\n D-Pad / Arrow Keys: Select Item"','text = "點兩下：丟棄物品\n方向鍵／觸控：選擇道具"')]
for x,y in reps:
    assert x in s, x
    s=s.replace(x,y)
open(p,'w').write(s)

p='scenes/title_scene.tscn'
s=open(p).read()
reps=[('text = "Start"','text = "開始遊戲"'),
('text = "World Test"','text = "世界測試"'),
('text = "Dungeon Test"','text = "地城測試"'),
('text = "Host Online"','text = "建立連線"'),
('text = "Online"','text = "連線"'),
('text = "Options"','text = "設定"'),
('text = "Quit"','text = "結束遊戲"'),
('text = "[center][b][font_size=20]DEBUG OPTIONS[/font_size][/b][/center]"','text = "[center][b][font_size=20]除錯選項[/font_size][/b][/center]"'),
('text = "[center][font_size=14]Level Select[/font_size][/center]"','text = "[center][font_size=14]選擇關卡[/font_size][/center]"')]
for x,y in reps:
    assert x in s, x
    s=s.replace(x,y)
open(p,'w').write(s)

print("patched")
