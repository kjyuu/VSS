import os
import numpy as np
import cv2
import dearpygui.dearpygui as dpg
import math
def conv_img2raw(img,width,height):
    resized_img=cv2.resize(img, (width, height), interpolation=cv2.INTER_NEAREST)
    raw=np.flip(resized_img[:],2)
    raw=raw.ravel()
    raw=np.asfarray(raw,dtype='f')
    raw=np.true_divide(raw,255.0)
    return raw
def SaveAllImages(list_of_images,path):
    print("saving images")
    # start by deleting all files in path
    for file in os.listdir(path):
        os.remove(os.path.join(path,file))
    for i in range(len(list_of_images)):
        id,image,type=list_of_images[i]
        print(id,image.shape,type)
        if type=="original":
            cv2.imwrite(os.path.join(path,str(id)+"_original.png"),image)
        elif type=="scaled":
            cv2.imwrite(os.path.join(path,str(id)+"_scaled.png"),image)
        elif type=="distorted":
            cv2.imwrite(os.path.join(path,str(id)+"_distorted.png"),image)
        elif type=="chessboard":
            cv2.imwrite(os.path.join(path,str(id)+"_chessboard.png"),image)
        elif type=="undistorted":
            cv2.imwrite(os.path.join(path,str(id)+"_undistorted.png"),image)
        elif type=="undistorted_roi":
            cv2.imwrite(os.path.join(path,str(id)+"_undistorted_cropped.png"),image)
            
    return None
def DrawImagesInParent(list_of_images,results_parent,results_tex_reg):
    dpg.delete_item(results_parent, children_only=True)
    dpg.delete_item(results_tex_reg, children_only=True)
    group_results_horizontal=[]
    group_results_vertical=[]
    #sort list of images by id
    dpg.add_button(label="Save",parent=results_parent, callback=lambda:SaveAllImages(list_of_images,"ignored\\results"))
    list_of_images.sort(key=lambda x: x[0])
    for i in range(len(list_of_images)):
        id,image,type=list_of_images[i]
        if type=="original": # original will always be new image, add groups here
            group_results_horizontal=dpg.add_group(horizontal=True,parent=results_parent)
            group_results_vertical=dpg.add_group(horizontal=False,parent=group_results_horizontal)
            dpg.add_text("Original",parent=group_results_vertical)
            t=dpg.add_raw_texture(width=image.shape[1], height=image.shape[0], default_value=conv_img2raw(image,image.shape[1],image.shape[0]),format=dpg.mvFormat_Float_rgb,parent=results_tex_reg)
            dpg.add_image(t,parent=group_results_vertical)
        elif type=="scaled":
            group_results_vertical=dpg.add_group(horizontal=False,parent=group_results_horizontal)
            dpg.add_text("Scaled",parent=group_results_vertical)
            t=dpg.add_raw_texture(width=image.shape[1], height=image.shape[0], default_value=conv_img2raw(image,image.shape[1],image.shape[0]),format=dpg.mvFormat_Float_rgb,parent=results_tex_reg)
            dpg.add_image(t,parent=group_results_vertical)
        elif type=="distorted":
            group_results_vertical=dpg.add_group(horizontal=False,parent=group_results_horizontal)
            dpg.add_text("Distorted",parent=group_results_vertical)
            t=dpg.add_raw_texture(width=image.shape[1], height=image.shape[0], default_value=conv_img2raw(image,image.shape[1],image.shape[0]),format=dpg.mvFormat_Float_rgb,parent=results_tex_reg)
            dpg.add_image(t,parent=group_results_vertical)
        elif type=="chessboard":
            group_results_vertical=dpg.add_group(horizontal=False,parent=group_results_horizontal)
            dpg.add_text("Found chessboard corners",parent=group_results_vertical)
            t=dpg.add_raw_texture(width=image.shape[1], height=image.shape[0], default_value=conv_img2raw(image,image.shape[1],image.shape[0]),format=dpg.mvFormat_Float_rgb,parent=results_tex_reg)
            dpg.add_image(t,parent=group_results_vertical)
        elif type=="undistorted":
            group_results_vertical=dpg.add_group(horizontal=False,parent=group_results_horizontal)
            dpg.add_text("Undistorted",parent=group_results_vertical)
            t=dpg.add_raw_texture(width=image.shape[1], height=image.shape[0], default_value=conv_img2raw(image,image.shape[1],image.shape[0]),format=dpg.mvFormat_Float_rgb,parent=results_tex_reg)
            dpg.add_image(t,parent=group_results_vertical)
        elif type=="undistorted_roi":
            group_results_vertical=dpg.add_group(horizontal=False,parent=group_results_horizontal)
            dpg.add_text("Undistorted Cropped",parent=group_results_vertical)
            t=dpg.add_raw_texture(width=image.shape[1], height=image.shape[0], default_value=conv_img2raw(image,image.shape[1],image.shape[0]),format=dpg.mvFormat_Float_rgb,parent=results_tex_reg)
            dpg.add_image(t,parent=group_results_vertical)
    return None
