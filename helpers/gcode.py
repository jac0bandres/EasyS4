# General gcode reader
import numpy as np
from pygcode import Line

def read_file(file_path: str, coordinate: str):
    with open(file_path, 'r') as fh:
        coords = []
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
                    x = gcode.X

                    if coordinate == "xyz":
                        y = gcode.Y
                        z = gcode.Z
                    elif coordinate == "crt":
                        c = gcode.C
                        b = gcode.B

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
