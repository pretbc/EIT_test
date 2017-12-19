#Motion detector

import argparse
import datetime
import imutils
import time
import cv2
import subprocess
import os
from random import randint

"""
def motionDetection(slot=0 , key=''):
        # construct the argument parser and parse the arguments
        ap = argparse.ArgumentParser()
        ap.add_argument("-v", "--video", help="path to the video file")
        ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
        args = vars(ap.parse_args())
        camera = cv2.VideoCapture(slot)
        time.sleep(0.25)
        # initialize the first frame in the video stream
        firstFrame = None

        # loop over the frames of the video
        while True:
                # grab the current frame and initialize the occupied/unoccupied
                # text
                (grabbed, frame) = camera.read()
                text = "Unoccupied"
         
                # if the frame could not be grabbed, then we have reached the end
                # of the video
                if not grabbed:
                        break
         
                # resize the frame, convert it to grayscale, and blur it
                frame = imutils.resize(frame, width=500)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                gray = cv2.GaussianBlur(gray, (21, 21), 0)
         
                # if the first frame is None, initialize it
                if firstFrame is None:
                        firstFrame = gray
                        continue
                # compute the absolute difference between the current frame and
                # first frame
                frameDelta = cv2.absdiff(firstFrame, gray)
                thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
         
                # dilate the thresholded image to fill in holes, then find contours
                # on thresholded image
                thresh = cv2.dilate(thresh, None, iterations=2)
                (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE) #CHAIN_
         
                # loop over the contours
                for c in cnts:
                        # if the contour is too small, ignore it
                        if cv2.contourArea(c) < args["min_area"]:
                                continue
         
                        # compute the bounding box for the contour, draw it on the frame,
                        # and update the text
                        (x, y, w, h) = cv2.boundingRect(c)
                        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        text = "Occupied"


                # draw the text and timestamp on the frame
                cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                        (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
         
                # show the frame and record if the user presses a key
                cv2.imshow("Security Feed", frame)
                #cv2.imshow("Thresh", thresh)
                #cv2.imshow("Frame Delta", frameDelta)
                key = cv2.waitKey(1) & 0xFF
         
                # if the `q` key is pressed, break from the lop
                if key == 'q':
                        break
         
        # cleanup the camera and close any open windows
        camera.release()
        cv2.destroyAllWindows()
"""

def channel(a,b,c):
        channelNum = [a,b,c]
        for element in channelNum:
                subprocess.call(['irsend','SEND_ONCE','newtv','KEY_'+element], shell=False)
                time.sleep(0.4)
        time.sleep(3)
        
def zappPlus(loop):
        for i in range (0,loop):
                subprocess.call(['irsend','SEND_ONCE','newtv','KEY_CHANNELUP'], shell=False)
                time.sleep(3)
                result()
                
def result():
        isChannelOK = cmd_output('stb.eit> getInfo',100)
        if isChannelOK:
                checkCH = channel_output('Selecting channel ',300) 
                with open('/home/pi/Desktop/EITresult.txt','a+')as file:
                        file.write(checkCH)
                        file.write('Channel OK\n')
        else:
                checkCH = channel_output('Selecting channel ',300)
                with open('/home/pi/Desktop/EITresult.txt','a+')as file:
                        file.write(checkCH)
                        file.write('Channel NOK\n')
        print checkCH
        time.sleep(7)


def cmd_output(to_find,lines):
    cmd = ('tail -n'+str(lines)+' /home/pi/Desktop/output.txt | grep -i "'+to_find+'"')
    output = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)
    result = output.stdout.read()
    print result
    if ' 00,' in result:
            return True
    elif ' 02' in result:
            return False

def channel_output(to_find,lines):
    cmd = ('tail -n'+str(lines)+' /home/pi/Desktop/output.txt | grep -i "'+to_find+'"')
    output = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)
    time.sleep(1)
    result = output.stdout.read()
    return result


def saveCrash(i):
        cmd = ('tail -n500 /home/pi/Desktop/output.txt')
        output = subprocess.Popen(cmd,stdout=subprocess.PIPE, shell=True)
        result = output.stdout.read()
        with open('/home/pi/Desktop/crash+'+str(i)+'.txt', 'a+')as file:
                file = file.write(result)


def checkChannel(idChannel):
        checkOK = channel_output('zapp on digit : '+idChannel,120)
        print(checkOK)
        if ('zapp on digit : '+idChannel) in checkOK:
                with open('/home/pi/Desktop/EITresult.txt','a+')as file:
                        file.write(checkOK)
                result()
                return False
        else:
                return True

                        
def main():
        for j in range(0,1000):
                chanelOK = True
                while chanelOK:
                        channel('2','6','6')
                        chanelOK = checkChannel('266')
                zappPlus(17)
                chanelOK = True
                while chanelOK:
                        channel('3','3','1')
                        chanelOK = checkChannel('331')
                zappPlus(30)

                
main()     
