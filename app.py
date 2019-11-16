import speech_recognition as sr
import numpy as np, os, time
from flask import Flask, render_template, redirect,request, flash, redirect, url_for
from collections import deque
from helper_scripts.forms import Submit, TestMic, SelectMicrophoneDevice, StopRecording, CheckConfiguredDevice
from helper_scripts.function import AudioToText
from helper_scripts.DisplayAnimator import DisplayAnime

"""class RecordingQueue():
    def __init__(self):
        self.flagQueue = deque(maxlen=1)
    def updateQueue(self):
        self.flagQueue.append(1)"""
        


app = Flask(__name__)

app.config['SECRET_KEY'] = '840abcfc2aad4166f009b1c7d2d6e572'
#app.config['SECRET_KEY'] = '030d2f24454f5deb339128ae708c767e'
queue = deque(maxlen=64)

app.config["deviceId"] = ''

""" Below functions will ensure no cache utilization """
@app.after_request
def add_header(response):
    response.cache_control.no_store = True
    return response



if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate, public, max-age=0"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

@app.route('/', methods=['GET','POST'])
@app.route('/home', methods=['GET','POST'])
def home():
    form = Submit()
    #testMic = TestMic()
    audio = AudioToText(baseDirPath=app.root_path, sampleRate=48000, chunkSize=2048)
    testMicDevice = SelectMicrophoneDevice()
    display = DisplayAnime(imgDirPath= app.root_path + '/Data/', gifSaveDir = app.root_path + '/static/output/')
    #stopRecording = StopRecording()
    #checkConfiguredDevice = CheckConfiguredDevice()
    predictedText = '--' 


    posts = [
            {
            'author':'Version 1: Displays the static sign images for each English letter. ',
            'title' : 'Sign Language Animator (Version : 1)',
            'content': 'Converts the speech into sign language and displays an Animation video'
            }
    ]

    if request.method == 'GET': 
        return render_template("home.html",form = form, predictedText=predictedText,  posts=posts, micLists={},testMicrophone=testMicDevice)

    else:
        if request.form['submit'] == 'Test Mic':
            MicTestingFlag=True
            micList = AudioToText.test_and_select_microphone()
            '''if testMicDevice.validate_on_submit():
                flash('Device Saved', 'success')
                return render_template("home.html", form = form, posts=posts, micLists=micList, MicTestingFlag=MicTestingFlag, testMicrophone=testMicDevice)
            else:
                flash('Wrong Data Entered', 'danger')
                return redirect(url_for('home'))'''
            return render_template("home.html", predictedText=predictedText, form = form, posts=posts, micLists=micList, MicTestingFlag=MicTestingFlag, testMicrophone=testMicDevice)

        elif request.form['submit'] == 'Save':
            """ Save Device button is clicked """
            #print(type(testMicDevice.data["deviceId"]))
            #print(len(str(testMicDevice.data["deviceId"])))
            if type(testMicDevice.data["deviceId"]) == int and len(str(testMicDevice.data["deviceId"])) >= 1:
                flash(f'Device Configured : {testMicDevice.data["deviceId"]}','success')
                app.config['deviceId'] = testMicDevice.data["deviceId"]
                print(f'app.config["deviceId"] ::::==== {app.config["deviceId"]}')
                return redirect(url_for('home'))

            else:
                flash('Wrong device ID entered','danger')
                return redirect(url_for('home'))

        elif request.form['submit'] == 'Record':
            try:
                os.remove(app.root_path + url_for('static',filename='uploads/prediction.txt'))
            except FileNotFoundError:
                print('error')
            startRecodingFlag = True 
            print(f'device id :::: >>>{app.config["deviceId"]}')
            if len(str(app.config["deviceId"])) < 1: #app.config["deviceId"] :#
                flash(f'No Microphone device is configured. Please Run Mic test', 'danger')
                return redirect(url_for('home'))
            else:
                audio.start(device_id=int(app.config["deviceId"]))
                return render_template("home.html", form = form, posts=posts, predictedText=predictedText,
                                        micLists={},testMicrophone=testMicDevice, startRecodingFlag=startRecodingFlag)
                #text = audio.getText(deviceId=int(app.config["deviceId"]))

        elif request.form['submit'] == 'Stop':
            startRecodingFlag = False
            #audio.stop()
            while not os.path.exists(app.root_path + url_for('static',filename='uploads/prediction.txt')):
                time.sleep(3)
            #predictedText = audio.predQueue
            with open( app.root_path + url_for('static',filename='uploads/prediction.txt'), 'r') as f:
                predictedText = f.read()
            print(f'The predicted Text :::: >> {predictedText}')

            retFlag = display.display(predictedText)
            print(f'retFlag====>>>>{retFlag}')
            while not os.path.exists(app.root_path + url_for('static',filename='output/output.gif')):
                time.sleep(2)
            return render_template("home.html", form = form, predictedText=predictedText, posts=posts, retFlag=retFlag,
                                        micLists={},testMicrophone=testMicDevice, startRecodingFlag=startRecodingFlag, audio=audio)

        elif request.form['submit'] == 'Check Configured Device':
            #startRecodingFlag = False
            if len(str(app.config["deviceId"]))>=1:
                flash(f'Active microphone is {app.config["deviceId"]}','success')
                
            else:
                flash(f'No device configured. Please run mic-test and configure the microphone.', 'danger')    
            return redirect(url_for('home'))

        #elif request.form['submit'] == 'Record':
            

                #text = audio.getText(deviceId=int(app.config["deviceId"]))
                #flash(f'predicted text : {text}','success')



    return render_template('home.html')


@app.route('/about',methods=['GET','POST'] )
def about():
    form = Submit()
    if request.method == 'POST':
        return redirect(url_for('home'))
    return render_template('about.html', form=form)





if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD']=True
    app.run(host = '127.0.0.1', port = 8080, debug=True, use_reloader=True)