def Calibrate(list_of_filepaths, chessboardSize, size_of_chessboard_squares_mm, results_parent,calib_tex_reg,calib_enable=False,enable_scaling=False,target_height=0,target_width=0,scale_factor_x=0,scale_factor_y=0):
    if calib_enable==True:
        # implement cv2 calibration on list of images and return camera matrix and distortion coefficients
        objpoints = []  # 3D points in real world space
        imgpoints = []  # 2D points in image plane
        list_of_images = []
        for filepath in list_of_filepaths:
            if os.path.splitext(filepath)[1] in ['.jpg', '.png', '.jpeg', '.bmp','.tif']:
                image = cv2.imread(filepath)
                print(os.path.basename(filepath), "is an image file with", image.shape[1], "x", image.shape[0], "pixels")
                list_of_images.append(image)
        objp = np.zeros((chessboardSize[0] * chessboardSize[1], 3), np.float32) # chessboardSize[0] is height, chessboardSize[1] is width
        objp[:, :2] = np.mgrid[0:chessboardSize[0], 0:chessboardSize[1]].T.reshape(-1, 2) # x,y coordinates, T.reshape(-1,2) flattens the array
        objp *= size_of_chessboard_squares_mm # scale by size of squares
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001) # termination criteria for subpixel corner detection, max 30 iterations or epsilon 0.001
        list_of_images_to_draw=[] # first field is id, second is image, third is type
        
        id=0
        for image in list_of_images: # loop through images
            id+=1
            frameSize = (image.shape[1], image.shape[0]) # get frame size
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
            if enable_scaling:
                resized=ResizeImage(image,target_height=target_height,target_width=target_width,scale_factor_x=scale_factor_x,scale_factor_y=scale_factor_y)
                list_of_images_to_draw.append((id,resized,'original'))#resized counted as original only for scaling purposes
            else:
                list_of_images_to_draw.append((id,image,'original'))
                
            # Find the chessboard corners
            ret, corners = cv2.findChessboardCorners(gray, chessboardSize, None)
            # flags flags=cv2.CALIB_CB_ADAPTIVE_THRESH +cv2.CALIB_CB_FAST_CHECK +cv2.CALIB_CB_NORMALIZE_IMAGE +cv2.CALIB_CB_FILTER_QUADS +cv2.CALIB_CB_CLUSTERING
            # If found, add object points and image points
            if ret:
                objpoints.append(objp) # append object points
                #imgpoints.append(corners) # append image points without refining them
                corners2 = cv2.cornerSubPix(gray,corners, (5,5), (-1,-1), criteria)
                imgpoints.append(corners2) # [imageNumber][cornerNumber][?][x,y]
                imgcopy=image.copy()
                img_with_corners = cv2.drawChessboardCorners(imgcopy, chessboardSize, corners2, ret) # draw corners on image
                #img_with_corners=cv2.circle(img_with_corners,(int(round(imgpoints[-1][0][0][0])),int(round(imgpoints[-1][0][0][1]))),50,(0,0,255),-1)
                #img_with_corners=cv2.line(img_with_corners,(int(round(imgpoints[-1][-1][0][0])),int(round(imgpoints[-1][-1][0][1]))),(int(round(imgpoints[-1][0][0][0])),int(round(imgpoints[-1][0][0][1]))),(0,255,0),5)
                #img_with_corners=cv2.putText(img_with_corners,"Hi",(int(round(imgpoints[-1][-1][0][0]))-50,int(round(imgpoints[-1][-1][0][1]))+50),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,0),2,cv2.LINE_AA)
                if enable_scaling:
                    resized=ResizeImage(img_with_corners,target_height=target_height,target_width=target_width,scale_factor_x=scale_factor_x,scale_factor_y=scale_factor_y)
                    list_of_images_to_draw.append((id,resized,'chessboard'))
                else:
                    list_of_images_to_draw.append((id,img_with_corners,'chessboard'))
            else:
                print("No Checkerboard Found")
        # Calibrate camera
        if len(objpoints) == 0:
            print("No checkerboard found in images")
            return None, None
        else: 
            ret, cameraMatrix, distCoeffs, rvecs, tvecs, stdDeviationsIntrinsics, stdDeviationsExtrinsics, perViewErrors = cv2.calibrateCameraExtended(objpoints, imgpoints, frameSize, None, None) # returns camera matrix, distortion coefficients, rotation and translation vectors
            fovx, fovy, focalLength, principalPoint, aspectRatio=cv2.calibrationMatrixValues(cameraMatrix, frameSize, 4.8, 3.6)
            newCameraMatrix, roi = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, frameSize, 1)
            map_undist_1,map_undist_2=cv2.initUndistortRectifyMap(cameraMatrix, distCoeffs, None, newCameraMatrix, frameSize, cv2.CV_32FC1)
            id=0
            for image in list_of_images:
                id+=1
                undist = cv2.remap(image,map_undist_1,map_undist_2,cv2.INTER_CUBIC)
                undist=cv2.rectangle(undist,roi,(255,0,0),2)
                undist_roi=undist[roi[1]:roi[1]+roi[3],roi[0]:roi[0]+roi[2]]
                pts_src=np.array(imgpoints[id-1][:],dtype=np.float64)
                pts_src=pts_src.reshape(-1,2)
                pts_undst=cv2.undistortImagePoints(pts_src, cameraMatrix, distCoeffs)
                pts_undst=pts_undst.reshape(-1,2)
                # draw arrow for every point in pts_src and pts_undst
                for i in range(pts_src.shape[0]):
                    temp_point=np.array([pts_src[i,0],pts_src[i,1]])
                    temp_point2=np.array([pts_undst[i,0],pts_undst[i,1]])
                    scale=50
                    point_diff=temp_point2-temp_point
                    endpoint_scaled=temp_point+point_diff*scale
                    undist=cv2.arrowedLine(undist,(int(temp_point[0]),int(temp_point[1])),(int(endpoint_scaled[0]),int(endpoint_scaled[1])),(0,0,255),2)
                    
                if enable_scaling:
                    resized=ResizeImage(undist,target_height=target_height,target_width=target_width,scale_factor_x=scale_factor_x,scale_factor_y=scale_factor_y)
                    list_of_images_to_draw.append((id,resized,'undistorted'))
                    resized_roi=ResizeImage(undist_roi,target_height=target_height,target_width=target_width,scale_factor_x=scale_factor_x,scale_factor_y=scale_factor_y)
                    list_of_images_to_draw.append((id,resized_roi,'undistorted_roi'))
                else:
                    list_of_images_to_draw.append((id,undist,'undistorted'))
                    list_of_images_to_draw.append((id,undist_roi,'undistorted_roi'))
        DrawImagesInParent(list_of_images_to_draw,results_parent,calib_tex_reg)
            
        return cameraMatrix, distCoeffs
    else:
        return None, None
