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
chessboardSize=(5,5)
images = glob.glob('assets\\images\\calib_example\\*.tif')
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)
# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)
size_of_chessboard_squares_mm = 30
objp = objp * size_of_chessboard_squares_mm
# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.
def update_dynamic_texture(sender, app_data, user_data):
    new_color = dpg.get_value(sender)
    new_color[0] = new_color[0] / 255
    new_color[1] = new_color[1] / 255
    new_color[2] = new_color[2] / 255
    new_color[3] = new_color[3] / 255

    for i in range(0, 100 * 100 * 4):
        raw_data[i] = new_color[i % 4]
def func():
    print('func')
    dpg.configure_item(win,pos=(400,400))
    # for image in images:
    #     print(image)
    #     imgData = cv.imread(image)
    #     print(imgData)
    #     time.sleep(1)
    #     print("slept")
    #     data=np.flip(imgData,2)
    #     data=data.ravel()
    #     data=np.asfarray(data,dtype='f')
    #     texture_data_frame=np.true_divide(data,255.0)
    #     #dpg.set_value("texture_cam",texture_data_frame)
    #     dpg.set_value("raw_tex_1",texture_data_frame)
        
    #     gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    #     # Find the chess board corners
    #     ret, corners = cv.findChessboardCorners(gray, chessboardSize, None)
    #     print(ret)
    #     # If found, add object points, image points (after refining them)
    #     if ret == True:

    #         objpoints.append(objp)
    #         corners2 = cv.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
    #         imgpoints.append(corners)

    #         # Draw and display the corners
    #         cv.drawChessboardCorners(img, chessboardSize, corners2, ret)
    #         cv.imshow('img', img)
    #         cv.waitKey(1000)
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
        width, height, channels, data = dpg.load_image(res)
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
texture_data=[]
for i in range(0,frameSize[0]*frameSize[1]):
    texture_data.append(255/255)
    texture_data.append(100/255)
    texture_data.append(100/255)
    texture_data.append(255/255)
raw_data=array.array('f',texture_data)

#dpg.set_item_pos(tex_reg,pos=(400,400))
#dpg.configure_item(tex_reg,pos=(400,400))
with dpg.window(label="Image tutorial",tag="win") as win:
    with dpg.group() as tex_reg:
        with dpg.texture_registry(show=True,tag="tex_reg"):
            dpg.add_raw_texture(frameSize[0],frameSize[1],raw_data,format=dpg.mvFormat_Float_rgba,tag="raw_tex_1")
            #dpg.add_dynamic_texture(width=frameSize[0], height=frameSize[1], default_value=images[1], tag="tex41")
            pass
    print(dpg.get_item_pos(tex_reg))
    dpg.add_button(label="start script",callback=func)
    dpg.add_image("raw_tex_1")
    with dpg.font_registry():
        default_font=dpg.add_font("assets/fonts/JetBrainsMono2.304/JetBrainsMono-Medium.ttf",20)
    dpg.bind_font(default_font)
    with dpg.menu_bar(label="menuBar"):
        with dpg.menu(label="menu"):
            dpg.add_menu_item(label="Show Font Manager", callback=lambda:dpg.show_tool(dpg.mvTool_Font))

    dpg.show_tool(dpg.mvTool_ItemRegistry)
dpg.show_viewport()
dpg.set_viewport_always_top(False)
dpg.show_metrics()
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

img = cv.imread('assets/images/calib_example/Image4.tif')
h,  w = img.shape[:2]
newCameraMatrix, roi = cv.getOptimalNewCameraMatrix(cameraMatrix, dist, (w,h), 1, (w,h))



# Undistort
dst = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

cv.imwrite('ignored/caliResult1.png', dst)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]



# Undistort with Remapping
mapx, mapy = cv.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
dst = cv.remap(img, mapx, mapy, cv.INTER_LINEAR)

cv.imwrite('ignored/caliResult2.png', dst)
# crop the image
x, y, w, h = roi
dst = dst[y:y+h, x:x+w]




# Reprojection Error
mean_error = 0

for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], cameraMatrix, dist)
    error = cv.norm(imgpoints[i], imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error

print( "total error: {}".format(mean_error/len(objpoints)) )