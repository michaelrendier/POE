#!/usr/bin/env bash
# renders the planning-rig previews next to this file (needs a display; OpenSCAD 2021.01 preview renderer)
cd "$(dirname "$0")"
S=poe_servo_ring.scad
CS=("--colorscheme=Tomorrow Night")
openscad -o rig_overview.png --imgsize=1600,1000 --projection=p "${CS[@]}" --camera=640,0,120,72,0,-38,4300 $S
openscad -o rig_ring_closeup.png --imgsize=1600,1000 --projection=p "${CS[@]}" --camera=200,0,0,68,0,-52,1500 -D 'show_tent=false' -D 'show_wall=false' $S
openscad -o rig_rest_pose.png --imgsize=1600,1000 --projection=p "${CS[@]}" --camera=80,0,0,68,0,-52,1150 -D 'view="rest"' -D 'show_tent=false' $S
openscad -o rig_N18.png --imgsize=1600,1000 --projection=p "${CS[@]}" --camera=200,0,0,68,0,-52,1700 -D 'N=18' -D 'show_tent=false' -D 'show_wall=false' $S
