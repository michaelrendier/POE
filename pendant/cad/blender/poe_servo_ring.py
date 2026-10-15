"""
poe_servo_ring.py -- P.O.E. "free-standing point of light": CONCEPT MOCK-UP of the macro-scale servo ring (Blender 4.x, python3).

Run:   blender -b -P poe_servo_ring.py -- --render          (writes PNG previews next to this file and poe_servo_ring.blend)
       blender -P poe_servo_ring.py                         (opens the model in the UI; lights, cameras and the aperture are named objects)

This is a conceptual 3D representation for engineering discussion before the design moves to OpenSCAD / Fritzing. It is NOT a validated
optical design. Units are millimetres (1 Blender unit = 1 mm). Coordinates: the ring lies in the XY plane, +Z is the forward-out axis of the
pendant (the direction the beams travel), +Y points from the pendant toward the wearer's face.

What it models
  * a steel ring (1/2 in round stock) carrying N independent arms (default 13, an odd number);
  * each arm has THREE axes: pan, tilt and a focus slide, so every arm can aim at one common 3D point and put its beam waist exactly there;
  * a source (633 nm HeNe), a 1x16 polarization-maintaining fibre splitter and a controller / safety board behind the chest plate;
  * the focal point, the beams (through the focus and on to a beam dump), the hard-no cone around the wearer's eye direction, a schematic
    wearer's head, and the multi-tapped copper pancake coil (38 mm OD, 17 turns, 0.8 mm pitch) with its tap markers;
  * an animation that traces a 3D shape with the focal point while the arms move independently in unison;
  * a geometric safety check (no beam direction inside the cone) and a travel check on every frame.

Stated working figures (from the design discussion, unverified here): 633 nm; 13 arms; ~75 uW per arm (~1 mW total); beam waist ~20 um;
lens-to-focus 100 mm. They are annotations; Blender draws geometry, not optics. Visibility of the point in clean air is an OPEN research
question and is not modelled.
"""
import math
import os
import sys

import bpy
from mathutils import Vector

# ───────────────────────── parameters (edit here) ─────────────────────────
N_ARMS = 13
RING_R = 80.0                  # ring radius, mm (arm spacing ~38.7 mm at 13 arms)
STOCK_D = 12.7                 # 1/2 in round stock
FOCAL = Vector((0.0, 0.0, 180.0))   # rest focal point
FOCAL_LEN = 100.0              # lens-to-focus distance, mm (each lens' focal length)
BEAM_EXT = 130.0               # beam continues this far past the focus before the dump
LENS_FRONT = 59.0              # pivot-to-lens-front distance along the optical axis at slide = 0
SLIDE_MIN, SLIDE_MAX = -40.0, 70.0   # carriage travel
KEEPOUT_HALF_ANGLE = 45.0      # degrees, around +Y (toward the wearer's eyes); beams must never point inside it
WEARER_AXIS = Vector((0.0, 1.0, 0.0))
GIMBAL_Z = 32.35               # height of the tilt axis above the ring plane
APERTURE_FSTOP = 2.0           # depth-of-field aperture of Cam_Focus (the 'viewport aperture')
FRAMES = 120
TRACE_AMP = Vector((26.0, 26.0, 28.0))   # amplitude of the traced 3D figure, mm
HERE = os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else os.getcwd()


# ───────────────────────── helpers ─────────────────────────
def mat(name, color, metallic=0.0, rough=0.5, emit=None, strength=0.0, alpha=1.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Metallic"].default_value = metallic
    b.inputs["Roughness"].default_value = rough
    b.inputs["Alpha"].default_value = alpha
    if emit is not None:
        b.inputs["Emission Color"].default_value = (*emit, 1)
        b.inputs["Emission Strength"].default_value = strength
    if alpha < 1:
        m.blend_method = "BLEND" if hasattr(m, "blend_method") else None
    return m


def collection(name):
    c = bpy.data.collections.get(name) or bpy.data.collections.new(name)
    if c.name not in bpy.context.scene.collection.children:
        bpy.context.scene.collection.children.link(c)
    return c


def put(obj, coll, material=None, parent=None, loc=None, rot=None, scale=None):
    for c in list(obj.users_collection):
        c.objects.unlink(obj)
    coll.objects.link(obj)
    if material is not None and hasattr(obj.data, "materials"):
        obj.data.materials.clear()
        obj.data.materials.append(material)
    if parent is not None:
        obj.parent = parent
    if loc is not None:
        obj.location = loc
    if rot is not None:
        obj.rotation_euler = rot
    if scale is not None:
        obj.scale = scale
    return obj


def empty(name, coll, parent=None, loc=(0, 0, 0), rot=(0, 0, 0), kind="PLAIN_AXES", size=3):
    o = bpy.data.objects.new(name, None)
    o.empty_display_type, o.empty_display_size = kind, size
    coll.objects.link(o)
    o.parent, o.location, o.rotation_euler = parent, loc, rot
    return o


def cyl(name, coll, r, depth, material, parent=None, loc=(0, 0, 0), rot=(0, 0, 0), v=40):
    bpy.ops.mesh.primitive_cylinder_add(vertices=v, radius=r, depth=depth, location=(0, 0, 0))
    o = bpy.context.active_object
    o.name = name
    return put(o, coll, material, parent, loc, rot)


def box(name, coll, size, material, parent=None, loc=(0, 0, 0), rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 0, 0))
    o = bpy.context.active_object
    o.name = name
    o.scale = size
    bpy.ops.object.transform_apply(scale=True)
    return put(o, coll, material, parent, loc, rot)


