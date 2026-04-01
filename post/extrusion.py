'''
Custom extrusion
'''
import re
from pygcode import Line
import numpy as np

from helpers.coord import to_xyz

def dampen_extrusion(file_path, b_len, threshold):
    with open(file_path, 'r') as fh:
        print(f'Opening {file_path}')

        X = []
        Y = []
        Z = []
        C = []
        B = []
        E = []
        F = []
        file_len = len(fh.readlines())
        fh.seek(0)
        print(f'{file_len} lines')
        i = 0
        prev_pos = None
        for line_text in fh:
            i += 1
            line_text = line_text.strip()
            if not line_text or line_text.startswith(';'):
                continue

            line = Line(line_text)
            # using lists and defining propeties by their index to reduce overhead
            if not line.block.gcodes:
                continue

            for param in line.block.modal_params:
                if param.letter == 'E':
                    e = param.value

            if e is None:
                continue

            for gcode in sorted(line.block.gcodes):
                if gcode.word not in ('G01', 'G00'):
                    continue 
                x = float(gcode.X) if gcode.X is not None else None
                z = float(gcode.Z) if gcode.Z is not None else None
                b = float(gcode.B) if gcode.B is not None else None 

                for word in line.block.words:
                    if word.letter == 'F':
                        f = word.value
                
                if z and x:
                    dist = np.sqrt(abs(x)**2 + abs(z-b_len*np.sin(b))**2)
                    if dist < threshold:
                        e = e*(dist/5)
                        line_text = re.sub(r"(E)[+-]?\d+(?:\.\d+)?", rf"\g<1>" + str(e), line_text) 
            fh.write(line_text)