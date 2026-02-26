# General gcode reader
import numpy as np
from pygcode import Line

def read_file(file_path: str, coordinate: str):
    with open(file_path, 'r') as fh:
        coords = []
        prev_gcode = {'X': 0, 'Y': 0, 'Z': 0, 'C': 0, 'B': 0} # i hate to use a dict here but oh well
        for line_text in fh:
            line_text = line_text.strip()
            if not line_text or line_text.startswith(';'):
                continue

            line = Line(line_text)
            # using lists and defining propeties by their index to reduce overhead
            if not line.block.gcodes:
                continue

            for gcode in sorted(line.block.gcodes):
                if gcode.word not in ('G01', 'G00'):
                    continue 
                if coordinate == "xyz":
                    x = gcode.X if gcode.X is not None else prev_gcode['X']

                    if coordinate == "xyz":
                        y = gcode.Y if gcode.Y is not None else prev_gcode['Y']
                        z = gcode.Z if gcode.Z is not None else prev_gcode['Z']
                        prev_gcode['Y'] = y
                        prev_gcode['Z'] = z
                    elif coordinate == "crt":
                        c = gcode.C if gcode.C is not None else prev_gcode['C']
                        b = gcode.B if gcode.B is not None else prev_gcode['B']
                        prev_gcode['C'] = c
                        prev_gcode['B'] = b

                    f = None
                    e = None

                    for word in line.block.words:
                        if word.letter == 'F':
                            f = word.value

                    for param in line.block.modal_params:
                        if param.letter == 'E':
                            e = param.value

                    if coordinate == 'xyz':
                        coords.append([x, y, z, f, e])
                    elif coordinate == 'crt':
                        coords.append([x, z, c, b, f, e])

        return np.array(coords)
