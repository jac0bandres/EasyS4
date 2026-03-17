import re
from helpers.gcode import S4_DF

def rewrite_line(line_text, x, y, z):
    e_match = re.search(r'(E[0-9.-]+)', line_text)
    f_match = re.search(r'(F[0-9.-]+)', line_text)

    e_str = e_match.group(1) if e_match else ""
    f_str = e_match.group(1) if f_match else ""

    g_cmd = 'G1' if 'G1' in line_text or 'G01' in line_text else 'G0'
    new_line = f'{g_cmd} X{x:.3f} Y{y:.3f} Z{z:.3f} E{e_str:.3f} F{f_str:.3f}'

    return new_line

def transform_to_xyz(file_path, b_len):
    df = S4_DF(file_path, b_len)

    with open(f'input_gcode/{file_path}','r') as ifh:
        with open(f'output_gcode/')
    