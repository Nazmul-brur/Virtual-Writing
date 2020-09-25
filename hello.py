import cv2
import numpy as np


p, q, r = 200, 200, -1

cap = cv2.VideoCapture (0)

def take_inp(event, x1, y1, flag, param):
    global p, q, r
    if event == cv2.EVENT_LBUTTONDOWN:
        p = x1
        q = y1
        r = 1
cv2.namedWindow ("Dot_mat")
cv2.setMouseCallback ("Dot_mat", take_inp)

while True:

    _, input = cap.read ()
    input = cv2.flip (input, 1)

    gray_inp_img = cv2.cvtColor (input, cv2.COLOR_BGR2GRAY)

    cv2.imshow ("Dot_mat", input)

    if r == 1 or cv2.waitKey (30) == 27:
        cv2.destroyAllWindows ()
        break


stp = 4



old_pts = np.array ([[p, q]], dtype=np.float32).reshape (-1, 1, 2)

mask = np.zeros_like (input)



while True:
    _, new_input = cap.read ()
    new_input = cv2.flip (new_input, 1)
    new_gray = cv2.cvtColor (new_input, cv2.COLOR_BGR2GRAY)
    new_pts, status, err = cv2.calcOpticalFlowPyrLK (gray_inp_img,
                                                     new_gray,
                                                     old_pts,
                                                     None, maxLevel=1,
                                                     criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT,
                                                               14, 0.08))

    for i, j in zip (old_pts, new_pts):
        p, q = j.ravel ()
        a, b = i.ravel ()
        if cv2.waitKey (2) & 0xff == ord ('g'):
            stp = 1

        elif cv2.waitKey (2) & 0xff == ord ('b'):
            stp = 0
        elif cv2.waitKey (2) & 0xff == ord ('w'):
            stp= 2
        elif cv2.waitKey (2) & 0xff == ord ('r'):
            stp=3

        elif cv2.waitKey (2) & 0xff == ord ('c'):
            mask = np.zeros_like (new_input)

        if stp == 0:
            mask = cv2.line (mask, (a, b), (p, q), (255, 0, 0), 6)
        elif stp==2:
            mask = cv2.line (mask, (a, b), (p, q), (255, 255, 255), 6)
        elif stp==3:
            mask = cv2.line (mask, (a, b), (p, q), (0, 0, 255), 6)


        cv2.circle (new_input, (p, q), 6, (0, 0, 255), -1)

    new_inp_img = cv2.addWeighted (mask, 0.3, new_input, 0.7, 0)


    cv2.imshow ("Result", new_input)
    cv2.imshow ("canvus", mask)


    gray_inp_img = new_gray.copy ()
    old_pts = new_pts.reshape (-1, 1, 2)

    if cv2.waitKey (1) & 0xff == 27:
        break



cv2.destroyAllWindows ()
cap.release ()
