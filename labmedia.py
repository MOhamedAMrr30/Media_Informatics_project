import cv2
import numpy as np


fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))


cap = cv2.VideoCapture(0)


angle = 0
reflect = False
shear = 0

while True:
    
    ret, frame = cap.read()

    if ret:
      
        rot_mat = cv2.getRotationMatrix2D((frame.shape[1] / 2, frame.shape[0] / 2), angle, 1)
        frame = cv2.warpAffine(frame, rot_mat, (frame.shape[1], frame.shape[0]))

        
        if reflect:
            frame = cv2.flip(frame, 1)

        
        shear_mat = np.float32([[1, shear, 0], [0, 1, 0]])
        frame = cv2.warpAffine(frame, shear_mat, (frame.shape[1], frame.shape[0]))

       
        out.write(frame)

       
        cv2.imshow('frame', frame)

      
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('r'):
            angle = -90
        elif key == ord('l'):
            reflect = True
        elif key == ord('h'):
            shear += 0.2

    else:
        break

cap.release()
out.release()
cv2.destroyAllWindows()
