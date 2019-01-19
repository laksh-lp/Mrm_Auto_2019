import numpy as np
import cv2

cap = cv2.VideoCapture('rtsp://192.168.1.9/user=admin&password=&channel=1&stream=0.sdp?real_stream--rtp-caching=1')
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    #ret1, frame1 = cap1.read()
    frame=cv2.resize(frame,(480,360))
    # Display the resulting frame
    cv2.imshow('cam9',frame)
    #cv2.imshow('frame1',frame1)
cap = cv2.VideoCapture('rtsp://192.168.1.9/user=admin&password=&channel=2&stream=0.sdp')
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret1, frame1 = cap1.read()

    # Display the resulting frame
    cv2.imshow('frame',frame)
    cv2.imshow('frame1',frame1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
#cap1.release()
cv2.destroyAllWindows()
cap1.release()
cv2.destroyAllWindows()
