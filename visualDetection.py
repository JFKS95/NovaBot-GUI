from __future__ import print_function
import sys
import cv2
from random import randint
import math, numpy as np

def nothing(x):
    pass

def VisualErrorCodeCheck(image, counter, startSeq, rawLightData, errorCodeSeq, visualErrorCode, deltaFlashX, deltaFlashY):
    # image processing
    visCode = "NODATA"
    image = cv2.medianBlur(image,3)
    hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

    # hard coded HSV Colour Ranges
    lower_green, upper_green = (np.array([58,46,155]), np.array([84,255,255]))
    lower_blue, upper_blue = (np.array([100,67,221]), np.array([120,255,255]))
    lower_red, upper_red = (np.array([0,0,0]) , np.array([16,255,255]))
    # thresholding HSV image with defined colour ranges
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    blue_mask = cv2.inRange(hsv, lower_blue, upper_blue)
    red_mask = cv2.inRange(hsv, lower_red, upper_red)
    # bitwise-AND the mask and frame
    res_green = cv2.bitwise_and(image, image, mask=green_mask)
    res_blue = cv2.bitwise_and(image, image, mask=blue_mask)
    res_red = cv2.bitwise_and(image, image, mask=red_mask)
    # add the seperate images together to see each on the same output feed
    res = np.add(res_green, res_blue)
    res = np.add(res, res_red)
    cv2.imshow('res_green', res_green)
    cv2.imshow('res_blue', res_blue)
    cv2.imshow('res_red', res_red)

    # find values of array
    maxGreen = np.amax(res_green)
    maxBlue = np.amax(res_blue)
    maxRed = np.amax(res_red)

    #print(startSeq)
    # ERROR CODE ANALYSIS
    # wait for Red to begin recording
    #print('counter: ', counter)
    #print('rawLightData: ', rawLightData)
    #print('errorCodeSeq: ', errorCodeSeq)


    if startSeq == 0:
        if maxRed >= 170:
            startSeq = 1
            maxRedPos = np.where(res_red == np.amax(res_red))
            maxRedVal = np.amax(res_red)

            flashPosY, flashPosX = (int(np.round(np.mean(maxRedPos[0]))), int(np.round(np.mean(maxRedPos[1]))))
            deltaFlashX, deltaFlashY = (flashPosX - p1[0], flashPosY - p1[1])
            print(deltaFlashX, deltaFlashY)
            # print(maxRed)
            print('Red detected, starting visual error code detection')


    # when recording, putting values into raw matrix of colours
    if startSeq == 1:
        if maxRed >= 170:
            rawLightData.append('R')
        elif maxGreen >= 170:
            rawLightData.append('G')
        elif maxBlue >= 170:
            rawLightData.append('B')
        else:
            rawLightData.append('Z')

        if counter == 0:
            # put first detected Red into errorCodeSeq array
            errorCodeSeq.append(rawLightData[counter])
        else:
            # for consequent colours, only put into errorCodeSeq array if
            # different from previous
            if rawLightData[counter] is not rawLightData[counter-1]:
                errorCodeSeq.append(rawLightData[counter])
                print(errorCodeSeq)

                if len(errorCodeSeq) > max(len(Normal), len(V001), len(V002)):
                    print('incorrect Sequence detected, starting again')
                    visCode = "NODATA"
                    startSeq = 0
                    counter = -1
                    errorCodeSeq = []
                    rawLightData = []
                elif errorCodeSeq == Normal:
                    #RBG
                    print('sequence:',errorCodeSeq)
                    print('error code: Normal Operation')
                    visCode = "ERROR"
                    errorCodeDetection = 0
                    visualErrorCode = 0
                elif errorCodeSeq == V001:
                    #RRBG
                    print('sequence:', errorCodeSeq)
                    print('error code: V001')
                    visCode = "V001"
                    errorCodeDetection = 0
                    visualErrorCode = 0
                elif errorCodeSeq == V001alt:
                    #RRBG
                    print('sequence:', errorCodeSeq)
                    print('error code: V001')
                    visCode = "V001"
                    errorCodeDetection = 0
                    visualErrorCode = 0
                elif errorCodeSeq == V002:
                    #RRGB
                    print('sequence:', errorCodeSeq)
                    print('error code: V002')
                    visCode = "V002"
                    errorCodeDetection = 0
                    visualErrorCode = 0
                elif errorCodeSeq == V002alt:
                    #RRGB
                    print('sequence:', errorCodeSeq)
                    print('error code: V002')
                    visCode = "V002"
                    errorCodeDetection = 0
                    visualErrorCode = 0

        counter = counter + 1
    return(counter, startSeq, rawLightData, errorCodeSeq, visualErrorCode, deltaFlashX, deltaFlashY, visCode)


