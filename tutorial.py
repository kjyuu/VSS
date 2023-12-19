import dearpygui.dearpygui as dpg
import cv2
import array
import numpy as np
import glob
dpg.create_context()
dpg.create_viewport(title='Custom Title', width=850, height=1100)

dpg.setup_dearpygui()
def func():
    for fname in images:
        print(fname)
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chess board corners
        width, height, channels, data = dpg.load_image(fname)
        with dpg.texture_registry():
            dpg.add_dynamic_texture(width=width, height=height, default_value=data)
        ret, corners = cv2.findChessboardCorners(gray, (7,6), None)
        # If found, add object points, image points (after refining them)
        if ret == True:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            imgpoints.append(corners2)
            # Draw and display the corners
            cv2.drawChessboardCorners(img, (7,6), corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(500)
    print(objpoints)
    print(imgpoints)
cam1=cv2.VideoCapture(0)
ret,frame=cam1.read()
frame_width=cam1.get(cv2.CAP_PROP_FRAME_WIDTH)
frame_height=cam1.get(cv2.CAP_PROP_FRAME_HEIGHT)
video_fps=cam1.get(cv2.CAP_PROP_FPS)
print("values:",frame_width,frame_height,video_fps)
data=np.flip(frame,2)
data=data.ravel()
data=np.asfarray(data,dtype='f')
texture_data_frame=np.true_divide(data,255.0)
texture_data=[]
for i in range(0,100*100):
    texture_data.append(255/255)
    texture_data.append(100/255)
    texture_data.append(100/255)
    texture_data.append(255/255)
raw_data=array.array('f',texture_data)
width, height, channels, data = dpg.load_image("assets/images/o1z01.bmp")
with dpg.texture_registry(show=True):
    dpg.add_raw_texture(100,100,raw_data,format=dpg.mvFormat_Float_rgba,tag="texture_tag")
    dpg.add_dynamic_texture(width=width, height=height, default_value=data, tag="tex41")
    dpg.add_raw_texture(frame_width,frame_height,texture_data_frame,format=dpg.mvFormat_Float_rgb,tag="texture_cam",label="tex_1")
    pass
with dpg.window(label="Image tutorial"):
    dpg.add_image("texture_tag")
    dpg.add_image("tex41")
    dpg.add_button(label="start",callback=func)
    #dpg.add_image("texture_cam")
    with dpg.font_registry():
        default_font=dpg.add_font("assets/fonts/NotoSerifCJKjp-Medium.otf",30)
        font_qsb=dpg.add_font("assets/fonts/quicksand/Quicksand_Book.otf",30)
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
images = glob.glob('assets/images/*.bmp')

cv2.destroyAllWindows()
dpg.show_viewport()
dpg.show_metrics()
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
#cv2.destroyAllWindows()