# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 10:32:04 2019

@author: vaibhavK
"""

import cv2
import numpy as np, os
import imageio
import imutils

class DisplayAnime():
    
    def __init__(self, imgDirPath, gifSaveDir):
        self.imgDirPath = imgDirPath 
        self.gifSaveDir = gifSaveDir
        self.labels = {}
    
    def display(self, predictedText):
        final = []
        images = os.listdir(self.imgDirPath)
        for i,img in enumerate(images):
            self.labels[str(img.split('.')[0]).lower()] = self.imgDirPath + img

        blackScrn = np.zeros(shape=(200,200,3),dtype= 'uint8')
        start = cv2.putText(blackScrn.copy(), f'==Start==', (20,100),cv2.FONT_HERSHEY_COMPLEX, .85,(255,255,255), 2)
        ''' Adding starting image'''
        final.append(start)
        final.append(start)
        for char in predictedText.lower():
            print(char)
            if char == ' ':
                char = 'space'
            image = cv2.imread(self.labels[char])
            #image = imutils.auto_canny(image.copy(), sigma=0.25)
            #image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            image = cv2.putText(image, f'{char}', (10,40),cv2.FONT_HERSHEY_COMPLEX, .85,(0,0,255), 2)
            final.append(cv2.cvtColor(image,cv2.COLOR_BGR2RGB))
        '''Adding End image ''' 
        end = cv2.putText(blackScrn.copy(), f'End', (20,100),cv2.FONT_HERSHEY_COMPLEX, .85,(255,255,255), 2)
        final.append(end)

        ''' Convert the image into GIF and Save'''
        try:
            imageio.mimsave( self.gifSaveDir + 'output.gif', final, duration = 0.65, loop=0)
            return True
        except Exception as e:
            print(e)
            return False
        
 




if __name__ =='__main__':
    
    path = '/'.join(os.path.dirname(os.path.abspath('__file__')).split('\\')[:-1])
    obj = DisplayAnime(imgDirPath= path + '/Data/', gifSaveDir= path + '/static/output/')
    obj.display('I am Vaibhav')
    
    
    
    
    
    
    
    
    
    
    
    
# =============================================================================
#     
# for i in range(1,10):
#     img = cv2.imread('./Data/'+ str(i)+'.jpg')
#     img = cv2.resize(img,(200,200),cv2.INTER_AREA)
#     cv2.imwrite('./Data/'+ str(i)+'.jpg',img)
# =============================================================================
# =============================================================================
# dataPath = 'D:/Projects/Duff_and_Dumb/Data/'
# 
# dct = {}
# 
# images = os.listdir(dataPath)
# 
# for i,img in enumerate(images):
#     dct[str(img.split('.')[0]).lower()] = dataPath + img
#     
# 
# blackScrn = np.zeros(shape=(200,200,3),dtype= 'uint8')
# start = cv2.putText(blackScrn.copy(), f'START', (80,100),cv2.FONT_HERSHEY_COMPLEX, .85,(255,255,255), 1)
#     
# #create a movie
# word = 'Flight got delayed'
# cntForEachChar = 25
# final = []
# final.append(start)
# for char in word.lower():
#     print(char)
#     if char == ' ':
#         char = 'space'
#     image = cv2.imread(dct[char])
#     #temp = image.copy()
#     image = cv2.putText(image, f'{char}', (10,50),cv2.FONT_HERSHEY_COMPLEX, .85,(0,0,255), 1)
#     
#     #image = [image] * (cntForEachChar)
#     final.append(image)
#     #final.append(blackScrn)
#     #img.extend([temp])
#     #image[0] = cv2.putText(image[0], f'{char}', (10,50),cv2.FONT_HERSHEY_COMPLEX, .65,(0,255,0), 1)
#     #final.extend([image])
# 
# end = cv2.putText(blackScrn.copy(), f'End', (800,100),cv2.FONT_HERSHEY_COMPLEX, .85,(255,255,255), 1)
# final.append(end)
#     
# x = []
# for item in final:
#     x = x + item    
# #x = final[0]+final[1]    
# 
# 
# for i in range(len(x)):
#     cv2.imshow('img',x[i])
#     cv2.waitKey(100)
# cv2.destroyAllWindows()
# 
# 
# 
# 
# 
# 
# x = [list(item) for item in x]
# 
# final[0].save('output.gif', format='GIF', 
#       append_images=final[1:], save_all=True, duration=100, loop=0)
# 
# 
# with imageio.get_writer('movie.gif', mode='i') as writer:
#     for item in final:
#         writer.append_data(item)
# writer.close()
# 
# imageio.mimsave('surface.gif', final, fps = 2)
# 
# =============================================================================
