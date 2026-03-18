import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np
from scipy.spatial.distance import cdist

def vis_extrusion(df):
    e_col = 'E'
    
    plot_df = df[[e_col]].dropna().reset_index(drop=True)
    fig = plt.figure(figsize=(10,9))
    ax = fig.add_subplot(111)
    
    ax.plot(plot_df[e_col], color='blue')
    ax.set_xlabel('t')
    ax.set_ylabel('Extrusion change (mm)')
    plt.title('Extrusion')
    plt.show()

def vis_deltas(df):    
    x_col = 'X_Cart' if 'X_Cart' in df.columns else 'X'
    y_col = 'Y_Cart' if 'Y_Cart' in df.columns else 'Y'
    z_col = 'Z_Polar' if 'Z_Polar' in df.columns else 'Z'

    dist = cdist([df[x_col], df[y_col], df[z_col]], [df[x_col], df[y_col], df[z_col]], metric='euclidean')
    plt.plot(dist)

    plt.title('Deltas')
    plt.show()

def vis_toolpaths(df):
    # Prepare data (handle NaNs and column logic)
    x_col = 'X_Cart' if 'X_Cart' in df.columns else 'X'
    y_col = 'Y_Cart' if 'Y_Cart' in df.columns else 'Y'
    z_col = 'Z_Polar' if 'Z_Polar' in df.columns else 'Z'
    
    plot_df = df[[x_col, y_col, z_col]].dropna().reset_index(drop=True)
    
    fig = plt.figure(figsize=(10, 9))
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(bottom=0.2) 

    line, = ax.plot(plot_df[x_col], plot_df[y_col], plot_df[z_col], 
                    color='blue', lw=0.8, alpha=0.8)

    ax.set_xlim(-60, 60)
    ax.set_ylim(-60, 60)
    ax.set_zlim(-60, 60)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_aspect('equal')

    ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
    slider = Slider(ax_slider, 'Timeline', 0, len(plot_df)-1, 
                    valinit=len(plot_df)-1, valstep=1)

    def update(val):
        idx = int(slider.val)
        line.set_data(plot_df[x_col][:idx], plot_df[y_col][:idx])
        line.set_3d_properties(plot_df[z_col][:idx])
        fig.canvas.draw_idle()

    slider.on_changed(update)

    plt.title("Interactive GCode Playback")
    plt.show()
    #return slider, fig 