def sphere(name, coll, r, material, loc=(0, 0, 0), seg=32):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=seg, ring_count=seg // 2, radius=r, location=loc)
    o = bpy.context.active_object
    o.name = name
    return put(o, coll, material)


def label(text, coll, loc, size=7.0, color=(1, 1, 1), track=None):
    c = bpy.data.curves.new("txt_" + text[:12], "FONT")
    c.body, c.size, c.align_x = text, size, "CENTER"
    o = bpy.data.objects.new("Label_" + text[:20], c)
    coll.objects.link(o)
    o.location = loc
    o.data.materials.append(mat("LabelWhite", color, rough=0.8, emit=color, strength=1.0))
    if track is not None:
        t = o.constraints.new("TRACK_TO")
        t.target, t.track_axis, t.up_axis = track, "TRACK_Z", "UP_Y"
    return o


def aim(pivot_xyz, point):
    """pan (about +Z), tilt (about local +Y, negative elevation) and distance for an arm whose tilt axis passes through pivot_xyz."""
    d = point - pivot_xyz
    L = d.length
    d /= L
    return math.atan2(d.y, d.x), math.asin(d.z), L, d


# ───────────────────────── scene ─────────────────────────
def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system, sc.unit_settings.scale_length, sc.unit_settings.length_unit = "METRIC", 0.001, "MILLIMETERS"
    sc.frame_start, sc.frame_end = 1, FRAMES
    sc.world = bpy.data.worlds.new("World")
    sc.world.use_nodes = True
    sc.world.node_tree.nodes["Background"].inputs[0].default_value = (0.012, 0.014, 0.02, 1)

    C = {n: collection(n) for n in ("Ring", "Arms", "Beams", "Electronics", "Safety", "Wearer", "Coil", "Lights", "Cameras", "Labels")}
    steel = mat("Steel", (0.55, 0.57, 0.6), 1.0, 0.35)
    dark = mat("DarkAlu", (0.08, 0.09, 0.11), 0.8, 0.45)
    alu = mat("Aluminium", (0.7, 0.72, 0.75), 0.9, 0.3)
    glass = mat("Lens", (0.6, 0.8, 1.0), 0.0, 0.05, alpha=0.5)
    redbeam = mat("RedBeam", (1, 0.02, 0.01), 0.0, 0.5, emit=(1.0, 0.03, 0.01), strength=18.0)
    dot = mat("FocalDot", (1, 0.6, 0.5), 0.0, 0.3, emit=(1.0, 0.45, 0.35), strength=120.0)
    fiber = mat("Fibre", (0.95, 0.7, 0.1), 0.0, 0.4)
    board = mat("Board", (0.05, 0.25, 0.1), 0.2, 0.5)
    copper = mat("Copper", (0.85, 0.42, 0.22), 1.0, 0.25)
    cone_m = mat("KeepOutCone", (1.0, 0.3, 0.0), 0.0, 0.8, emit=(1.0, 0.25, 0.0), strength=0.25, alpha=0.05)
    skin = mat("Wearer", (0.5, 0.35, 0.3), 0.0, 0.7)
    dump = mat("BeamDump", (0.02, 0.02, 0.025), 0.0, 1.0, alpha=0.3)
    chest = mat("ChestPlate", (0.18, 0.2, 0.24), 0.3, 0.6)

    # ring (1/2 in round stock)
    bpy.ops.mesh.primitive_torus_add(major_radius=RING_R, minor_radius=STOCK_D / 2, major_segments=128, minor_segments=24)
    ring = put(bpy.context.active_object, C["Ring"], steel)
    ring.name = "Ring_steel_half_inch"
    # chest / mounting plate behind the ring
    cyl("ChestPlate", C["Ring"], 125.0, 4.0, chest, loc=(0, 0, -30.0), v=96)
    # three spokes tie the ring to the plate
    for k in range(3):
        a = 2 * math.pi * k / 3 + math.pi / 6
        cyl(f"Spoke_{k}", C["Ring"], 4.0, 30.0, steel, loc=(RING_R * math.cos(a), RING_R * math.sin(a), -15.0), v=16)

    # focal point (target), moved by animation
    focal = sphere("FocalPoint", C["Beams"], 1.8, dot, tuple(FOCAL))
    fl = bpy.data.lights.new("Light_FocalPoint", "POINT")
    fl.color, fl.energy, fl.shadow_soft_size = (1.0, 0.1, 0.05), 2500.0, 2.0
    fo = bpy.data.objects.new("Light_FocalPoint", fl)
    C["Lights"].objects.link(fo)
    fo.parent = focal

    arms = []
    lens_world = []
    for i in range(N_ARMS):
        phi = 2 * math.pi * i / N_ARMS + math.pi / 2          # arm 0 on the +Y (toward-the-face) side
        bx, by = RING_R * math.cos(phi), RING_R * math.sin(phi)
        top = STOCK_D / 2
        base = box(f"Arm{i:02d}_base", C["Arms"], (22, 22, 10), dark, loc=(bx, by, top + 5), rot=(0, 0, phi))
        pan = empty(f"Arm{i:02d}_pan", C["Arms"], loc=(bx, by, top + 10))
        cyl(f"Arm{i:02d}_pandisc", C["Arms"], 13, 6, alu, parent=pan, loc=(0, 0, 3), v=36)
        for s in (-1, 1):
            box(f"Arm{i:02d}_yoke{'LR'[s > 0]}", C["Arms"], (14, 3, 22), alu, parent=pan, loc=(0, s * 11.5, 16))
        tilt = empty(f"Arm{i:02d}_tilt", C["Arms"], parent=pan, loc=(0, 0, GIMBAL_Z - (top + 10)))
        cyl(f"Arm{i:02d}_trunnion", C["Arms"], 3.0, 26, steel, parent=tilt, rot=(math.pi / 2, 0, 0), v=20)
        box(f"Arm{i:02d}_rail", C["Arms"], (SLIDE_MAX - SLIDE_MIN + 30, 10, 7), dark, parent=tilt,
            loc=((SLIDE_MAX + SLIDE_MIN + 30) / 2, 0, 0))
        car = empty(f"Arm{i:02d}_carriage", C["Arms"], parent=tilt, loc=(0, 0, 0), kind="ARROWS", size=4)
        box(f"Arm{i:02d}_carriageblock", C["Arms"], (26, 14, 12), alu, parent=car, loc=(13, 0, 0))
        cyl(f"Arm{i:02d}_collimator", C["Arms"], 6.5, 34, steel, parent=car, loc=(37, 0, 0), rot=(0, math.pi / 2, 0), v=28)
        cyl(f"Arm{i:02d}_lens", C["Arms"], 9, 3.5, glass, parent=car, loc=(LENS_FRONT - 1.75, 0, 0), rot=(0, math.pi / 2, 0), v=40)
        beam = cyl(f"Arm{i:02d}_beam", C["Beams"], 0.3, 1.0, redbeam, parent=car, v=8)
        # cylinder of depth 1 centred on its origin: shift so the origin is at the beam start, then stretch along the axis
        beam.data.transform(__import__("mathutils").Matrix.Translation((0, 0, 0.5)))
        beam.rotation_euler = (0, math.pi / 2, 0)
        beam.location = (LENS_FRONT, 0, 0)
        beam.scale = (1, 1, FOCAL_LEN + BEAM_EXT)
        # fibre from the splitter to this arm (service loop not modelled)
        cv = bpy.data.curves.new(f"Fibre{i:02d}", "CURVE")
        cv.dimensions, cv.bevel_depth, cv.bevel_resolution = "3D", 0.9, 3
        sp = cv.splines.new("POLY")
        pts = [(0, 0, -62), (0.45 * bx, 0.45 * by, -45), (0.9 * bx, 0.9 * by, -18), (bx, by, top + 4)]
        sp.points.add(len(pts) - 1)
        for p, c in zip(sp.points, pts):
            p.co = (*c, 1)
        fo_ = bpy.data.objects.new(f"Fibre{i:02d}", cv)
        C["Electronics"].objects.link(fo_)
        fo_.data.materials.append(fiber)
        arms.append(dict(i=i, pan=pan, tilt=tilt, car=car, pivot=Vector((bx, by, GIMBAL_Z))))

    # electronics stack behind the chest plate
    box("Splitter_1x16_PM", C["Electronics"], (84, 44, 22), board, loc=(0, 0, -62))
    cyl("HeNe_633nm", C["Electronics"], 17, 250, alu, loc=(0, 0, -105), rot=(0, math.pi / 2, 0), v=40)
    box("Controller_and_SafetyMCU", C["Electronics"], (70, 50, 12), board, loc=(120, 0, -62))
    # beam dump / baffle
    dump_z = FOCAL.z + FOCAL_LEN + 0  # beams end ~BEAM_EXT beyond the focus; the dump sits beyond that
    cyl("BeamDump", C["Safety"], 140, 3, dump, loc=(0, 0, FOCAL.z + BEAM_EXT + 30), v=80)

    # hard-no cone around +Y (apex at the pendant centre)
    depth = 330.0
    r_base = depth * math.tan(math.radians(KEEPOUT_HALF_ANGLE))
    bpy.ops.mesh.primitive_cone_add(vertices=96, radius1=r_base, radius2=0, depth=depth, location=(0, 0, 0))
    cone = bpy.context.active_object
    cone.name = "KeepOutCone_45deg_toward_eyes"
    cone.data.transform(__import__("mathutils").Matrix.Translation((0, 0, -depth / 2)))   # apex at the origin, base at z = -depth
    put(cone, C["Safety"], cone_m, rot=(math.pi / 2, 0, 0))                                 # base toward +Y
    wf = cone.modifiers.new("edges", "WIREFRAME")
    wf.thickness = 0.6
    # schematic wearer: head with eyes, behind the chest plane
    sphere("Wearer_head_schematic", C["Wearer"], 55, skin, (0, 345, -60))
    for s in (-1, 1):
        sphere(f"Wearer_eye_{'LR'[s > 0]}", C["Wearer"], 5, mat("Eye", (0.9, 0.9, 0.95)), (s * 24, 345, -8), seg=16)

    # copper pancake coil: 17 turns, OD 38, ID ~10, pitch 0.8, 0.5 mm trace; placed beside the ring on its own display plate, to scale
    cx, cy, cz = -200.0, -20.0, 0.0
    cv = bpy.data.curves.new("PancakeCoil", "CURVE")
    cv.dimensions, cv.bevel_depth, cv.bevel_resolution, cv.resolution_u = "3D", 0.25, 3, 12
    sp = cv.splines.new("POLY")
    n_per_turn, turns, r0, pitch = 72, 17, 5.0, 0.8
    sp.points.add(n_per_turn * turns)
    for k, p in enumerate(sp.points):
        th = 2 * math.pi * k / n_per_turn
        r = r0 + pitch * th / (2 * math.pi)
        p.co = (cx + r * math.cos(th), cy + r * math.sin(th), cz, 1)
    co = bpy.data.objects.new("PancakeCoil_copper", cv)
    C["Coil"].objects.link(co)
    co.data.materials.append(copper)
    cyl("CoilPlate", C["Coil"], 26, 1.6, board, loc=(cx, cy, cz - 1.2), v=64)

    def coil_pt(turns_from_inside):
        th = 2 * math.pi * turns_from_inside
        r = r0 + pitch * turns_from_inside
        return (cx + r * math.cos(th), cy + r * math.sin(th), cz)
    for nm, t_ in (("tap_inner3_SWhigh", 3), ("tap_inner5_FM", 5), ("tap_outer5_NFC", 12), ("tap_full_17T", 17)):
        sphere("Coil_" + nm, C["Coil"], 1.1, mat("Tap", (1, 0.95, 0.2), emit=(1, 0.9, 0.1), strength=2.0), coil_pt(t_), seg=12)

    # lights (separate named objects, edit energy / colour / position freely)
    for name, kind, loc, energy, col, size in (
            ("Light_Key", "AREA", (350, -300, 420), 220000.0, (1.0, 0.95, 0.9), 200),
            ("Light_Fill", "AREA", (-380, -150, 220), 90000.0, (0.7, 0.8, 1.0), 260),
            ("Light_Rim", "AREA", (0, 380, 300), 120000.0, (0.9, 0.95, 1.0), 220)):
        ld = bpy.data.lights.new(name, kind)
        ld.energy, ld.size = energy, size
        ld.color = col
        lo = bpy.data.objects.new(name, ld)
        lo.location = loc
        C["Lights"].objects.link(lo)
        t = lo.constraints.new("TRACK_TO")
        t.target = focal
        t.track_axis, t.up_axis = "TRACK_NEGATIVE_Z", "UP_Y"

    # cameras (Cam_Focus carries the depth-of-field aperture)
    def cam(name, loc, target, ortho=None, lens=35.0, dof=False):
        cd = bpy.data.cameras.new(name)
        cd.lens, cd.clip_end = lens, 5000
        if ortho:
            cd.type, cd.ortho_scale = "ORTHO", ortho
        if dof:
            cd.dof.use_dof, cd.dof.focus_object, cd.dof.aperture_fstop = True, focal, APERTURE_FSTOP
        co_ = bpy.data.objects.new(name, cd)
        co_.location = loc
        C["Cameras"].objects.link(co_)
        t = co_.constraints.new("TRACK_TO")
        t.target, t.track_axis, t.up_axis = target, "TRACK_NEGATIVE_Z", "UP_Y"
        return co_
    mid = empty("Target_mid", C["Cameras"], loc=(-20, 0, 70))
    cam("Cam_Overview", (430, -520, 330), mid, lens=32)
    cam("Cam_Focus", (70, -105, FOCAL.z + 18), focal, lens=85, dof=True)
    cam("Cam_Side", (-700, 0, 150), mid, ortho=520)
    cam("Cam_Top", (0, 0, 800), empty("Target_top", C["Cameras"], loc=(0, 0, 0)), ortho=330)
    iso_t = empty("Target_iso", C["Cameras"], loc=(-20, 0, 150))
    k = 900 / math.sqrt(3)            # true isometric: camera on the (1,-1,1) diagonal, elevation 35.264 deg
    cam("Cam_Iso", (-20 + k, -k, 150 + k), iso_t, ortho=820)
    sc.camera = bpy.data.objects["Cam_Overview"]
    lb = bpy.data.objects["Cam_Overview"]
    label("Steel ring, 1/2 in stock, 13 arms x 3 axes (pan / tilt / focus slide)", C["Labels"], (0, -130, -12), 8, track=lb)
    label("633 nm HeNe + 1x16 PM splitter", C["Labels"], (0, 0, -150), 7, track=lb)
    label("hard-no cone 45 deg", C["Labels"], (0, 250, 130), 9, (1, 0.5, 0.1), track=lb)
    label("wearer's head (schematic)", C["Labels"], (0, 345, 15), 8, track=lb)
    label("copper pancake coil 38 mm OD, 17 T, taps", C["Labels"], (cx, cy - 36, 0), 6, track=lb)
    label("beam dump", C["Labels"], (0, 0, FOCAL.z + BEAM_EXT + 52), 8, track=lb)
    return focal, arms


