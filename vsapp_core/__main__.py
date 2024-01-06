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
    selectedFilesDistortion=selected_files
    #clear the window
    dpg.delete_item(outputwindow, children_only=True)
    for file in selected_files:
        dpg.add_text(file, parent=outputwindow)
        
fd = FileDialog(callback=outputSelectedForDistortion, show_dir_size=False, modal=False, allow_drag=False,no_resize=False)

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
    #with dpg.child_window(autosize_x=True, autosize_y=True,tag="child_window_main",no_scrollbar=True):
    with dpg.table(tag="table",policy=dpg.mvTable_SizingStretchSame, header_row=False, borders_innerH=False,borders_outerH=False, borders_innerV=True, borders_outerV=False, resizable=True) as guiTableMain:
                dpg.add_table_column(init_width_or_weight=0.4)
                dpg.add_table_column()
                with dpg.table_row():
                    with dpg.child_window(autosize_y=True) as mainColWind1: 
                        dpg.add_text("Image Distortion Module")
                        dpg.add_button(label="Select files", callback=fd.show_file_dialog)
                        dpg.add_child_window(width=-1, height=200, tag="txt_child",horizontal_scrollbar=True)
                        dpg.add_button(label="Start", callback=test)#app.startDistortion(selectedFilesDistortion))
                    with dpg.child_window(autosize_y=True) as mainColWind2:
                        dpg.add_input_text(label="Text Input 1", source="string_value")
                    test()
dpg.setup_dearpygui()
dpg.set_primary_window("Primary Window",True)
dpg.show_viewport()
dpg.set_viewport_always_top(False)
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()