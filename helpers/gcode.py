# General gcode reader
import numpy as np
from pygcode import Line
import pandas as pd
import time

class S4_DF:
    def __init__(self, gcode_filepath: str, b_len: float):
        self.df = read_gcode_file(gcode_filepath) 
        self.df = fill_forward(self.df)
        coord_type = check_coord(self.df)
        self.b_len = float(b_len)
        
        if coord_type == 'xyz':
           self.df = to_polar(self.df) 
        elif coord_type == 'core':
            self.df = to_xyz(self.df, self.b_len)

        self.df = fill_forward(self.df)

def read_gcode_file(file_path: str):
    with open(file_path, 'r') as fh:
        print(f'Opening {file_path}')

        X = []
        Y = []
        Z = []
        C = []
        B = []
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

            if i % 5000 == 0:
                print(f'Reading line {i}/{file_len}', end='\r', flush=True)
        print(f'Done: {round(time.time()-t, 2)}s', end='\r', flush=True)

        return pd.DataFrame({'X': X, 'Y': Y, 'Z': Z, 'C': C, 'B': B})

def fill_forward(df: pd.DataFrame):
    return df.fillna(value={'X': 0, 'Y': 0, 'Z': 0, 'C': 0, 'B': 0}, limit=1).ffill()

def to_polar(df):
    df['X_Polar'] = np.sqrt(df['X']**2 + df['Y']**2)
    df['C'] = np.degrees(np.arctan2(df['Y'], df['X']))
    df['B'] = 0.0

    return df

def to_xyz(df, b_len):
    radius = df['X'] - (b_len*np.cos(np.radians(df['B'])))

    df['X_Cart'] = radius*np.cos(np.radians(df['C']))
    df['Y_Cart'] = radius*np.sin(np.radians(df['C']))
    df['Z_Polar'] = df['Z']+np.sin(np.radians(df['B']))

    return df

def check_coord(df):
    if df['C'].isnull().all() or df['B'].isnull().all():
        return 'xyz'
    else:
        return 'core'