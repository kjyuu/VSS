import dearpygui.dearpygui as dpg
from filedialog30.fdialog import FileDialog
import app
import numpy as np
import cv2
import array
import os
dpg.create_context()
dpg.create_viewport(title='Distortion Modelling and Analysis', width=1600, height=900)
dpg.set_viewport_always_top(True)
list_to_distort=[]
def checkbox_changed(sender,app_data,user_data):
    if sender==checkbox_scale:
        dpg.configure_item(group_scaling,show=app_data)
    elif sender==ckeckbox_distort:
        dpg.configure_item(group_distortion,show=app_data)
def outputSelectedForDistortion(selected_files):
    outputwindow="txt_child"
    global list_to_distort
    list_to_distort=[]
    dpg.delete_item(outputwindow, children_only=True)
    for file in selected_files:
        dpg.add_text(file, parent=outputwindow)
        list_to_distort.append(file)
fd = FileDialog(callback=outputSelectedForDistortion, show_dir_size=False, modal=False, allow_drag=False,no_resize=False,default_path='assets\\images')
app.addFontRegistry()

dpg.configure_app(docking=True, docking_space=False)

with dpg.window(tag="Primary Window",no_scroll_with_mouse=True,no_scrollbar=True): # main window of the program
    app.addMenuBar()
    with dpg.table(tag="table",policy=dpg.mvTable_SizingStretchSame, header_row=False, borders_innerH=False,borders_outerH=False, borders_innerV=True, borders_outerV=False, resizable=True) as guiTableMain:
                dpg.add_table_column(init_width_or_weight=0.45)
                dpg.add_table_column()
                with dpg.table_row():
                    with dpg.child_window(autosize_y=True) as mainColWind1:
                        dpg.add_text("Image Distortion Module")
                        dpg.add_button(label="Select files", callback=fd.show_file_dialog)
                        dpg.add_child_window(width=-1, height=200, tag="txt_child",horizontal_scrollbar=True)
                        with dpg.group(horizontal=True):
                            checkbox_scale=dpg.add_checkbox(label="Scale",callback=checkbox_changed)
                            ckeckbox_distort=dpg.add_checkbox(label="Distort",callback=checkbox_changed)
                            dpg.add_button(label="Start", callback=lambda:app.distortImages(list_to_distort,dpg.get_value(target_height),dpg.get_value(target_width),dpg.get_value(target_scale_x),dpg.get_value(target_scale_y)))
                        with dpg.group(show=False) as group_scaling: 
                            dpg.add_text("Image scaling settings")
                            target_height=dpg.add_input_int(label="Target height", default_value=0,min_value=0,min_clamped=True)
                            target_width=dpg.add_input_int(label="Target width", default_value=0,min_value=0,min_clamped=True)
                            target_scale_x=dpg.add_input_float(label="Scale factor x", default_value=0,min_value=0,min_clamped=True)
                            target_scale_y=dpg.add_input_float(label="Scale factor y", default_value=0,min_value=0,min_clamped=True)
                        with dpg.group(show=False) as group_distortion:
                            pass 
                        with dpg.group() as group_results:
                            pass
                        #imageplot do wyświetlania, image button jako miniatury?
                    with dpg.child_window(autosize_y=True) as mainColWind2:
                        dpg.add_input_text(label="Text Input 1", source="string_value")
dpg.setup_dearpygui()
dpg.set_primary_window("Primary Window",True)
dpg.show_viewport()
dpg.set_viewport_always_top(False)
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()