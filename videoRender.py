# importing the module 
import cv2
import os
import sys
import numpy as np
  
# reading the video 
os.system('rm test.mp4')
os.system('yt-dlp -o "test.mp4" -f "[ext=mp4]" --merge-output-format mp4 %s' % sys.argv[1])

source = cv2.VideoCapture('test.mp4') 
  
# running the loop 
while True: 
  
    # extracting the frames 
    ret, img = source.read() 
    
    # noiseless_image_colored = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21) 
    
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # grayimg = cv2.fastNlMeansDenoising(grayimg, None, 20, 7, 21) 

    contrast = 1

    grayimg = cv2.addWeighted(grayimg, contrast, np.zeros(grayimg.shape, grayimg.dtype), 0, 0) 

    grayimg = cv2.medianBlur(grayimg, 11)

    #Get the edges 
    edges = cv2.adaptiveThreshold(grayimg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 5, 5)

    #Convert to a cartoon version
    color = cv2.bilateralFilter(img, 9, 250, 250)
    cartoon = cv2.bitwise_and(color, color, mask=edges)

    cartoon_gray = cv2.cvtColor(cartoon, cv2.COLOR_BGR2GRAY)

    # se=cv2.getStructuringElement(cv2.MORPH_RECT , (8,8))
    # bg=cv2.morphologyEx(cartoon_gray, cv2.MORPH_DILATE, se)
    # out_gray=cv2.divide(cartoon_gray, bg, scale=255)
    out_binary=cv2.threshold(cartoon_gray, 0, 255, cv2.THRESH_OTSU )[1] 

    edges = cv2.Canny(img,100,200)
    edges = cv2.dilate(edges, None, iterations=1)

    small = cv2.resize(edges, (320, 190), 
               interpolation = cv2.INTER_AREA)
    
    small[small > 150] = 255
    small[small < 151] = 0
    
    # [0,0] = (12, 318, -629)
    # [1,0] = (12, 316, -629)
    # [0,1] = (12, 318, -627)
    # execute as @a at @s run fill x y z x y z minecraft:target/minecraft:light_gray_wool

    f = open("videoPlayer/data/player/functions/set_first_frame.mcfunction", "w")

    for i in range(190):
        for j in range(320):
            if small[i, j] == 255:
                f.write("execute as @a at @s run fill %d %d %d %d %d %d minecraft:target\n" % (12, 318-(2*i), -629+(2*j), 12, 318-(2*i), -629+(2*j)))
      
    # displaying the video 
    cv2.imshow("Live", small)
    f.close()
    break
  
    # exiting the loop 
    key = cv2.waitKey(1) 
    if key == ord("q"): 
        break
      
# closing the window 
cv2.destroyAllWindows() 
source.release()