def run():
  vcode = "NODATA"
  # initialising video capture object to read frames from
  cap = cv2.VideoCapture(0)

  print('Starting program ...')

  # INITIALISE VARIABLES -------------------------------------------------------
  bboxes = []             # Selected ROIs and ROI colours
  colors = []
  manualROIselection = 1  # Manual ROI selection activated
  trackingStage = 0       # Tracking stage deactivated
  exitProgram = 0         # Exit program for Tracking stage deactivated


  # AUTOMATED ROI DETECTION ----------------------------------------------------
  print('Automated ROI Detection Stage ... ')
  while True:
      key = cv2.waitKey(25) & 0xFF
      success, frame = cap.read()

      if not success:
          print('Lost connection with video stream at automated ROI Detection stage ...')
          sys.exit()

      # ------------------------------------------------- #
      # detection stage goes here ----------------------- #
      # ------------------------------------------------- #


      # enter manual ROI selection
      if key == ord('m'):
          manualROIselection = 1
          break
      # enter tracking with detected ROIs
      elif key == ord('t'):
          manualROIselection = 0
          break

      cv2.imshow('Video Stream', frame)
      if key == ord('q'):
          exitProgram = 1
          break

  # MANUAL ROI SELECTION -------------------------------------------------------
  # while loop is not necessarily needed here, but kept for future flexibility
  # if further functionality is needed during this stage
  while True:
      key = cv2.waitKey(1) & 0xFF
      success, frame = cap.read()
      if not success:
          print('Lost connection with video stream at manual ROI Selection stage ...')
          sys.exit(1)
      if exitProgram == 1:
          break

      # detected ROIs are to be used, pass through this stage
      if manualROIselection == 0:
          break

      # ROIs are to be manually selected
      elif manualROIselection == 1:
          print('Manual ROI Selection Stage ...')
          while True:
              bbox = cv2.selectROI('Select Region of Interest', frame)
              bboxes.append(bbox)
              colors.append((randint(64, 255), randint(64, 255), randint(64, 255)))
              key = cv2.waitKey(0) & 0xFF
              if key == ord('q'):
                  cv2.destroyWindow('Select Region of Interest')
                  print('Selected bounding boxes {}'.format(bboxes))
                  break
      break



  # TRACKING STAGE -------------------------------------------------------------
  # initialise VARIABLES
  counter = 0
  startSeq = 0
  rawLightData = []
  errorCodeSeq = []
  visualErrorCode = 0
  chosenROI = 0   # for incrementing between ROIs
  visualErrorCode = 0     # visualErrorCode is deactivated
  deltaFlashX, deltaFlashY = None, None

  # initialising error codes
  Normal = ['R','Z','B','Z','G',      'Z','R','Z','B','Z','G']
  V001 = ['R', 'Z', 'R', 'Z', 'B', 'Z', 'G',      'Z','R', 'Z', 'R', 'Z', 'B', 'Z', 'G']
  V001alt = ['R', 'Z', 'B', 'Z', 'G',      'Z','R', 'Z', 'R', 'Z', 'B', 'Z', 'G']
  V002 = ['R', 'Z', 'R', 'Z', 'G', 'Z', 'B',      'Z','R', 'Z', 'R', 'Z', 'G', 'Z', 'B', ]
  V002alt = ['R', 'Z', 'G', 'Z', 'B',      'Z','R', 'Z', 'R', 'Z', 'G', 'Z', 'B', ]

  print('Tracking Stage ...')
  while True:
      key = cv2.waitKey(1) & 0xFF
      success, frame = cap.read()
      #frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
      if not success:
          print('Lost connection with video stream at Tracking stage ...')
          sys.exit()
      if exitProgram == 1:
          break

      # Create MultiTracker object
      multiTracker = cv2.MultiTracker_create()
      # Initialise MultiTracker
      for bbox in bboxes:
          multiTracker.add(cv2.TrackerCSRT_create(), frame, bbox)

      # Process Video and Track objects
      while cap.isOpened():
          key = cv2.waitKey(1) & 0xFF
          success, frame = cap.read()
          if not success:
              break

          # tracker updated for current frame
          success, boxes = multiTracker.update(frame)
          # drawing boxes for visualisation of tracked objects
          for i, newbox in enumerate(boxes):
              p1 = (int(newbox[0]), int(newbox[1]))
              p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
              cv2.rectangle(frame, p1, p2, colors[i], 2, 1)



          # PROCESS VISUAL ERROR CODES -----------------------------------------

          if key == ord('e'):
              print('Error Code Check')
              visualErrorCode = 1

          # option to increment through the ROIs being tracked
          if key == ord('n'):
              print('boxes shape: ', np.shape(boxes))
              chosenROI = chosenROI + 1
              # if increments above max number of ROIs, reset
              if (chosenROI+1) > np.shape(boxes)[0]:
                  chosenROI = 0
              print('starting scan again ... ')
              print('chosenROI is now: ', chosenROI)
              # ROIs have been switched, so start again
              startSeq = 0
              counter = 0
              errorCodeSeq = []
              rawLightData = []

          # CREATE MOVING MASKS
          if visualErrorCode == 1:
              # black video sized box for mask
              mask = np.zeros((np.shape(frame)), dtype = "uint8")
              # create mask using currently chosen ROI
              p1 = (int(boxes[chosenROI][0]), int(boxes[chosenROI][1]))
              p2 = (int(boxes[chosenROI][0] + boxes[chosenROI][2]), int(boxes[chosenROI][1] + boxes[chosenROI][3]))
              cv2.rectangle(mask, p1, p2, (255,255,255), -1)
              maskedImg = cv2.bitwise_and(frame, mask)
              if deltaFlashX and deltaFlashY is not None:
                  mask = np.zeros((np.shape(frame)), dtype = "uint8")
                  cv2.circle(mask, (deltaFlashX + p1[0] , deltaFlashY + p1[1]), 15, (255,255,255), -1)
                  FlashCircle = cv2.bitwise_and(frame, mask)
                  cv2.imshow('',FlashCircle)
              cv2.imshow('mask2',maskedImg)
              # running visual error code check on the current mask selected
              counter, startSeq, rawLightData, errorCodeSeq, visualErrorCode, deltaFlashX, deltaFlashY = VisualErrorCodeCheck(maskedImg, counter, startSeq, rawLightData, errorCodeSeq, visualErrorCode, deltaFlashX, deltaFlashY)
              
          elif visualErrorCode ==0:
              pass
          vcode = visCode
          cv2.imshow('Video Stream', frame)


          if key == ord('q'):
              print('Exitting program ...')
              exitProgram = 1
              break


  print('Program Shutdown ...')
  cap.release()
  cv2.destroyAllWindows()
  return vcode

if __name__ == "__run__":

  run(VisualErrorCodeCheck(maskedImg, counter, startSeq, rawLightData, errorCodeSeq, visualErrorCode, deltaFlashX, deltaFlashY))
  #cap.release()
  #cv2.destroyAllWindows()
  #sys.exit()

  
