import cv2                                              #cv2 is the library that is used for image processing
import numpy as np
import matplotlib.pyplot as plt

def make_coordinates(image,line_parameters):
    slope,intercept=line_parameters
    y1=image.shape[0]
    y2=int(y1*(3/5))              
    x1=int((y1-intercept)/slope)
    x2=int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])

def average_slope_intercept(image,lines):
    left_fit=[]
    right_fit=[]
    for line in lines:
        x1,y1,x2,y2=line.reshape(4)
        parameters=np.polyfit((x1,x2),(y1,y2),1)
        slope=parameters[0]
        intercept=parameters[1]
        if slope<0:
            left_fit.append((slope,intercept))
        else:
            right_fit.append((slope,intercept))
    left_fit_average=np.average(left_fit,axis=0)
    right_fit_average=np.average(right_fit,axis=0)
    left_line=make_coordinates(image,left_fit_average)
    right_line=make_coordinates(image,right_fit_average)
    return np.array([left_line,right_line])

def canny(image):
    gray=cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)        #it converts the lane_image into black and white image which is faster in image processing
    blur=cv2.GaussianBlur(gray,(5,5),0)                     #gaussian blur is used to reduce the noise and smoothen the image  we took kernel 5,5 which is mostly used
    canny=cv2.Canny(blur,50,150)                            #it marks the whiteline when the pixel adjacent to the pixel is higher
    return canny

def display_lines(image,lines):
    line_image=np.zeros_like(image)
    if lines is not None:
        for x1,y1,x2,y2 in lines:
            # x1,y1,x2,y2=line.reshape(4)
            cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10)
    return line_image

def region_of_interest(image):
    height=image.shape[0]
    polygons=np.array([[(200,height),(1100,height),(550,250)]])
    mask=np.zeros_like(image)                               #it will bring a black image of same width and height of lane_image, why black means zeros_like means 0 intensity which means black
    cv2.fillPoly(mask,polygons,255)
    masked_image=cv2.bitwise_and(image,mask)
    return masked_image

# image=cv2.imread('test_image.jpg')                      #to read the image
# lane_image=np.copy(image)                               #we store copy of image in other variable called lane_image
# canny_image=canny(lane_image)
# cropped_image=region_of_interest(canny_image)
# lines=cv2.HoughLinesP(cropped_image,2, np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
# averaged_lines=average_slope_intercept(lane_image,lines)
# line_image=display_lines(lane_image,averaged_lines)
# combo_image=cv2.addWeighted(lane_image,0.8,line_image,1,1)
# cv2.imshow('result',canny_image)          #this shows the image in the name of result
# cv2.waitKey(0)                                          #this shows how much second the reult image wants to show

cap=cv2.VideoCapture("test2.mp4")
while(cap.isOpened()):
    _,frame=cap.read()
    canny_image=canny(frame)
    cropped_image=region_of_interest(canny_image)
    lines=cv2.HoughLinesP(cropped_image,2, np.pi/180,100,np.array([]),minLineLength=40,maxLineGap=5)
    averaged_lines=average_slope_intercept(frame,lines)
    line_image=display_lines(frame,averaged_lines)
    combo_image=cv2.addWeighted(frame,0.8,line_image,1,1)
    cv2.imshow('result',combo_image)          #this shows the image in the name of result
    cv2.waitKey(0)                                          #this shows how much second the reult image wants to show

# plt.imshow(canny)                 matplotlib code to see dimensions
# plt.show()