# ───────────────────────── motion, checks, animation ─────────────────────────
def pose(arms, target, frame=None):
    """put every arm on `target`; returns per-arm (pan, tilt, slide, min angle to the wearer axis)."""
    rows = []
    for a in arms:
        pan_a, el, L, d = aim(a["pivot"], target)
        slide = L - FOCAL_LEN - LENS_FRONT
        a["pan"].rotation_euler = (0, 0, pan_a)
        a["tilt"].rotation_euler = (0, -el, 0)
        a["car"].location = (slide, 0, 0)
        ang = math.degrees(d.angle(WEARER_AXIS))
        rows.append((a["i"], math.degrees(pan_a), math.degrees(el), slide, ang))
        if frame is not None:
            a["pan"].keyframe_insert("rotation_euler", index=2, frame=frame)
            a["tilt"].keyframe_insert("rotation_euler", index=1, frame=frame)
            a["car"].keyframe_insert("location", index=0, frame=frame)
    return rows


def figure(t):
    """closed 3D figure traced by the focal point (a Lissajous knot), t in [0, 2*pi)"""
    return FOCAL + Vector((TRACE_AMP.x * math.sin(2 * t), TRACE_AMP.y * math.sin(3 * t + 1.0), TRACE_AMP.z * math.sin(t + 0.4)))


