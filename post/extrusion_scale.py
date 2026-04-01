# To scale extrusions and bypass whole S4_Slicer process
import re
from pygcode import Line
import numpy as np
import os

RETRACTION_LENGTH = -1.0

def dampen_e(file_path, threshold, b_len, e_max, dampen):
    file_name = os.path.basename(file_path)
    with open(file_path, 'r') as ifh:
        with open(f'output_gcode/{file_name}_dampened.gcode', 'w') as ofh:
            print(f'Opening {file_path}')
            file_len = len(ifh.readlines())
            ifh.seek(0)
            print(f'{file_len} lines')
            i = 0
            for line_text in ifh:
                i += 1

                line = Line(line_text)
                # using lists and defining propeties by their index to reduce overhead
                if not line.block.gcodes:
                    ofh.write(line_text)
                    continue
                    
                e = None

                for param in line.block.modal_params:
                    if param.letter == 'E':
                        e = param.value
                
                if e is None:
                    ofh.write(line_text)
                    continue
                
                if np.abs(e) == 1.0:
                    ofh.write(line_text)
                    continue

                for gcode in sorted(line.block.gcodes):
                    if gcode.word not in ('G01', 'G00'):
                        continue 
                    x = float(gcode.X) if gcode.X is not None else None
                    z = float(gcode.Z) if gcode.Z is not None else None
                    b = float(gcode.B) if gcode.B is not None else None
                    
                    if z and x and e:
                        dist = np.sqrt((x+b_len*np.cos(np.deg2rad(b)))**2 + (z+b_len*np.sin(np.deg2rad(b)))**2)
                        if dist < threshold:
                            e = e_max*np.exp(dampen*(dist-threshold))
                            line_text = re.sub(r"(E)[+-]?\d+(?:\.\d+)?", rf"\g<1>" + str(e), line_text) 
                ofh.write(line_text)

def scale_e(file_path, scale):
    file_name = os.path.basename(file_path)
    with open(file_path, 'r') as ifh:
        with open(f'output_gcode/{file_name}_{scale}x.gcode', 'w') as ofh:
            for line_text in ifh.readlines():
                line = Line(line_text)

                for param in line.block.modal_params:
                    if param.letter == "E":
                        extrusion = param.value
                        scaled_e = extrusion * scale

                        line_text = re.sub(r"(E)[+-]?\d+(?:\.\d+)?", rf"\g<1>" + str(scaled_e), line_text)

                ofh.write(line_text)
                    
