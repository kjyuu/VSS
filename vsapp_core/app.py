import os
import numpy as np
import cv2
import dearpygui.dearpygui as dpg
import math

def resizeImage(inputImage,target_width=0,target_height=0,scale_factor_x=0,scale_factor_y=0):
    # resize image
    # if selected width or height, calculate target for resized image
    epsilon = 1e-10 # constant for checking if float is 0
    target_size=0
    fx=1.0
    fy=1.0
    if target_height!=0 and target_width==0 and abs(scale_factor_x)< epsilon and abs(scale_factor_y)<epsilon: #scaling by set height / shape[0] is height
        target_width=int(inputImage.shape[1]*(target_height/inputImage.shape[0]))
        target_size = (target_width, target_height)
    elif target_width!=0 and target_height==0 and abs(scale_factor_x)< epsilon and abs(scale_factor_y)<epsilon: #scaling by set width
        target_height=int(inputImage.shape[0]*(target_width/inputImage.shape[1]))
        target_size = (target_width, target_height)
    elif target_height!=0 and target_width!=0 and abs(scale_factor_x)< epsilon and abs(scale_factor_y)<epsilon: #scaling by set width and height
        target_size = (target_width, target_height)
    elif target_height==0 and target_width==0 and abs(scale_factor_x)>epsilon and abs(scale_factor_y)<epsilon: #scaling by scale_factor_x
        target_size=0
        fx=scale_factor_x
        fy=1.0
    elif target_height==0 and target_width==0 and abs(scale_factor_x)<epsilon and abs(scale_factor_y)>epsilon: #scaling by scale_factor_y
        target_size=0
        fx=1.0
        fy=scale_factor_y
    elif target_height==0 and target_width==0 and abs(scale_factor_x)>epsilon and abs(scale_factor_y)>epsilon: #scaling by scale_factor_x and scale_factor_y
        target_size=0
        fx=scale_factor_x
        fy=scale_factor_y
    else:
        print("Error: resizeImage() - invalid arguments, returned original image")
        return inputImage
    # resize image depending on target size
    if np.size(target_size)==2:
        if target_size[0]>inputImage.shape[1]:
            resized = cv2.resize(inputImage, target_size, interpolation = cv2.INTER_CUBIC) #inter_area better for shrinking, inter_cubic for enlarging
        else:
            resized = cv2.resize(inputImage, target_size, interpolation = cv2.INTER_AREA)
    else:
        resized = cv2.resize(inputImage,None, fx=fx, fy=fy, interpolation = cv2.INTER_AREA)
    return resized
def ResizeAndDistort(selected_files,enable_scaling=False,enable_distortion=False,Cx=-1,Cy=-1,dstBC_k1=0,dstBC_k2=0,dstBC_k3=0,dstBC_p1=0,dstBC_p2=0,target_height=0,target_width=0,scale_factor_x=0,scale_factor_y=0):
    for file in selected_files:
        #check if file is of image type
        if os.path.splitext(file)[1] in ['.jpg', '.png', '.jpeg', '.bmp','.tif']:
            image = cv2.imread(file)
            print(os.path.basename(file), "is an image file with size", image.shape[1], "x", image.shape[0], "pixels")
            cv2.imshow("Original",image)
            print("scaling status:",enable_scaling)
            if enable_scaling:
                resized=resizeImage(image,target_height=target_height,target_width=target_width,scale_factor_x=scale_factor_x,scale_factor_y=scale_factor_y)
                print("Resized image to", resized.shape[1], "x", resized.shape[0], "pixels")
                cv2.imshow("Resized",resized)
                (h, w, c) = resized.shape
            else:
                (h, w, c) = image.shape
            print("distortion status:",enable_distortion)
            if enable_distortion:
                if(Cx==-1 or Cy==-1):
                    Cx,Cy = (w // 2, h // 2)
                # set up the x and y maps as float32
                map_x = np.zeros((h,w),np.float32)
                map_y = np.zeros((h,w),np.float32)
                for y in range(h):
                    for x in range(w):
                        #create radial distortion maps
                        r2=((x - Cx) ** 2 + (y - Cy) ** 2)
                        x_rel=x-Cx #x=0, Cx=240,x_rel=-240 map_x[0,0]=240-240=0
                        y_rel=y-Cy
                        map_x[y, x] = Cx + x_rel * (1+(dstBC_k1*r2)+(dstBC_k2*r2**2)+(dstBC_k3*r2**3))+(2*dstBC_p1*x_rel*y_rel)+(dstBC_p2*(r2+2*x_rel*x_rel))
                        map_y[y, x] = Cy + y_rel * (1+(dstBC_k1*r2)+(dstBC_k2*r2**2)+(dstBC_k3*r2**3))+(dstBC_p1*(r2+2*y_rel*y_rel))+(2*dstBC_p2*x_rel*y_rel)
                if enable_scaling:
                    dst = cv2.remap(resized,map_x,map_y,cv2.INTER_CUBIC)
                else:
                    dst = cv2.remap(image,map_x,map_y,cv2.INTER_CUBIC)
                # do the remap  this is where the magic happens      
                #show the results and wait for a key
                cv2.imshow("Distorted",dst)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
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