# To scale extrusions and bypass whole S4_Slicer process
import re
from pygcode import Line
import os

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
                    
