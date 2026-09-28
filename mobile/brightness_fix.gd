extends Node
## NavcorX mobile: the GL Compatibility renderer (the only one that works on
## phone web browsers - Forward+ shows a black screen on web) renders sky-based
## ambient light and some lights noticeably darker/less reliably than Forward+,
## and how much darker varies by phone/GPU. Scenes that look fine on desktop
## can end up almost solid black on a real phone.
##
## Fix: whenever any scene's WorldEnvironment loads, boost its exposure a bit
## as a safety net, regardless of which specific light is under-rendering.

func _ready() -> void:
	get_tree().node_added.connect(_on_node_added)

func _on_node_added(node: Node) -> void:
	if node is WorldEnvironment:
		var world_env := node as WorldEnvironment
		var env : Environment = world_env.environment
		if is_instance_valid(env):
			env.tonemap_exposure *= 1.8
			env.ambient_light_energy = max(env.ambient_light_energy, 1.0) * 1.8
