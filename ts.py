import dearpygui.dearpygui as dpg
import cv2
import array
import numpy as np
import glob
dpg.create_context()
dpg.create_viewport(title='Custom Title', width=850, height=800)
dpg.set_viewport_always_top(True)
dpg.setup_dearpygui()
def func():
    dpg.show_tool(dpg.mvTool_ItemRegistry)
    for fname in images:
        print(fname)
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        lwr = np.array([0, 0, 143])
        upr = np.array([179, 61, 252])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        msk = cv2.inRange(hsv, lwr, upr)
        
        krn = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 30))
        dlt = cv2.dilate(msk, krn, iterations=5)
        res = 255 - cv2.bitwise_and(dlt, msk)

        res = np.uint8(res)
        ret, corners = cv2.findChessboardCorners(res, (5, 5),flags=cv2.CALIB_CB_ADAPTIVE_THRESH +cv2.CALIB_CB_FAST_CHECK +cv2.CALIB_CB_NORMALIZE_IMAGE)
        width, height, channels, data = dpg.load_image(fname)
        t=dpg.add_dynamic_texture(width=width, height=height, default_value=data,parent="texreg")
        print(t)
        dpg.add_image(t,parent="win")
        if ret:
            print(corners)
            fnl = cv2.drawChessboardCorners(img, (7, 7), corners, ret)
            cv2.imshow("fnl", fnl)
            cv2.waitKey(0)
        else:
            print("No Checkerboard Found")
        # Find the chess board corners
        width, height, channels, data = dpg.load_image(fname)
        t=dpg.add_dynamic_texture(width=width, height=height, default_value=data,parent="texreg")
        print(t)
        dpg.add_image(t,parent="win")
        # ret, corners = cv2.findChessboardCorners(img, (7,6), None)
        # # If found, add object points, image points (after refining them)
        # if ret == True:
        #     objpoints.append(objp)
        #     corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
        #     imgpoints.append(corners2)
        #     # Draw and display the corners
        #     cv2.drawChessboardCorners(img, (7,6), corners2, ret)
        #     cv2.imshow('img', img)
        #     cv2.waitKey(500)
    print(objpoints)
    print(imgpoints)


width, height, channels, data = dpg.load_image("assets/images/o1z01.bmp")
with dpg.texture_registry(show=True,tag="texreg"):
    dpg.add_dynamic_texture(width=width, height=height, default_value=data, tag="tex41")
    pass
with dpg.window(label="Image tutorial",tag="win") as win:
    dpg.add_image("tex41")
    dpg.add_button(label="start",callback=func)
    #dpg.add_image("texture_cam")
    with dpg.font_registry():
        default_font=dpg.add_font("assets/fonts/JetBrainsMono2.304/JetBrainsMono-Medium.ttf",20)
    dpg.bind_font(default_font)
    with dpg.menu_bar(label="menuBar"):
        with dpg.menu(label="menu"):
            dpg.add_menu_item(label="Show Font Manager", callback=lambda:dpg.show_tool(dpg.mvTool_Font))

# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((6*7,3), np.float32)
objp[:,:2] = np.mgrid[0:7,0:6].T.reshape(-1,2)
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
images = glob.glob('assets/images/*.jpg')

#dpg.focus_item(win)
#dpg.set_primary_window(win, True)
cv2.destroyAllWindows()
dpg.show_viewport()
dpg.set_viewport_always_top(False)
dpg.show_metrics()
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()
#cv2.destroyAllWindows()