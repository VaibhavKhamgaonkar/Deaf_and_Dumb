# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 21:14:51 2019

@author: VabhavK
"""
import speech_recognition as sr
import os,time,numpy as np
from collections import deque
#from app import RecordingQueue
from threading import Thread


class AudioToText():
    ''' Class to get the text output for the spoken audio  '''
    
    def __init__(self, baseDirPath, sampleRate=48000, chunkSize=2048 ):
        self.sampleRate = sampleRate
        self.chunkSize = chunkSize
        self.recognize = sr.Recognizer()
        self.baseDir = baseDirPath + '/' #'/'.join(os.path.dirname(os.path.abspath('__file__')).split('\\')[:-1]) +'/'
        #self.predQueue = []
        #super().__init__(self)
        
    def start(self, device_id=1):
        """ Device id has to be passed as an argument """
        self.stopped= False
        t = Thread(target=self.getText, name='Audio2Text', args=(device_id,))
        t.daemon = True
        t.start()
        return self
    
    def stop(self):
        self.stopped = True
        #return self.predQueue
        
    #def update(self)
    
    @staticmethod
    def test_and_select_microphone():
        micList = {}#sr.Microphone.list_microphone_names()
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            #("Microphone with name \"{1}\" found for `Microphone(device_index={0})`".format(index, name))
            micList[name] = index
        return micList
        
    
    def getText(self,deviceId):
        ''' Function to get the Text output froman Audio
        it requires device id. Device id is the number of microphone connected to the system. 
        To get the correct microphone number, user have to run the above method "test_and_select_microphone()"
                
        '''
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                print('Stopping the Process..!')
                return
        
            with sr.Microphone(device_index=deviceId,sample_rate=self.sampleRate,chunk_size=self.chunkSize) as source:
                self.recognize.adjust_for_ambient_noise(source,duration=0.5)
                
                print('Say Something')
                audio = self.recognize.listen(source=source, phrase_time_limit=None)
                
                try:
                    text = self.recognize.recognize_google(audio)
                    print('You said :', text)
                except sr.UnknownValueError:
                    print("Google Speech Recognition could not understand audio")
                    text = "Speech Recognition system could not understand audio"
                except sr.RequestError as e: 
                    print("Could not request results from Google Speech Recognition service; {0}".format(e)) 
                    text = 'proxy error!!!'
            #self.predQueue.append(text)
            #print(self.predQueue)
            #print(len(self.predQueue))
            print(text)
            with open(self.baseDir +'static/uploads/prediction.txt','w') as f:
                f.write(text)
            self.stopped = True
            #return self.predQueue
    
    
    
    
if __name__ =='__main__'    :
    obj = AudioToText()
    obj.start()
    obj.stop()
    #x = obj.predQueue
    #obj.getText(deviceId=1)
    
    
    
    
# =============================================================================
# q = deque(maxlen = 8)
# q.append(1)
# q.append(10)
# q.append(11)
# q.append(12)
# q.append(13)
# q.append(14)   
# 
# for i in range(len(q)):
#     print(q.popleft())
#     len(q)
#     
# =============================================================================

# =============================================================================
# 
# sr.Microphone.list_microphone_names()
# 
# AudioToText.test_and_select_microphone()
# 
# a = AudioToText()
# 
# a.test_and_select_microphone()
# 
# =============================================================================
