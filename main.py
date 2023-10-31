import dearpygui.dearpygui as dpg
import numpy as np
import cv2
dpg.create_context()
dpg.create_viewport(title='Vision System Studio', width=1100, height=1200)
with dpg.window(tag="Primary Window"):
    dpg.add_text("Welcome to Vision System Studio!")
    with dpg.menu_bar():
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
            dpg.add_menu_item(label="Language")
        with dpg.menu(label="Help"):
            dpg.add_menu_item(label="About")
            dpg.add_menu_item(label="Metrics")
            dpg.add_menu_item(label="Documentation")
    dpg.add_button(label="New Project")
    dpg.add_input_text(label="string",default_value="Quick brown fox")
dpg.setup_dearpygui()
dpg.set_primary_window("Primary Window",True)
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()