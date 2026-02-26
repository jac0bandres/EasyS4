import argparse
import sys

from helpers.gcode import read_file

def test_gcode(file_name):
    test = read_file(file_name, 'xyz')
    print(test)

def main():
    # Initialize the parser
    parser = argparse.ArgumentParser(
        description="EasyS4, S4_Slicer utility"
    )

    parser.add_argument(
        "file_path", 
        help="Path to the input .stl file"
    )

    parser.add_argument(
        "layer_height", 
        type=float, 
        help="The thickness of each layer in mm"
    )

    parser.add_argument(
        "-e", "--extrusion", 
        type=float, 
        dest="extrusion_scale",
        help="Optional scaling factor for extrusion (e.g., 1.05 for 105%%)"
    )

    parser.add_argument(
        "--no-nonplanar", 
        action="store_false", 
        dest="nonplanar",
        help="Disable nonplanar slicing (enabled by default)"
    )
    parser.set_defaults(nonplanar=True)

    args = parser.parse_args()

    print("--- Configuration Loaded ---")
    print(f"File Path:       {args.file_path}")
    print(f"Layer Height:    {args.layer_height}")
    print(f"Extrusion Scale: {args.extrusion_scale if args.extrusion_scale else 'Default'}")
    print(f"Nonplanar:       {args.nonplanar}")

    print(test_gcode(args.file_path))

if __name__ == "__main__":
    main()