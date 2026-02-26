# from read_gcode import read_gcode
# from plot import plot
# import math
# import numpy as np
# 
# b_len = 5
# 
# def xczb_xyz(x, z, c, b):
#     c = math.radians(c)
#     b = math.radians(b)
#     return (x-(b_len*math.cos(b)))*math.cos(c), (x-b_len*math.cos(b))*math.sin(c), z+math.sin(b) # joint position
# 
# def xyz_polar(x, y, z):
#     
# 
# gcode = read_gcode("output_gcode/25dino_0.02x.gcode", gword_filter=['G01'])
# pts = []
# 
# for g in gcode:
#     x, y, z = xczb_xyz(*g)
#     pts.append([x,y,z])
# 
# pts = np.array(pts)
# plot(pts)