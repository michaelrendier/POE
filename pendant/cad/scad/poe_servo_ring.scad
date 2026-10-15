// poe_servo_ring.scad -- P.O.E. free-standing point of light: WALL-MOUNTED PLANNING RIG (concept, full scale, millimetres)
// OpenSCAD (GPL-2+ with CGAL exception). Not a proof of concept: a drafted CAD concept for engineers to plan against.
//
// Frame: the wall is the plane z = 0 - 40; the ring lies in z = 0 (parallel to the wall); beams travel +z into the room.
// Ring: 1/2 in (12.7 mm) round steel. N arms on it; ring_d = 0 computes the diameter from the arm pitch.
// Each arm = coarse PAN servo (axis along +z) + coarse TILT servo + a lens tube with a 3-axis FIBRE-TIP POSITIONER behind a fixed lens
// (fine steering by lateral fibre shift, focus by axial fibre shift; piezo-class, TBD). Servo bodies are stand-in boxes at published
// nominal sizes (ROBOTIS DYNAMIXEL XL330-M288-T: 20 x 34 x 26 mm, as quoted by resellers; verify on the vendor drawing / STEP).
// Parts marked "nominal" are stand-ins, not vendor models.  See README.md in this folder.
//
// Render:  openscad -o rig.png --imgsize=1600,1000 --camera=... poe_servo_ring.scad          (see render.sh)
//          -D 'view="rest"'   all arms along +z      -D 'target=[x,y,z]'  where the focal point is      -D 'N=18'

N          = 13;          // arms (13 or 18 in the plan)
pitch      = 48;          // mm of ring per arm (servo + swept tube footprint)
ring_d     = 0;           // ring centre-line diameter, mm; 0 = N * pitch / PI
stock_d    = 12.7;        // 1/2 in round stock
target     = [140, 60, 700];      // focal point, mm (up to ~1220 mm = 4 ft)
view       = "aimed";     // "aimed" or "rest"
show_tent  = true;        // fog test enclosure (peasoup-fog scatter volume) and beam dump
show_wall  = true;
room       = true;        // true: draw the room frame (depth horizontal, y up) so the wall is vertical; false: raw frame (+z out of the ring)
show_sensor= true;        // pinhole photodiode that watches the fog-lit focal point (phase-lock feedback)
beam_ext   = 160;         // beams continue past the focus by this much
tent_d     = 1300;        // test enclosure depth, mm

R   = (ring_d > 0 ? ring_d : N * pitch / PI) / 2;
PZ  = 120;                // z of every tilt axis
LT  = 100;                // tilt axis to lens front, along the optical axis
$fn = 36;

// ---------- nominal stand-in parts ----------
module servo_xl330() {                    // 20 x 26 x 34 mm body, horn on top (z); nominal stand-in
  color("#2b2b30") translate([-10, -13, 0]) cube([20, 26, 34]);
  color("#c8c8cc") translate([0, 0, 34]) cylinder(d = 17, h = 3);
}
module lens_tube() {                      // lens tube, 32 mm OD, + 25.4 mm lens
  color("#8a8d93") rotate([0, 0, 0]) cylinder(d = 32, h = LT - 6);
  color("#cfe6ff", 0.6) translate([0, 0, LT - 6]) cylinder(d = 25.4, h = 5);
}
module fibre_positioner() {               // 3-axis fibre-tip positioner (XY fine + Z focus), TBD piezo-class; nominal block
  color("#3a4f7a") translate([-20, -20, -48]) cube([40, 40, 46]);
  color("#d9a441") translate([0, 0, -80]) cylinder(d = 3, h = 34);      // fibre lead
}
module ring() { color("#6b6e75") rotate_extrude($fn = 160) translate([R, 0]) circle(d = stock_d, $fn = 24); }
module standoffs() {
  for (a = [45, 135, 225, 315]) color("#9a9ea6") translate([R * cos(a), R * sin(a), -40]) cylinder(d = 10, h = 40);
}
module line(p1, p2, r = 0.8) {            // thin cylinder from p1 to p2
  d = p2 - p1; L = norm(d);
  translate(p1) rotate([0, acos(d[2] / L), atan2(d[1], d[0])]) cylinder(r = r, h = L, $fn = 8);
}

// ---------- one arm ----------
module arm(i) {
  a  = 360 * i / N;
  c  = [R * cos(a), R * sin(a), 0];
  P  = [c[0], c[1], PZ];
  d  = target - P;  L = norm(d);
  psi = view == "aimed" ? acos(d[2] / L) : 0;
  phi = view == "aimed" ? atan2(d[1], d[0]) : a;
  u   = view == "aimed" ? d / L : [0, 0, 1];
  // ring clamp and pan servo (axis +z)
  color("#9a9ea6") translate([c[0], c[1], 0]) rotate([0, 0, a]) translate([-14, -12, stock_d / 2]) cube([28, 24, 6]);
  translate([c[0], c[1], stock_d / 2 + 6]) rotate([0, 0, a]) servo_xl330();
  // pan plate + posts up to the tilt servo
  translate([c[0], c[1], stock_d / 2 + 6 + 37]) rotate([0, 0, phi]) {
    color("#c8c8cc") translate([-15, -15, 0]) cube([30, 30, 3]);
    for (s = [-1, 1]) color("#c8c8cc") translate([-3, s * 14 - 1.5, 3]) cube([6, 3, PZ - (stock_d / 2 + 6 + 37) - 3 + 17]);
  }
  // tilt servo, lens tube, fibre positioner on the tilt axis P
  translate(P) rotate([0, 0, phi]) {
    color("#2b2b30") translate([-13, -10, -17]) cube([26, 20, 34]);        // tilt servo (axis along y), nominal
    rotate([0, psi, 0]) { lens_tube(); fibre_positioner(); }
  }
  // beam: lens front -> target -> beyond
  p1 = P + u * LT;
  color("#ff1a1a") line(p1, target + (target - p1) / norm(target - p1) * beam_ext, 0.9);
}

// ---------- scene ----------
module world() {
  ring(); standoffs();
  for (i = [0 : N - 1]) arm(i);
  color("#fff1a8") translate(target) sphere(r = 9, $fn = 24);               // focal point
  if (show_wall) color("#d8d4cc", 0.35) translate([-700, -700, -44]) cube([1400, 1400, 4]);
  if (show_tent) {
    color("#aee3ff", 0.07) translate([-520, -520, -40]) cube([1040, 1040, tent_d + 40]);                    // fog enclosure (clear)
    color("#101014") translate([0, 0, tent_d + 20]) cylinder(d = 700, h = 6);                                  // beam dump
    color("#555a63") translate([-440, -520, 120]) cube([120, 70, 70]);                                            // fog machine (on the floor of the tent)
    color("#2f3a4a") translate([620, -60, target[2] - 40]) cube([90, 60, 90]);                                 // test camera on a stand
  }
  if (show_sensor) {
    color("#6a8fb5") translate([300, -360, target[2]]) rotate([0, 90, 25]) cylinder(d = 28, h = 90);      // photodiode + collection lens
    line([300, -360, target[2]], target, 0.4);
  }
}

// raw frame -> room frame: X' = z (depth), Y' = x (lateral), Z' = y (up)
if (room) multmatrix([[0,0,1,0],[1,0,0,0],[0,1,0,0],[0,0,0,1]]) world(); else world();
