import dearpygui.dearpygui as dpg
import cv2
# dpg.create_context()
# dpg.create_viewport(title='Custom Title', width=850, height=1100)

# dpg.setup_dearpygui()
# dpg.show_viewport()
# dpg.start_dearpygui()
# dpg.destroy_context()

cam1=cv2.VideoCapture(1, cv2.CAP_DSHOW)
print(cam1.get(cv2.CAP_PROP_FRAME_WIDTH),
cam1.get(cv2.CAP_PROP_FRAME_HEIGHT),
cam1.get(cv2.CAP_PROP_FPS),
cam1.get(cv2.CAP_PROP_CONTRAST),
cam1.get(cv2.CAP_PROP_BRIGHTNESS),
cam1.get(cv2.CAP_PROP_SATURATION),
cam1.get(cv2.CAP_PROP_HUE),
cam1.get(cv2.CAP_PROP_GAIN),
cam1.get(cv2.CAP_PROP_EXPOSURE),
cam1.get(cv2.CAP_PROP_SHARPNESS),
cam1.get(cv2.CAP_PROP_GAMMA),
cam1.get(cv2.CAP_PROP_TEMPERATURE),
cam1.get(cv2.CAP_PROP_TRIGGER),
cam1.get(cv2.CAP_PROP_ZOOM),
cam1.get(cv2.CAP_PROP_FOCUS),
cam1.get(cv2.CAP_PROP_BACKLIGHT),
cam1.get(cv2.CAP_PROP_PAN))


#print(frameWidth," x ",frameHeight," @ ",frameFps)
while True:
    ret,frame=cam1.read()
    cv2.imshow('cam1',frame)
    print(frame.shape)
    
    #print(cam1.get(cv2.CAP_PROP_FPS))
    if cv2.waitKey(1)==ord('q'):
        break
cam1.release()
cv2.destroyAllWindows()