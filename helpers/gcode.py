# General gcode reader
import numpy as np
from pygcode import Line
from typing import Optional
import pandas as pd
import time

class S4_DF:
    def __init__(self, gcode_filepath: str, b_len: Optional[float]):
        self.df = read_gcode_file(gcode_filepath) 
        coord_type = check_coord(self.df)
        self.b_len = float(b_len) if b_len else 41.5
        
        if coord_type == 'xyz':
           self.df.xyz = self.df
           self.df.polar = to_polar(self.df) 
        elif coord_type == 'core':
            self.df.polar = self.df
            self.df.xyz = to_xyz(self.df, self.b_len)
        
def read_gcode_file(file_path: str):
    with open(file_path, 'r') as fh:
        print(f'Opening {file_path}')

        X = []
        Y = []
        Z = []
        C = []
        B = []
        E = []
        F = []
        L = []
        G = []
        file_len = len(fh.readlines())
        fh.seek(0)
        print(f'{file_len} lines')
        i = 0
        t = time.time()
        for line_text in fh:
            i += 1
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
                x = float(gcode.X) if gcode.X is not None else None
                y = float(gcode.Y) if gcode.Y is not None else None
                z = float(gcode.Z) if gcode.Z is not None else None
                c = float(gcode.C) if gcode.C is not None else None
                b = float(gcode.B) if gcode.B is not None else None

                f = None
                e = None

                for word in line.block.words:
                    if word.letter == 'F':
                        f = word.value

                for param in line.block.modal_params:
                    if param.letter == 'E':
                        e = param.value
                
                X.append(x)
                Y.append(y)
                Z.append(z)
                C.append(c)
                B.append(b)
                E.append(e)
                F.append(f)
                L.append(i)
                G.append(gcode.word)

            if i % 5000 == 0:
                print(f'Reading line {i}/{file_len}', end='\r', flush=True)
        print(f'Done: {round(time.time()-t, 2)}s', end='\r', flush=True)

        return pd.DataFrame({'X': X, 'Y': Y, 'Z': Z, 'C': C, 'B': B, 'E': E, 'F': F, 'L': L, 'G': G})

def fill_forward(df: pd.DataFrame):
    return df.fillna(value={'X': 0, 'Y': 0, 'Z': 0}, limit=1).ffill()

def to_polar(df):
    df['X_Polar'] = np.sqrt(df['X']**2 + df['Y']**2)
    df['C'] = np.degrees(np.arctan2(df['Y'], df['X']))
    df['B'] = 0.0

    return df

def to_xyz(df, b_len, angle_step=1.0):
    """
    Interpolates B and C angles between rows and transforms to Cartesian.
    Assumes X and Z remain constant between angular changes.
    """
    
    # 1. Identify where interpolation is needed
    # We calculate the max angular delta between rows to determine step count
    diff_b = np.abs(df['B'].diff().shift(-1).fillna(0))
    diff_c = np.abs(df['C'].diff().shift(-1).fillna(0)) 
    df['E'].fillna(0)
    max_diff = np.maximum(diff_b, diff_c)
    
    interpolated_rows = []

    for i in range(len(df) - 1):
        start_row = df.iloc[i]
        end_row = df.iloc[i+1]
        
        # Calculate steps for this specific segment
        steps = int(np.ceil(max_diff.iloc[i] / angle_step))
        steps = max(steps, 1) # Ensure at least the original point is kept

        # Generate linear ramps for B and C
        # We use endpoint=False to avoid duplicating the 'end_row' 
        # which becomes the 'start_row' of the next iteration
        b_interp = np.linspace(start_row['B'], end_row['B'], steps, endpoint=False)
        c_interp = np.linspace(start_row['C'], end_row['C'], steps, endpoint=False)

        if start_row['E'] == end_row['E'] or start_row['G'] == 'G00':
            e_interp = np.full(steps, start_row['E'])
        else:
            e_interp = np.linspace(start_row['E'], end_row['E'], steps, endpoint=False)
        np.nan_to_num(e_interp, 0)
        
        # Create a temporary block of data
        # X and Z are assumed constant between these angle changes
        for b, c, e in zip(b_interp, c_interp, e_interp):
            interpolated_rows.append({
                'G': start_row['G'],
                'X_mach': start_row['X'],
                'Z_mach': start_row['Z'],
                'B': b,
                'C': c,
                'E': e,
            })

    # Add the final row of the original dataframe
    last_row = df.iloc[-1]
    interpolated_rows.append({
        'G': last_row['G'],
        'X_mach': last_row['X'],
        'Z_mach': last_row['Z'],
        'B': last_row['B'],
        'C': last_row['C'],
        'E': last_row['E']
    })

    # Convert back to DataFrame for vector math
    idf = pd.DataFrame(interpolated_rows)

    # 2. Apply the Kinematic Transformation
    z_hop = np.where(idf['G'] == 'G00', 1, 0)
    L = b_len + z_hop
    
    rad_b = np.radians(idf['B'])
    rad_c = np.radians(idf['C'])
    
    # Reverse the machine offset to find Polar R and Z
    # r_orig is the distance from the rotation center in the X plane
    r_orig = idf['X_mach'] + (np.sin(rad_b) * L)
    z_orig = idf['Z_mach'] - ((np.cos(rad_b) - 1) * L) - z_hop
    
    # Final Cartesian Output
    idf['X'] = r_orig * np.cos(rad_c)
    idf['Y'] = r_orig * np.sin(rad_c)
    idf['Z'] = z_orig

    export_cartesian_gcode(idf)
    
    return idf

def check_coord(df):
    if df['C'].isnull().all() or df['B'].isnull().all():
        return 'xyz'
    else:
        return 'core'

def export_cartesian_gcode(idf, filename="cura_preview.gcode"):
    with open(filename, 'w') as f:
        f.write("G90 ; Absolute positioning\n")
        f.write("M82 ; Absolute extrusion\n")
        
        for _, row in idf.iterrows():
            g_cmd = "G0" if row['G'] == 'G00' else "G1"
            f.write(f"{g_cmd} X{row['X']:.3f} Y{row['Y']:.3f} Z{row['Z']:.3f} E{row['E']:.5f}\n")