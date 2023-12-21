import numpy as np
import cv2 as cv,cv2
import glob
import pickle
import dearpygui.dearpygui as dpg
import array
import time
dpg.create_context()
dpg.create_viewport(title='Custom Title', width=1300, height=900)
dpg.set_viewport_always_top(True)
dpg.setup_dearpygui()

# Definitions
frameSize = (640,480)
#chessboardSize=(12,13) # tif H x W
#chessboardSize=(35,49)
chessboardSize=(7,10)
# images = glob.glob('assets\\images\\calib_example\\*.tif')
#images = glob.glob('assets\\images\\o1z*.bmp')
images = glob.glob('assets\\images\\o3z02*.jpg')
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)
size_of_chessboard_squares_mm = 30
objp = objp * size_of_chessboard_squares_mm
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
def conv_img2raw(img,width,height):
    resized_img=cv2.resize(img, (width, height), interpolation=cv2.INTER_NEAREST)
    raw=np.flip(resized_img[:],2)
    raw=raw.ravel()
    raw=np.asfarray(raw,dtype='f')
    raw=np.true_divide(raw,255.0)
    return raw
def func():
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
        ret=False
        hgroup=dpg.add_group(horizontal=True,parent="win")
        ret, corners = cv2.findChessboardCorners(img, (chessboardSize[0],chessboardSize[1]),flags=cv2.CALIB_CB_ADAPTIVE_THRESH +cv2.CALIB_CB_FAST_CHECK +cv2.CALIB_CB_NORMALIZE_IMAGE)
        t=dpg.add_raw_texture(width=img.shape[1], height=img.shape[0], default_value=conv_img2raw(img,img.shape[1],img.shape[0]),format=dpg.mvFormat_Float_rgb,parent="tex_reg")
        dpg.add_image(t,parent=hgroup)
        if ret:
            print(ret)
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray,corners, (5,5), (-1,-1), criteria)
            imgpoints.append(corners2)
            img_corners = cv2.drawChessboardCorners(img,(chessboardSize[0],chessboardSize[1]), corners2, ret)
            t=dpg.add_raw_texture(width=img_corners.shape[1], height=img_corners.shape[0], default_value=conv_img2raw(img_corners,img_corners.shape[1],img_corners.shape[0]),format=dpg.mvFormat_Float_rgb,parent="tex_reg")
            dpg.add_image(t,parent=hgroup)
        else:
            print("No Checkerboard Found")
       
    # print(objpoints)
    # print(imgpoints)
texture_data=[]
for i in range(0,frameSize[0]*frameSize[1]):
    texture_data.append(255/255)
    texture_data.append(200/255)
    texture_data.append(100/255)
    texture_data.append(255/255)
raw_data=array.array('f',texture_data)

#dpg.set_item_pos(tex_reg,pos=(400,400))
#dpg.configure_item(tex_reg,pos=(400,400))
with dpg.window(label="Image tutorial",tag="win") as win:
    with dpg.group() as tex_reg:
        with dpg.texture_registry(tag="tex_reg"):
            dpg.add_raw_texture(frameSize[0],frameSize[1],raw_data,format=dpg.mvFormat_Float_rgba,tag="raw_tex_1")
            pass
    dpg.add_button(label="start script",callback=func)
    with dpg.font_registry():
        default_font=dpg.add_font("assets/fonts/JetBrainsMono2.304/JetBrainsMono-Medium.ttf",20)
    dpg.bind_font(default_font)
    with dpg.menu_bar(label="menuBar"):
        with dpg.menu(label="menu"):
            dpg.add_menu_item(label="Show About", callback=lambda:dpg.show_tool(dpg.mvTool_About))
            dpg.add_menu_item(label="Show Metrics", callback=lambda:dpg.show_tool(dpg.mvTool_Metrics))
            dpg.add_menu_item(label="Show Documentation", callback=lambda:dpg.show_tool(dpg.mvTool_Doc))
            dpg.add_menu_item(label="Show Debug", callback=lambda:dpg.show_tool(dpg.mvTool_Debug))
            dpg.add_menu_item(label="Show Style Editor", callback=lambda:dpg.show_tool(dpg.mvTool_Style))
            dpg.add_menu_item(label="Show Font Manager", callback=lambda:dpg.show_tool(dpg.mvTool_Font))
            dpg.add_menu_item(label="Show Item Registry", callback=lambda:dpg.show_tool(dpg.mvTool_ItemRegistry))

dpg.set_primary_window("win",True)
dpg.show_viewport()
dpg.set_viewport_always_top(False)
while dpg.is_dearpygui_running():
    dpg.render_dearpygui_frame()
dpg.destroy_context()
#cv2.destroyAllWindows()

############## CALIBRATION #######################################################
ret, cameraMatrix, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize, None, None)

# Save the camera calibration result for later use (we won't worry about rvecs / tvecs)
pickle.dump((cameraMatrix, dist), open( "ignored/calibration.pkl", "wb" ))
pickle.dump(cameraMatrix, open( "ignored/cameraMatrix.pkl", "wb" ))
pickle.dump(dist, open( "ignored/dist.pkl", "wb" ))


############## UNDISTORTION #####################################################

img = cv.imread('assets\\images\\calib_example\\Image4.tif')
cv.imwrite('ignored/caliResult0.png', img)
h,  w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))



# Undistort
dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
cv.imwrite('ignored/caliResult1a.png', dst)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('ignored/caliResult1.png', dst)


# Undistort with Remapping
mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)
cv.imwrite('ignored/caliResult2a.png', dst)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite('ignored/caliResult2.png', dst)



# Reprojection Error
mean_error = 0

for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error

print( "total error: {}".format(mean_error/len(objpoints)) )