def check_and_animate(focal, arms):
    worst_angle, worst_slide = 180.0, [1e9, -1e9]
    pts = []
    for f in range(1, FRAMES + 1):
        p = figure(2 * math.pi * (f - 1) / FRAMES)
        focal.location = p
        focal.keyframe_insert("location", frame=f)
        rows = pose(arms, p, frame=f)
        worst_angle = min(worst_angle, min(r[4] for r in rows))
        worst_slide = [min(worst_slide[0], min(r[3] for r in rows)), max(worst_slide[1], max(r[3] for r in rows))]
        pts.append(p)
    # keep-out check on the beams' RAYS beyond the housing (r > RING_R + 30): none may enter the cone
    cos_lim = math.cos(math.radians(KEEPOUT_HALF_ANGLE))
    violations = 0
    for a in arms:
        for f in (1, FRAMES // 4, FRAMES // 2, 3 * FRAMES // 4):
            _, _, L, d = aim(a["pivot"], figure(2 * math.pi * (f - 1) / FRAMES))
            for s in range(0, 700, 10):
                q = a["pivot"] + d * s
                if q.length > RING_R + 30 and (q / q.length).dot(WEARER_AXIS) > cos_lim:
                    violations += 1
    # lens spacing at the rest pose
    pose(arms, FOCAL)
    focal.location = FOCAL
    lens = [a["pivot"] + aim(a["pivot"], FOCAL)[3] * (aim(a["pivot"], FOCAL)[2] - FOCAL_LEN) for a in arms]
    gap = min((lens[i] - lens[j]).length for i in range(len(lens)) for j in range(i))
    # traced path as a curve
    cv = bpy.data.curves.new("TracedPath", "CURVE")
    cv.dimensions, cv.bevel_depth = "3D", 0.35
    sp = cv.splines.new("POLY")
    sp.points.add(len(pts))
    for p_, q in zip(sp.points, pts + [pts[0]]):
        p_.co = (*q, 1)
    o = bpy.data.objects.new("TracedPath", cv)
    bpy.data.collections["Beams"].objects.link(o)
    o.data.materials.append(bpy.data.materials["FocalDot"])
    print("SAFETY/TRAVEL CHECK over %d frames:" % FRAMES)
    print("  smallest angle between any beam direction and the wearer axis: %.1f deg (limit %.0f) -> %s" %
          (worst_angle, KEEPOUT_HALF_ANGLE, "PASS" if worst_angle > KEEPOUT_HALF_ANGLE else "FAIL"))
    print("  beam-ray points inside the cone beyond the housing: %d -> %s" % (violations, "PASS" if violations == 0 else "FAIL"))
    print("  carriage travel needed: %.1f .. %.1f mm (available %.0f .. %.0f) -> %s" %
          (worst_slide[0], worst_slide[1], SLIDE_MIN, SLIDE_MAX, "PASS" if SLIDE_MIN <= worst_slide[0] and worst_slide[1] <= SLIDE_MAX else "OUT OF TRAVEL"))
    print("  smallest lens-to-lens centre spacing at rest: %.1f mm (lens ring diameter 18 mm)" % gap)


def render(path_prefix, frames=((1, "Cam_Overview"), (1, "Cam_Focus"), (1, "Cam_Side"), (1, "Cam_Top"), (30, "Cam_Overview")), res=(1280, 720)):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES"
    sc.cycles.device, sc.cycles.samples = "CPU", 64
    sc.cycles.use_denoising = False
    sc.render.resolution_x, sc.render.resolution_y = res
    sc.render.image_settings.file_format = "PNG"
    for fr, cam_name in frames:
        sc.frame_set(fr)
        sc.camera = bpy.data.objects[cam_name]
        sc.render.filepath = f"{path_prefix}_{cam_name}_f{fr:03d}.png"
        bpy.ops.render.render(write_still=True)
        print("rendered", sc.render.filepath)


if __name__ == "__main__":
    focal, arms = build()
    check_and_animate(focal, arms)
    bpy.context.scene.frame_set(1)
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(HERE, "poe_servo_ring.blend"))
    if "--iso" in sys.argv:
        render(os.path.join(HERE, "preview"), frames=((1, "Cam_Iso"),), res=(1400, 1100))
    elif "--render" in sys.argv:
        render(os.path.join(HERE, "preview"))
