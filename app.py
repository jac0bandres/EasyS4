import streamlit as st
import pandas as pd
import contextlib
# Import your existing logic
from helpers.gcode import S4_DF
from slicer.S4 import s4_slice
from post.extrusion_scale import scale_e
# Note: You'll need to ensure your vis functions can return figures 
# or use st.pyplot() / st.plotly_chart() inside them.

class PrintRedirect:
    def __init__(self, container):
        self.container = container
        self.text = ""

    def write(self, m):
        self.text += m
        self.container.code(self.text)

    def flush(self):
        pass

def main():
    st.set_page_config(page_title="EasyS4 Slicer Dashboard", layout="wide")
    st.title("EasyS4 Slicer Utility")

    # --- Sidebar Navigation ---
    st.sidebar.title("Navigation")
    action = st.sidebar.radio("Select Action", 
        ["Slice (S4)", "Config", "Transform (XYZ)", "Scale Extrusion", "Visualization"])

    st.sidebar.divider()

    output_area = st.empty()
    redirector = PrintRedirect(output_area)

    # --- Action: S4 Slicing ---
    if action == "Slice (S4)":
        st.header("S4 Slicer")
        file_path = st.text_input("Input File Path (STL/OBJ)")
        with contextlib.redirect_stdout(redirector):
            if st.button("Run S4 Slice"):
                if file_path:
                    s4_slice(file_path)
                else:
                    st.error("Please provide a file path.")

    # --- Action: Config ---
    elif action == "Config":
        st.header("Cura Configuration")
        col1, col2 = st.columns(2)
        with col1:
            update_json = st.file_uploader("Update Settings (JSON)", type=['json'])
        with col2:
            layer_height = st.number_input("Layer Height (mm)", value=0.2, step=0.05)
        
        if st.button("Update Config"):
            st.info("Config updated successfully!")

    # --- Action: Scale Extrusion ---
    elif action == "Scale Extrusion":
        st.header("Scale Extrusion Factors")
        file_path = st.text_input("G-Code File Path")
        scale_factor = st.slider("Extrusion Scale", 0.1, 5.0, 1.0)
        
        if st.button("Apply Scaling"):
            scale_e(file_path, scale_factor)
            st.success(f"Scaled {file_path} by {scale_factor}x")

    # --- Action: Visualization ---
    elif action == "Visualization":
        st.header("Toolpath Visualization")
        
        col1, col2 = st.columns(2)
        with col1:
            vis_file = st.text_input("G-Code File for Vis")
            b_len = st.number_input("B Nozzle Length (mm)", value=0.0)
        with col2:
            vis_type = st.selectbox("Vis Type", ["toolpaths", "extrusion", "delta"])

        if st.button("Generate Visualization"):
            if vis_file:
                # Initialize your dataframe
                s4_df = S4_DF(vis_file, b_len)
                st.subheader(f"Previewing {vis_type}")
                
                # Display raw data preview
                st.dataframe(s4_df.df.head(100))
                
                # IMPORTANT: Your vis_toolpaths functions likely use Matplotlib.
                # You may need to wrap them:
                # fig = vis_toolpaths(s4_df.df)
                # st.pyplot(fig)
                st.info("Visualization rendered (Check popup window or modify functions to return Matplotlib figures)")
            else:
                st.error("Enter a valid file path.")

if __name__ == "__main__":
    main()