import dearpygui.dearpygui as dpg
from filedialog30.fdialog import FileDialog
import app
import numpy as np
import cv2
import array
dpg.create_context()
dpg.create_viewport(title='Engineering Thesis App', width=1600, height=900)
dpg.set_viewport_always_top(True)
selectedFilesDistortion=[]
def outputSelectedForDistortion(selected_files):
    outputwindow="txt_child"
    #send selected_files outside the scope
    global selectedFilesDistortion
    selectedFilesDistortion=[]
    #clear the window
    dpg.delete_item(outputwindow, children_only=True)
    for file in selected_files:
        dpg.add_text(file, parent=outputwindow)
        selectedFilesDistortion.append(file)
        
fd = FileDialog(callback=outputSelectedForDistortion, show_dir_size=False, modal=False, allow_drag=False,no_resize=False)

app.addFontRegistry()

dpg.configure_app(docking=True, docking_space=False)

with dpg.window(tag="Primary Window"): # main window of the program
    app.addMenuBar()
    #with dpg.child_window(autosize_x=True, autosize_y=True,tag="child_window_main",no_scrollbar=True):
    with dpg.table(tag="table",policy=dpg.mvTable_SizingStretchSame, header_row=False, borders_innerH=False,borders_outerH=False, borders_innerV=True, borders_outerV=False, resizable=True) as guiTableMain:
                dpg.add_table_column(init_width_or_weight=0.4)
                dpg.add_table_column()
                with dpg.table_row():
                    with dpg.child_window(autosize_y=True) as mainColWind1: 
                        dpg.add_text("Image Distortion Module")
                        dpg.add_button(label="Select files", callback=fd.show_file_dialog)
                        dpg.add_child_window(width=-1, height=200, tag="txt_child",horizontal_scrollbar=True)
                        dpg.add_button(label="Start", callback=lambda:app.startDistortion(selectedFilesDistortion))
                    with dpg.child_window(autosize_y=True) as mainColWind2:
                        dpg.add_input_text(label="Text Input 1", source="string_value")
dpg.setup_dearpygui()
dpg.set_primary_window("Primary Window",True)
dpg.show_viewport()
dpg.set_viewport_always_top(False)
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()