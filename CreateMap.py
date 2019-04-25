import cv2, numpy as np
import argparse
from matplotlib import pyplot as plt

def make_480p(cap):
  cap.set(3,640)
  cap.set(4,480)

def run():

  # setting up camera
  cap = cv2.VideoCapture(0)

  make_480p(cap)

  ZoneA = None
  ZoneB = None
  TriTrackLoc = None
  RotationA = None
  RotationB = None


  # initialise tracker
  tracker = cv2.TrackerCSRT_create()
  print("starting video stream")

  while(True):
    # Capture frame
    ret, frame = cap.read()

    # define key presses for commands later in script
    key = cv2.waitKey(1) & 0xFF

    # capture resolution for later use in script
    resolution = np.shape(frame)
    ymax, xmax,_ = resolution

    # filter out yellow and green and black here using colourspace -----------------------




    
    # canny edge detect
    edges = cv2.Canny(frame,200,250)

    # dilate the edges a bit to help fill contours
    kernel = np.ones((1,1),np.uint8)
    edges = cv2.dilate(edges,kernel)

    # find all available contours
    contours,hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



    # click t, to locate tri-track
    if TriTrackLoc is not None:
      (success,box) = tracker.update(frame)

      if success:
        (xT,yT,wT,hT) = [int(v) for v in box]
        cv2.rectangle(frame,(xT,yT),(xT+wT,yT+hT),(0,255,0),2)
      
        xT_center = str((xT+wT/2))
        yT_center = str(ymax-(yT-hT/2))
        targetFile = open('/home/team-g/catkin_ws/src/ros_dom/src/TriTrackLoc.txt','w')
        targetFile.write(xT_center+'\n'+yT_center)
        targetFile.close()

    if key == ord('t'):
      TriTrackLoc = cv2.selectROI(frame)
      xT,yT,wT,hT = TriTrackLoc
      print(TriTrackLoc)
      tracker.init(frame,TriTrackLoc)


    # click c, to export map -------------------------------------------------------------
    if key == ord('c'):
      contourLines = np.zeros((edges.shape[0], edges.shape[1], 3), dtype=np.uint8)
      for i in range(len(contours)):
          color = (255,255,255)
          cv2.drawContours(contourLines, contours, i, color, -1)     
          
      # export image Shehroz's mapping
      
      cv2.imwrite('/home/team-g/catkin_ws/src/provide_map/map/PUCKWANK.jpg', np.invert(edges))
      # Show in a window
      #cv2.imshow('NOT',e np.invert(contourLines))
      cv2.imshow('image',np.invert(edges))
    # ------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------
    



    if RotationA is not None:
      (success,box) = tracker.update(frame)

      if success:
        (xRA,yRA,wRA,hRA) = [int(v) for v in box]
        cv2.rectangle(frame,(xRA, yRA),(xRA+wRA,yRA+hRA),(0,255,255),2)

    if RotationB is not None:
      (success,box) = tracker.update(frame)

      if success:
        (xRB,yRB,wRB,hRB) = [int(v) for v in box]
        cv2.rectangle(frame,(xRB, yRB),(xRB+wRB,yRB+hRB),(255,255,0),2)

    # click r, for rotation tests
    if key == ord('e'):
      RotationA = cv2.selectROI(frame)
      xRA, yRA, wRA, hRA = RotationA
      tracker.init(frame,RotationA)
      
    
    if key == ord('r'):
      RotationB = cv2.selectROI(frame)
      xRB, yRB, wRB, hRB = RotationB
      tracker.init(frame,RotationB)




    # click d, to choose zones -----------------------------------------------------------
    if key == ord('d'):
      ZoneA = cv2.selectROI(frame)
      xA, yA, wA, hA = ZoneA
      
      print(ZoneA)
      # ZoneB = cv2.selectROI(frame)
      # xB, yB, wB, hB = ZoneB
      # print(ZoneB)

    # if zone has been chosen then draw onto frame for visualisation  
    if ZoneA is not None:
      cv2.rectangle(frame,(xA,yA),(xA+wA,yA+hA),(0,255,0),2)
      #cv2.rectangle(frame,(xB,yB),(xB+wB,yB+hB),(0,255,0),2)

      # to adjust for coordinate differences between rviz and opencv
      x = str((xA+wA/2))
      y = str(ymax-(yA+hA/2))
      # print these coordinates to a txt file for rviz to use as obstacles      
      targetFile = open('/home/team-g/catkin_ws/src/simple_navigation_goals/src/TargetZone.txt','w')
      targetFile.write(x+'\n'+y)
      targetFile.close()
    # ------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------
      
    # Display Video Feed
    cv2.imshow('Camera Feed',frame)
    

    # Option to exit Video Capture
    if key == ord('q'):
      break
    
  cap.release()
  cv2.destroyAllWindows()

if __name__ == "__run__":

  run()

  
