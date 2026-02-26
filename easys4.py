import argparse
import sys
import numpy as np

from helpers.gcode import read_file
from helpers.coord import to_xyz
from post.vis import vis_toolpaths

def test_gcode(file_name):
    print(f"--- Testing G-Code for: {file_name} ---")
    return "G-Code data preview..."

def handle_s4(args):
    print(f"Slicing with S4: {args.file_path} @ {args.layer_height}mm")

# --- Action Placeholders ---
def handle_xyz(args):
    print(f"Slicing XYZ: {args.file_path} @ {args.layer_height}mm")

def handle_crt(args):
    print(f"Slicing Custom: {args.file_path} @ {args.layer_height}mm")

def handle_scale(args):
    print(f"Scaling Extrusion: {args.file_path} by factor {args.extrusion_scale}")

def handle_vis(args):
    print(f"Visualizing: {args.file_path}")
    coords = read_file(args.file_path, args.coordinate_type)
    if args.coordinate_type == 'crt':
        tmp = []
        for coord in coords:
            tmp.append(to_xyz(coord))
        coords = np.array(tmp)
    print(tmp)
    vis_toolpaths(coords)


def main():
    parser = argparse.ArgumentParser(description="EasyS4, S4_Slicer utility")
    
    # Create the subparser object
    subparsers = parser.add_subparsers(dest="action", required=True, help="Available actions")
    
    parser_s4 = subparsers.add_parser("s4", help="Slice using S4 Slicer")
    parser_s4.add_argument("file_path", help="Path to input file")
    parser_s4.add_argument("layer_height", type=float, help="Layer height in mm")
    parser_s4.set_defaults(func=handle_xyz)

    parser_xyz = subparsers.add_parser("xyz", help="Slice from polar to xyz")
    parser_xyz.add_argument("file_path", help="Path to input file")
    parser_xyz.add_argument("layer_height", type=float, help="Layer height in mm")
    parser_xyz.add_argument("--no-nonplanar", action="store_false", dest="nonplanar", default=True)
    parser_xyz.set_defaults(func=handle_xyz)

    # --- 2. CRT Sub-command ---
    parser_crt = subparsers.add_parser("crt", help="Slice from Core-R-Theta to xyz")
    parser_crt.add_argument("file_path", help="Path to input file")
    parser_crt.add_argument("layer_height", type=float, help="Layer height in mm")
    parser_crt.set_defaults(func=handle_crt)

    # --- 3. SCALE_E Sub-command ---
    parser_scale = subparsers.add_parser("scale_e", help="Scale extrusions only")
    parser_scale.add_argument("file_path", help="Path to input file")
    parser_scale.add_argument("-e", "--extrusion", type=float, required=True, dest="extrusion_scale", help="Scaling factor")
    parser_scale.set_defaults(func=handle_scale)

    # --- 4. VIS Sub-command ---
    parser_vis = subparsers.add_parser("vis", help="Visualize toolpaths")
    parser_vis.add_argument("file_path", help="Path to input file")
    parser_vis.add_argument("coordinate_type", help="xyz: Cartesian, crt: Core-R-Theta")
    parser_vis.set_defaults(func=handle_vis)

    # Parse arguments
    args = parser.parse_args()

    # Run the test function you provided
    print(test_gcode(args.file_path))

    # Execute the function associated with the sub-command
    args.func(args)

if __name__ == "__main__":
    main()