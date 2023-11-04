import dearpygui.dearpygui as dpg
import numpy as np
import cv2
dpg.create_context()
dpg.create_viewport(title='Vision System Studio', width=1100, height=1200)
with dpg.font_registry():
        default_font=dpg.add_font("assets/fonts/quicksand/Quicksand_Bold.otf",18)
dpg.bind_font(default_font)
with dpg.window(tag="Primary Window"): 
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
    
dpg.setup_dearpygui()
dpg.set_primary_window("Primary Window",True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()