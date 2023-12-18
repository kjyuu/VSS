import dearpygui.dearpygui as dpg
from filedialog20.fdialog import FileDialog

import numpy as np
import cv2
import array
dpg.create_context()
dpg.create_viewport(title='Engineering Thesis App', width=1920, height=1080)
#dpg.configure_viewport("Vision System Studio",clear_color=[255,0,0,255],decorated=True)

def set_cam_param(sender,app_data,user_data):
    print("sender is:",sender)
    print("app_data is:",app_data)
    print("user data is:",user_data)
    cam1.set(user_data,app_data)

cam1=cv2.VideoCapture(0)
ret,frame=cam1.read()
frame_width=cam1.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height=cam1.get(cv2.CAP_PROP_FRAME_HEIGHT)
video_fps=cam1.get(cv2.CAP_PROP_FPS)
print("W,H,FPS:",frame_width,frame_height,video_fps)
cam_params = [
cv2.CAP_PROP_FRAME_WIDTH,
cv2.CAP_PROP_FRAME_HEIGHT,
cv2.CAP_PROP_FPS,
cv2.CAP_PROP_CONTRAST,
cv2.CAP_PROP_BRIGHTNESS,
cv2.CAP_PROP_SATURATION,
cv2.CAP_PROP_HUE,
cv2.CAP_PROP_GAIN,
cv2.CAP_PROP_EXPOSURE,
cv2.CAP_PROP_SHARPNESS,
cv2.CAP_PROP_GAMMA,
cv2.CAP_PROP_TEMPERATURE,
cv2.CAP_PROP_TRIGGER,
cv2.CAP_PROP_ZOOM,
cv2.CAP_PROP_FOCUS,
cv2.CAP_PROP_BACKLIGHT,
cv2.CAP_PROP_PAN]
data=np.flip(frame,2)
data=data.ravel()
data=np.asfarray(data,dtype='f')
texture_data_frame=np.true_divide(data,255.0)
with dpg.texture_registry():
    dpg.add_raw_texture(frame_width,frame_height,texture_data_frame,format=dpg.mvFormat_Float_rgb,tag="texture_cam",label="tex_1")
    
with dpg.font_registry():
        dpg.add_font("assets/fonts/quicksand/Quicksand_Bold.otf",18)
        dpg.add_font("assets/fonts/JetBrainsMono2.304/JetBrainsMono-Bold.ttf",18)
        default_font=dpg.add_font("assets/fonts/JetBrainsMono2.304/JetBrainsMono-Medium.ttf",20)
        dpg.add_font("assets/fonts/JetBrainsMono2.304/JetBrainsMono-Light.ttf",20)
        dpg.add_font("assets/fonts/JetBrainsMono2.304/JetBrainsMono-Italic.ttf",20)
        dpg.add_font("assets/fonts/JetBrainsMono2.304/JetBrainsMonoNL-Medium.ttf",20)
dpg.bind_font(default_font)
dpg.configure_app(docking=True, docking_space=False)
with dpg.window(tag="Primary Window"): # main window of the program
    dpg.add_text("Welcome to the App!")
    with dpg.menu_bar(): # menu bar
        with dpg.menu(label="Project"):
            dpg.add_menu_item(label="New")
            dpg.add_menu_item(label="Open..")
            with dpg.menu(label="Open Recent"):
                dpg.add_menu_item(label="to do")
            dpg.add_menu_item(label="Save")
            dpg.add_menu_item(label="Save as..")
            dpg.add_menu_item(label="Project Settings")
        with dpg.menu(label="Source"):
            dpg.add_menu_item(label="Folder")
            dpg.add_menu_item(label="USB Device")
        with dpg.menu(label="Settings"):
            dpg.add_menu_item(label="Toggle Fullscreen", callback=lambda:dpg.toggle_viewport_fullscreen())
            dpg.add_menu_item(label="Language")
        with dpg.menu(label="Tools"):
            dpg.add_menu_item(label="Show About", callback=lambda:dpg.show_tool(dpg.mvTool_About))
            dpg.add_menu_item(label="Show Metrics", callback=lambda:dpg.show_tool(dpg.mvTool_Metrics))
            dpg.add_menu_item(label="Show Documentation", callback=lambda:dpg.show_tool(dpg.mvTool_Doc))
            dpg.add_menu_item(label="Show Debug", callback=lambda:dpg.show_tool(dpg.mvTool_Debug))
            dpg.add_menu_item(label="Show Style Editor", callback=lambda:dpg.show_tool(dpg.mvTool_Style))
            dpg.add_menu_item(label="Show Font Manager", callback=lambda:dpg.show_tool(dpg.mvTool_Font))
            dpg.add_menu_item(label="Show Item Registry", callback=lambda:dpg.show_tool(dpg.mvTool_ItemRegistry))
    with dpg.child_window(autosize_x=True, autosize_y=True,tag="child_window_main",no_scrollbar=True):
        with dpg.table(tag="table",policy=dpg.mvTable_SizingStretchSame, header_row=False, borders_innerH=False,borders_outerH=False, borders_innerV=True, borders_outerV=False, resizable=True):
                    dpg.add_table_column()
                    dpg.add_table_column()
                    dpg.add_table_column()
                    with dpg.table_row():
                        with dpg.child_window(autosize_y=True) as mainColWind1:
                            with dpg.file_dialog(label="Demo File Dialog", width=800, height=400, show=False, callback=lambda s, a, u : print(s, a, u), tag="__demo_filedialog"):
                                dpg.add_file_extension(".*", color=(255, 255, 255, 255))
                                #dpg.add_file_extension(".jpg", color=(0, 255, 0, 255))
                                #dpg.add_file_extension(".png", color=(0, 255, 0, 255))
                                #dpg.add_file_extension(".bmp", color=(0, 255, 0, 255))
                                #dpg.add_file_extension(".gif", color=(0, 255, 0, 255))
                                #dpg.add_button(label="Button on file dialog")
                            dpg.add_button(label="Show File Selector", user_data=dpg.last_container(), callback=lambda s, a, u:  dpg.configure_item(u, show=True))
                            pass
                        with dpg.child_window(autosize_y=True) as mainColWind2:
                            #for param in cam_params:
                            #    dpg.add_input_int(label=param,default_value=cam1.get(param),callback=set_cam_param,user_data=param)
                            width, height, channels, data = dpg.load_image("assets/images/o1z01.bmp")
                            with dpg.texture_registry():
                                dpg.add_static_texture(width=width, height=height, default_value=data, tag="tex41")
                            dpg.add_image("tex41")
                        with dpg.child_window(autosize_y=True) as mainColWind3:
                            dpg.add_button(label="thirds")
                            dpg.add_image("texture_cam")
           
dpg.setup_dearpygui()
dpg.set_primary_window("Primary Window",True)
dpg.show_viewport()
while dpg.is_dearpygui_running():
    ret,frame=cam1.read()
    data=np.flip(frame,2)
    data=data.ravel()
    data=np.asfarray(data,dtype='f')
    texture_data_frame=np.true_divide(data,255.0)
    dpg.set_value("texture_cam",texture_data_frame)
    dpg.render_dearpygui_frame()
cam1.release()
dpg.destroy_context()