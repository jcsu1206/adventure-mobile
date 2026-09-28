extends CanvasLayer
## NavcorX mobile touch controls (added for phone web play).
## Left half: floating joystick -> p1_move_*.  Right half: drag to look.
## Buttons bottom-right press real input actions.

var active := false
var look_accum := Vector2.ZERO

var _pad : Control
var _joy_index := -1
var _joy_origin := Vector2.ZERO
var _joy_pos := Vector2.ZERO
var _look_index := -1
var _btn_touch := {}   # touch index -> button id
const JOY_R := 110.0

# id, label, action, offset from bottom-right (in px of a 1080-high screen), radius
var buttons := [
    {"label":"ATK",   "action":"p1_attack_light", "off":Vector2(-170,-170), "r":85.0},
    {"label":"JUMP",  "action":"p1_jump",         "off":Vector2(-360,-110), "r":65.0},
    {"label":"ROLL",  "action":"p1_dodge",        "off":Vector2(-150,-370), "r":65.0},
    {"label":"GUARD", "action":"p1_block",        "off":Vector2(-340,-290), "r":55.0},
    {"label":"USE",   "action":"p1_event_action", "off":Vector2(-520,-120), "r":50.0},
]
var top_buttons := [
    {"label":"MENU", "action":"p1_start",     "off":Vector2(-90, 80), "r":45.0},
    {"label":"LOCK", "action":"p1_look_lock", "off":Vector2(-210, 80), "r":45.0},
]
var _all := []
var _pressed := {}

func _ready() -> void:
    layer = 100
    process_mode = Node.PROCESS_MODE_ALWAYS
    active = DisplayServer.is_touchscreen_available() or OS.has_feature("web_android") or OS.has_feature("web_ios")
    _pad = Control.new()
    _pad.set_anchors_preset(Control.PRESET_FULL_RECT)
    _pad.mouse_filter = Control.MOUSE_FILTER_IGNORE
    _pad.draw.connect(_on_draw)
    add_child(_pad)
    _all = buttons + top_buttons
    visible = active
    if active:
        # Touch is emulated as mouse clicks; stop taps from triggering mouse-bound attacks.
        for a in InputMap.get_actions():
            if String(a).begins_with("p1_"):
                for ev in InputMap.action_get_events(a):
                    if ev is InputEventMouseButton:
                        InputMap.action_erase_event(a, ev)

func _scale() -> float:
    return _pad.size.y / 1080.0

func _btn_center(b) -> Vector2:
    var s := _scale()
    var o : Vector2 = b["off"] * s
    var sz := _pad.size
    if b in top_buttons:
        return Vector2(sz.x + o.x, o.y)
    return sz + o

func _hit_button(p: Vector2) -> int:
    var s := _scale()
    for i in _all.size():
        if p.distance_to(_btn_center(_all[i])) <= _all[i]["r"] * s * 1.15:
            return i
    return -1

func _in_game() -> bool:
    # Only grab touches while a player character exists (not on title menus).
    var ps = MgrPlayerSocket.get_player_one() if MgrPlayerSocket.has_method("get_player_one") else null
    return ps != null and is_instance_valid(ps.thrall)

func _input(event: InputEvent) -> void:
    if not active:
        return
    if event is InputEventScreenTouch:
        var p : Vector2 = event.position
        if event.pressed:
            var bi := _hit_button(p)
            if bi >= 0 and _in_game():
                _btn_touch[event.index] = bi
                Input.action_press(_all[bi]["action"])
                _pressed[bi] = true
            elif p.x < _pad.size.x * 0.4 and _joy_index == -1 and _in_game():
                _joy_index = event.index
                _joy_origin = p
                _joy_pos = p
            elif _look_index == -1 and _in_game():
                _look_index = event.index
        else:
            if _btn_touch.has(event.index):
                var bi2 : int = _btn_touch[event.index]
                Input.action_release(_all[bi2]["action"])
                _pressed.erase(bi2)
                _btn_touch.erase(event.index)
            if event.index == _joy_index:
                _joy_index = -1
                _set_move(Vector2.ZERO)
            if event.index == _look_index:
                _look_index = -1
        _pad.queue_redraw()
    elif event is InputEventScreenDrag:
        if event.index == _joy_index:
            _joy_pos = event.position
            var v : Vector2 = (_joy_pos - _joy_origin) / (JOY_R * _scale())
            if v.length() > 1.0:
                v = v.normalized()
            _set_move(v)
            _pad.queue_redraw()
        elif event.index == _look_index:
            look_accum += event.relative / _scale()

func _set_move(v: Vector2) -> void:
    _axis("p1_move_left", -v.x); _axis("p1_move_right", v.x)
    _axis("p1_move_up", -v.y); _axis("p1_move_dn", v.y)

func _axis(action: String, s: float) -> void:
    if s > 0.05:
        Input.action_press(action, clampf(s, 0.0, 1.0))
    else:
        Input.action_release(action)

## Called by the camera each frame; returns drag since last call.
func consume_look() -> Vector2:
    var l := look_accum
    look_accum = Vector2.ZERO
    return l

func _process(_d: float) -> void:
    if active:
        var show := _in_game()
        if _pad.visible != show:
            _pad.visible = show
        _pad.queue_redraw()

func _on_draw() -> void:
    var s := _scale()
    var font := ThemeDB.fallback_font
    if _joy_index != -1:
        _pad.draw_circle(_joy_origin, JOY_R * s, Color(1,1,1,0.12))
        _pad.draw_arc(_joy_origin, JOY_R * s, 0, TAU, 48, Color(1,1,1,0.5), 3.0 * s)
        var knob := _joy_origin + (_joy_pos - _joy_origin).limit_length(JOY_R * s)
        _pad.draw_circle(knob, 45 * s, Color(1,1,1,0.55))
    else:
        var hint := Vector2(330, _pad.size.y / s - 420) * s
        _pad.draw_arc(hint, JOY_R * s, 0, TAU, 48, Color(1,1,1,0.25), 3.0 * s)
        _pad.draw_string(font, hint + Vector2(-40, 10) * s, "MOVE", HORIZONTAL_ALIGNMENT_LEFT, -1, int(26 * s), Color(1,1,1,0.5))
    for i in _all.size():
        var b = _all[i]
        var c := _btn_center(b)
        var r : float = b["r"] * s
        var on := _pressed.has(i)
        _pad.draw_circle(c, r, Color(1,1,1,0.45) if on else Color(0,0,0,0.35))
        _pad.draw_arc(c, r, 0, TAU, 48, Color(1,1,1,0.8), 3.0 * s)
        var fs := int((26 if r > 60 * s else 20) * s)
        var tw := font.get_string_size(b["label"], HORIZONTAL_ALIGNMENT_LEFT, -1, fs).x
        _pad.draw_string(font, c + Vector2(-tw / 2.0, fs * 0.35), b["label"], HORIZONTAL_ALIGNMENT_LEFT, -1, fs, Color.WHITE)