def ResizeImage(inputImage,target_width=0,target_height=0,scale_factor_x=0,scale_factor_y=0):
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
def ResizeAndDistort(selected_files,draw_parent,draw_tex_reg,enable_original=False,enable_scaling=False,enable_distortion=False,Cx=-1,Cy=-1,dstBC_k1=0,dstBC_k2=0,dstBC_k3=0,dstBC_p1=0,dstBC_p2=0,target_height=0,target_width=0,scale_factor_x=0,scale_factor_y=0):
    if enable_scaling or enable_distortion:
        list_of_images_to_draw=[]
        id=0
        for file in selected_files:
            #check if file is of image type
            if os.path.splitext(file)[1] in ['.jpg', '.png', '.jpeg', '.bmp','.tif']:
                image = cv2.imread(file)
                id+=1
                print("scaling status:",enable_scaling)
                # if original image is enabled, add original, else if scaling is enabled, add scaled image as original, if both enabled, add original and scaled if both disabled, skip
                h, w, c = 0,0,0
                if enable_original:
                    list_of_images_to_draw.append((id,image,'original'))
                    (h, w, c) = image.shape
                    if enable_scaling:
                        resized=ResizeImage(image,target_height=target_height,target_width=target_width,scale_factor_x=scale_factor_x,scale_factor_y=scale_factor_y)
                        list_of_images_to_draw.append((id,resized,'scaled'))
                        (h, w, c) = resized.shape
                elif enable_scaling:
                    resized=ResizeImage(image,target_height=target_height,target_width=target_width,scale_factor_x=scale_factor_x,scale_factor_y=scale_factor_y)
                    list_of_images_to_draw.append((id,resized,'original'))
                    (h, w, c) = resized.shape
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
                    list_of_images_to_draw.append((id,dst,'distorted'))
        DrawImagesInParent(list_of_images_to_draw,draw_parent,draw_tex_reg)
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