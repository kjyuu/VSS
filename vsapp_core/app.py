import os
import numpy as np
import cv2
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
def startDistortion(selectedFiles):
    print(np.size(selectedFiles))
    for file in selectedFiles:
        #check if file is image type
        if os.path.splitext(file)[1] in ['.jpg', '.png', '.jpeg', '.bmp','.tif']:
            print(file, "is an image file")
            true_dst=cv2.imread(file)
            src = cv2.imread("img2.png")

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