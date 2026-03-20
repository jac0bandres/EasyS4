import argparse
import numpy as np
import subprocess
from helpers.gcode import S4_DF

from helpers.gcode import read_gcode_file
from helpers.coord import to_xyz
from slicer.cura_config import update_cura_config, update_layer_height
from slicer.S4 import s4_slice
from post.vis import vis_toolpaths, vis_extrusion, vis_deltas
from post.extrusion_scale import scale_e

def test_gcode(file_name):
    print(f"--- Testing G-Code for: {file_name} ---")
    return "G-Code data preview..."

def handle_s4(args):
    print(f"Slicing with S4: {args.file_path}")
    s4_slice(args.file_path)

# --- Action Placeholders ---
def handle_xyz(args):
    print(f"Slicing XYZ: {args.file_path} @ {args.layer_height}mm")

def handle_crt(args):
    print(f"Slicing Custom: {args.file_path} @ {args.layer_height}mm")

def handle_scale(args):
    print(f"Scaling Extrusion: {args.file_path} by factor {args.extrusion_scale}")
    scale_e(args.file_path, args.extrusion_scale)

def handle_vis(args):
    print(f"Visualizing: {args.file_path}")
    s4_df = S4_DF(args.file_path, args.b_len)
    if args.type == 'toolpaths':
        vis_toolpaths(s4_df.df.xyz)
    if args.type == 'extrusion':
        vis_extrusion(s4_df.df.xyz)
    if args.type == 'delta':
        vis_deltas(s4_df.df.xyz) 

def handle_config(args):
    if args.update:
        update_cura_config(src=args.update)
    if args.layer_height:
        update_layer_height(args.layer_height)

def main():
    parser = argparse.ArgumentParser(description="EasyS4, S4_Slicer utility")
    
    # Create the subparser object
    subparsers = parser.add_subparsers(dest="action", required=True, help="Available actions")
    
    parser_s4 = subparsers.add_parser("s4", help="Slice using S4 Slicer")
    parser_s4.add_argument("file_path", help="Path to input file")
    parser_s4.set_defaults(func=handle_s4)

    parser_config= subparsers.add_parser("config", help="Config utility")
    parser_config.add_argument("-u", "--update", type=str, help="Settings json")
    parser_config.add_argument("-l", "--layer_height", type=str, help="Layer height")
    parser_config.set_defaults(func=handle_config)

    parser_xyz = subparsers.add_parser("xyz", help="Transform from polar to xyz")
    parser_xyz.add_argument("file_path", help="Path to input file")
    parser_xyz.set_defaults(func=handle_xyz)

    parser_crt = subparsers.add_parser("crt", help="Slice from Core-R-Theta to xyz")
    parser_crt.add_argument("file_path", help="Path to input file")
    parser_crt.add_argument("layer_height", type=float, help="Layer height in mm")
    parser_crt.set_defaults(func=handle_crt)

    parser_scale = subparsers.add_parser("scale_e", help="Scale extrusions only")
    parser_scale.add_argument("file_path", help="Path to input file")
    parser_scale.add_argument("-e", "--extrusion", type=float, required=True, dest="extrusion_scale", help="Scaling factor")
    parser_scale.set_defaults(func=handle_scale)

    parser_vis = subparsers.add_parser("vis", help="Visualize toolpaths")
    parser_vis.add_argument("-t", "--type", type=str, help="Type of visualization you'd like to perform. 'extrusion', 'toolpath'")
    parser_vis.add_argument("file_path", help="Path to input file")
    parser_vis.add_argument("-b", "--b_len", type=float, help="b_len: length of B nozzle fron hinge to tip (mm)")
    parser_vis.set_defaults(func=handle_vis)

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()