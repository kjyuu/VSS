import dearpygui.dearpygui as dpg
import cv2
import array
import numpy as np
dpg.create_context()
dpg.create_viewport(title='Custom Title', width=850, height=1100)
dpg.setup_dearpygui()

cam1=cv2.VideoCapture(1)
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
with dpg.texture_registry(show=True):
    dpg.add_raw_texture(100,100,raw_data,format=dpg.mvFormat_Float_rgba,tag="texture_tag")
    dpg.add_raw_texture(frame_width,frame_height,texture_data_frame,format=dpg.mvFormat_Float_rgb,tag="texture_cam",label="tex_1")
with dpg.window(label="Image tutorial"):
    dpg.add_image("texture_tag")
    dpg.add_image("texture_cam")
dpg.show_viewport()
dpg.show_metrics()
while dpg.is_dearpygui_running():
    # insert here any code you would like to run in the render loop
    # you can manually stop by using stop_dearpygui()
    #print("this will run every frame")
    ret,frame=cam1.read()
    data=np.flip(frame,2)
    data=data.ravel()
    data=np.asfarray(data,dtype='f')
    texture_data_frame=np.true_divide(data,255.0)
    dpg.set_value("texture_cam",texture_data_frame)
    #print(frame.shape)
    
    #print(cam1.get(cv2.CAP_PROP_FPS))
    #if cv2.waitKey(1)==ord('q'):
    #    break
    dpg.render_dearpygui_frame()
cam1.release()
dpg.destroy_context()
#cv2.destroyAllWindows()

# print(cam1.get(cv2.CAP_PROP_FRAME_WIDTH),
# cam1.get(cv2.CAP_PROP_FRAME_HEIGHT),
# cam1.get(cv2.CAP_PROP_FPS),
# cam1.get(cv2.CAP_PROP_CONTRAST),
# cam1.get(cv2.CAP_PROP_BRIGHTNESS),
# cam1.get(cv2.CAP_PROP_SATURATION),
# cam1.get(cv2.CAP_PROP_HUE),
# cam1.get(cv2.CAP_PROP_GAIN),
# cam1.get(cv2.CAP_PROP_EXPOSURE),
# cam1.get(cv2.CAP_PROP_SHARPNESS),
# cam1.get(cv2.CAP_PROP_GAMMA),
# cam1.get(cv2.CAP_PROP_TEMPERATURE),
# cam1.get(cv2.CAP_PROP_TRIGGER),
# cam1.get(cv2.CAP_PROP_ZOOM),
# cam1.get(cv2.CAP_PROP_FOCUS),
# cam1.get(cv2.CAP_PROP_BACKLIGHT),
# cam1.get(cv2.CAP_PROP_PAN))


#print(frameWidth," x ",frameHeight," @ ",frameFps)