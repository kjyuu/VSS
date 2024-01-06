import os
import numpy as np
import cv2
import dearpygui.dearpygui as dpg
def addFontRegistry():
    with dpg.font_registry():
            dpg.add_font("assets/fonts/quicksand/Quicksand_Bold.otf",18)
            dpg.add_font("assets/fonts/JetBrainsMono2.304/JetBrainsMono-Bold.ttf",18)
            default_font=dpg.add_font("assets/fonts/JetBrainsMono2.304/JetBrainsMono-Medium.ttf",20)
            dpg.add_font("assets/fonts/JetBrainsMono2.304/JetBrainsMono-Light.ttf",20)
            dpg.add_font("assets/fonts/JetBrainsMono2.304/JetBrainsMono-Italic.ttf",20)
            dpg.add_font("assets/fonts/JetBrainsMono2.304/JetBrainsMonoNL-Medium.ttf",20)
    dpg.bind_font(default_font)
def addMenuBar():
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
def create_new_project():
    pass
def open_project():
    pass
def save_project():
    pass
def save_project_settings():
    pass
def edit_app_settings():
    pass
def init_project():
    pass
def open_start_view():
    pass
def close_start_view():
    pass
def open_project_view():
    pass
def close_project_view():
    pass
def startDistortion(selectedFilesDistortion):
    print("started startDistortion:",np.size(selectedFilesDistortion))
    for file in selectedFilesDistortion:
        #check if file is image type
        if os.path.splitext(file)[1] in ['.jpg', '.png', '.jpeg', '.bmp','.tif']:
            print(file, "is an image file")
            true_dst=cv2.imread(file)
            src = true_dst

            # ground truth homography from true_dst to src
            H = np.array([
                [8.7976964e-01,   3.1245438e-01,  -3.9430589e+01],
                [-1.8389418e-01,   9.3847198e-01,   1.5315784e+02],
                [1.9641425e-04,  -1.6015275e-05,   1.0000000e+00]])

            # create indices of the destination image and linearize them
            h, w = true_dst.shape[:2]
            indy, indx = np.indices((h, w), dtype=np.float32)
            lin_homg_ind = np.array([indx.ravel(), indy.ravel(), np.ones_like(indx).ravel()])

            # warp the coordinates of src to those of true_dst
            map_ind = H.dot(lin_homg_ind)
            map_x, map_y = map_ind[:-1]/map_ind[-1]  # ensure homogeneity
            map_x = map_x.reshape(h, w).astype(np.float32)
            map_y = map_y.reshape(h, w).astype(np.float32)

            # remap!
            dst = cv2.remap(src, map_x, map_y, cv2.INTER_LINEAR)
            blended = cv2.addWeighted(true_dst, 0.5, dst, 0.5, 0)
            cv2.imshow('blended.png', blended)
            cv2.waitKey()