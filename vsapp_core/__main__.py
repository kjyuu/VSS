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
    elif sender==checkbox_distort:
        dpg.configure_item(group_distortion,show=app_data)
    elif sender==checkbox_calibrate:
        dpg.configure_item(group_calibration,show=app_data)
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
    texture_registry_calib=dpg.add_texture_registry() # texture registry for calibration results
    with dpg.table(tag="table",policy=dpg.mvTable_SizingStretchSame, header_row=False, borders_innerH=False,borders_outerH=False, borders_innerV=True, borders_outerV=False, resizable=True) as guiTableMain:
                dpg.add_table_column(init_width_or_weight=0.45)
                dpg.add_table_column()
                with dpg.table_row():
                    with dpg.child_window(autosize_y=True) as mainColWind1:
                        dpg.add_text("Image Distortion Module")
                        dpg.add_button(label="Select files", callback=fd.show_file_dialog)
                        dpg.add_child_window(width=-1, height=200, tag="txt_child",horizontal_scrollbar=True)
                        with dpg.group(horizontal=True):
                            checkbox_original=dpg.add_checkbox(label="Original",callback=checkbox_changed)
                            checkbox_scale=dpg.add_checkbox(label="Scale",callback=checkbox_changed)
                            checkbox_distort=dpg.add_checkbox(label="Distort",callback=checkbox_changed)
                            dpg.add_button(label="Start", callback=lambda:app.ResizeAndDistort(list_to_distort,draw_parent=group_results,draw_tex_reg=texture_registry_calib,enable_original=dpg.get_value(checkbox_original),
                                enable_scaling=dpg.get_value(checkbox_scale),target_height=dpg.get_value(target_height),target_width=dpg.get_value(target_width),scale_factor_x=dpg.get_value(target_scale_x),scale_factor_y=dpg.get_value(target_scale_y),
                                enable_distortion=dpg.get_value(checkbox_distort),dstBC_k1=dpg.get_value(dst_k1),dstBC_k2=dpg.get_value(dst_k2),dstBC_k3=dpg.get_value(dst_k3),dstBC_p1=dpg.get_value(dst_p1),dstBC_p2=dpg.get_value(dst_p2)))
                        with dpg.group(horizontal=True):
                            checkbox_calibrate=dpg.add_checkbox(label="Calibrate",callback=checkbox_changed)
                            dpg.add_button(label="Calibrate", callback=lambda:app.Calibrate(list_of_filepaths=list_to_distort,chessboardSize=(dpg.get_value(chessboard_squares_h)-1,dpg.get_value(chessboard_squares_w)-1),size_of_chessboard_squares_mm=dpg.get_value(size_of_chessboard_squares),results_parent=group_results,calib_tex_reg=texture_registry_calib,calib_enable=dpg.get_value(checkbox_calibrate),
                                                                                            enable_scaling=dpg.get_value(checkbox_scale),target_height=dpg.get_value(target_height),target_width=dpg.get_value(target_width),scale_factor_x=dpg.get_value(target_scale_x),scale_factor_y=dpg.get_value(target_scale_y)))
                        with dpg.group(show=False) as group_scaling: 
                            dpg.add_text("Image scaling settings")
                            target_height=dpg.add_input_int(label="Target height", default_value=0,min_value=0,min_clamped=True)
                            target_width=dpg.add_input_int(label="Target width", default_value=0,min_value=0,min_clamped=True)
                            target_scale_x=dpg.add_input_float(label="Scale factor x", default_value=0.5,min_value=0,min_clamped=True)
                            target_scale_y=dpg.add_input_float(label="Scale factor y", default_value=0.5,min_value=0,min_clamped=True)
                        with dpg.group(show=False) as group_distortion:
                            dpg.add_text("Distortion settings [Brown-Conrady]")
                            dst_k1=dpg.add_input_double(label="k1",default_value=0,step=0.0000001,step_fast=0.000001,format='%.8f')
                            dst_k2=dpg.add_input_double(label="k2",default_value=0,step=0.00000000001,step_fast=0.0000000001,format='%.12f')
                            dst_k3=dpg.add_input_double(label="k3",default_value=0,step=0.000000000000001,step_fast=0.00000000000001,format='%.16f')
                            dst_p1=dpg.add_input_double(label="p1",default_value=0,step=0.00001,step_fast=0.0001,format='%.6f')
                            dst_p2=dpg.add_input_double(label="p2",default_value=0,step=0.00001,step_fast=0.0001,format='%.6f')
                            pass
                        with dpg.group(show=False) as group_calibration: 
                            dpg.add_text("Camera Calibration settings")
                            chessboard_squares_h=dpg.add_input_int(label="Number of rows", default_value=6,min_value=0,min_clamped=True)
                            chessboard_squares_w=dpg.add_input_int(label="Number of columns", default_value=7,min_value=0,min_clamped=True)
                            size_of_chessboard_squares=dpg.add_input_float(label="Size of chessboard squares [mm]", default_value=5,min_value=0,min_clamped=True)
                        #imageplot do wyświetlania, image button jako miniatury?
                    with dpg.child_window(horizontal_scrollbar=True) as mainColWind2:
                        dpg.add_text("Results")
                        with dpg.group() as group_results:
                            pass
dpg.setup_dearpygui()
dpg.set_primary_window("Primary Window",True)
dpg.show_viewport()
dpg.set_viewport_always_top(False)
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()
