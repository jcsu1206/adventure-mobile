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
('[rendering]\n','[rendering]\n\nrenderer/rendering_method="gl_compatibility"\nrenderer/rendering_method.mobile="gl_compatibility"\nscaling_3d/scale=0.6\n')]
for x,y in reps:
    assert x in s, x
    s=s.replace(x,y)
open(p,'w').write(s)
print("patched")
