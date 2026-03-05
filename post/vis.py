import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

def vis_toolpaths(df):
    # Prepare data (handle NaNs and column logic)
    x_col = 'X_Cart' if 'X_Cart' in df.columns else 'X'
    y_col = 'Y_Cart' if 'Y_Cart' in df.columns else 'Y'
    z_col = 'Z_Polar' if 'Z_Polar' in df.columns else 'Z'
    
    plot_df = df[[x_col, y_col, z_col]].dropna().reset_index(drop=True)
    
    fig = plt.figure(figsize=(10, 9))
    # Adjust subplot to make room for slider at the bottom
    ax = fig.add_subplot(111, projection='3d')
    plt.subplots_adjust(bottom=0.2) 

    # Initial plot (first 10% of data or just the first point)
    line, = ax.plot(plot_df[x_col], plot_df[y_col], plot_df[z_col], 
                    color='blue', lw=0.8, alpha=0.8)

    ax.set_xlim(-60, 60)
    ax.set_ylim(-60, 60)
    ax.set_zlim(-60, 60)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    # 1. Force the physical box to be a cube
    ax.set_box_aspect([1, 1, 1]) 

    # 2. Force the scaling of the data to be equal (Requires Matplotlib 3.3.0+)
    ax.set_aspect('equal')

    # Add Slider Axes [left, bottom, width, height]
    ax_slider = plt.axes([0.2, 0.05, 0.6, 0.03])
    slider = Slider(ax_slider, 'Timeline', 0, len(plot_df)-1, 
                    valinit=len(plot_df)-1, valstep=1)

    def update(val):
        idx = int(slider.val)
        # Update line data to only show points up to the slider index
        line.set_data(plot_df[x_col][:idx], plot_df[y_col][:idx])
        line.set_3d_properties(plot_df[z_col][:idx])
        fig.canvas.draw_idle()

    slider.on_changed(update)

    plt.title("Interactive GCode Playback")
    plt.show()
    #return slider, fig 
