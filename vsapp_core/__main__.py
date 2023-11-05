import dearpygui.dearpygui as dpg
import numpy as np
import cv2
dpg.create_context()
dpg.create_viewport(title='Vision System Studio', width=1920, height=1080)
#dpg.configure_viewport("Vision System Studio",clear_color=[255,0,0,255],decorated=True)
with dpg.font_registry():
        default_font=dpg.add_font("assets/fonts/quicksand/Quicksand_Bold.otf",18)
dpg.bind_font(default_font)
dpg.configure_app(docking=True, docking_space=False)
with dpg.window(tag="Primary Window"): # main window of the program
    dpg.add_text("Welcome to Vision System Studio!")
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
                        with dpg.child_window(autosize_y=True,width=dpg.get_item_width("Primary Window")//4) as mainColWind1:
                            print(dpg.get_item_width("child_window_main"))
                            print(dpg.get_item_width("child_window_main")//3)
                        with dpg.child_window(autosize_y=True,width=dpg.get_item_width("Primary Window")//4) as mainColWind2:
                            pass
                        with dpg.child_window(autosize_y=True,width=dpg.get_item_width("Primary Window")//5) as mainColWind3:
                            dpg.add_button(label="thirds")
        #with dpg.group(horizontal=True) as mainCol1:
           
dpg.setup_dearpygui()
dpg.set_primary_window("Primary Window",True)
dpg.show_viewport()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()