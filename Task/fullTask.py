from __future__ import absolute_import, division
from psychopy import locale_setup, sound, gui, visual, core, data, event, logging, parallel
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions
import sys  # to get file system encoding
import socket

# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
os.chdir(_thisDir)

import instructions as inst

TCP_IP = '169.254.199.252'
TCP_PORT = 6700

parportAddress = 0x0378

restingStateLength = 120 # Length of resting state segments in seconds

Ncorr4prac = 3

motorReps = 2
schubotzReps = 15
linguisticReps = 1

slowDown = 2
off = int("00000000",2)
RSEO = int("00010100",2)
RSEC = int("00010101",2)

train1trig = int("00001000",2)
train2trig = int("00001001",2)
test1trig = int("00001010",2)
test2trig = int("00001011",2)
test3trig = int("00001100",2)
test4trig = int("00001101",2)

respKeyList = ['num_4', 'num_6']

connectDlg = gui.Dlg(title='Remonte control')
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    connectDlg.addText('Connection successfully established')
    RecConn = True
except:
    connectDlg.addText('Unable to establish connection')
    RecConn = False
connectDlg.show()
if connectDlg.OK == False:
    core.quit()  # user pressed cancel

if RecConn:
    s.send("1"+"C:\\Vision\\Workfiles\\2018_Standard_30Cap.rwksp")
    s.send("4")
    impDlg = gui.Dlg('Impedances')
    impDlg.addText('Press Okay when ready to check Impedences')
    impDlg.show()
    if impDlg.OK == False:
        core.quit()  # user pressed cancel
    s.send("I")
    setupDlg = gui.Dlg('Setup')
    setupDlg.addText('Press Okay when Impedences at suitable level')
    setupDlg.show()
    if setupDlg.OK == False:
        core.quit()  # user pressed cancel
    s.send("M")

# Be sure to add code for parallel port control!
port = parallel.ParallelPort(address=parportAddress) # parallel port setup
port.setData( off )# set all pins on port low

# Store info about the experiment session
expName = 'WFNeuroTasks'  # from the Builder filename that created this script
expInfo = {'participant':''}#, 'session':'001'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Function for dispalying penguin detective and specific speech bubbles
def displayPenguin(speechText):

    textBox.setText(speechText)

    endExpNow = False
    t = 0
    penguinClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_3 = event.BuilderKeyResponse()
    # keep track of which components have finished
    penComponents = [detectiveImage, key_resp_3, speechImage, textBox]

    for thisComponent in penComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine -------
    while continueRoutine:
        # get current time
        t = penguinClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        textBox.draw()
        # *textImage* updates
        if t >= 0.0 and speechImage.status == NOT_STARTED:
            # keep track of start time/frame for later
            speechImage.tStart = t
            speechImage.frameNStart = frameN  # exact frame index
            speechImage.setAutoDraw(True)

        if t >= 0.0 and detectiveImage.status == NOT_STARTED:
            # keep track of start time/frame for later
            detectiveImage.tStart = t
            detectiveImage.frameNStart = frameN  # exact frame index
            detectiveImage.setAutoDraw(True)

        # *textBox* updates
        if t >= 0.0 and textBox.status == NOT_STARTED:
            # keep track of start time/frame for later
            textBox.tStart = t
            textBox.frameNStart = frameN  # exact frame index
            textBox.setAutoDraw(True)

        # *key_resp_3* updates
        if t >= 0.0 and key_resp_3.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_3.tStart = t
            key_resp_3.frameNStart = frameN  # exact frame index
            key_resp_3.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if key_resp_3.status == STARTED:
            theseKeys = event.getKeys(keyList=['return'])

            # check for quit:
            if "escape" in theseKeys:
                endExpNow = True
            if len(theseKeys) > 0:  # at least one key was pressed
                continueRoutine = False

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in penComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine -------
    for thisComponent in penComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    # the Routine was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

# Function for sending triggers to EEG file
def sendTrigger(trigger):
    port.setData( trigger )
    core.wait(0.01)
    port.setData( off )

# Function for resting state
def restingState(speechText, RStrigger, RSlength = 120):

    if RecConn:
        s.send("S")

    displayPenguin(speechText[0])

    sendTrigger(RStrigger)
    
    textBox.setText(speechText[1])

    endExpNow = False
    t = 0
    penguinClock.reset()  # clock
    routineTimer.add(RSlength)
    frameN = -1
    continueRoutine = True
    # update component parameters for each repeat
    key_resp_3 = event.BuilderKeyResponse()
    # keep track of which components have finished
    penComponents = [detectiveImage, key_resp_3, speechImage, textBox]

    for thisComponent in penComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine -------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = penguinClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # *textImage* updates
        if t >= 0.0 and speechImage.status == NOT_STARTED:
            # keep track of start time/frame for later
            speechImage.tStart = t
            speechImage.frameNStart = frameN  # exact frame index
            speechImage.setAutoDraw(True)

        if t >= 0.0 and detectiveImage.status == NOT_STARTED:
            # keep track of start time/frame for later
            detectiveImage.tStart = t
            detectiveImage.frameNStart = frameN  # exact frame index
            detectiveImage.setAutoDraw(True)

        # *textBox* updates
        if t >= 0.0 and textBox.status == NOT_STARTED:
            # keep track of start time/frame for later
            textBox.tStart = t
            textBox.frameNStart = frameN  # exact frame index
            textBox.setAutoDraw(True)

        # *key_resp_3* updates
        if t >= 0.0 and key_resp_3.status == NOT_STARTED:
            # keep track of start time/frame for later
            key_resp_3.tStart = t
            key_resp_3.frameNStart = frameN  # exact frame index
            key_resp_3.status = STARTED
            # keyboard checking is just starting
            win.callOnFlip(key_resp_3.clock.reset)  # t=0 on next screen flip
            event.clearEvents(eventType='keyboard')
        if key_resp_3.status == STARTED:
            theseKeys = event.getKeys(keyList=['q','escape'])

            # check for quit:
            if "escape" in theseKeys:
                continueRoutine = False
                endExpNow = True
            elif "q" in theseKeys:
                continueRoutine = False

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in penComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if endExpNow or event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine -------
    for thisComponent in penComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

    if RecConn:
        s.send("P")

    # the Routine was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()

# Function for feedback
def feedbackRoutine(feedbackText, corr):

    # ------Prepare to start Routine "feedback"-------
    t = 0
    feedbackClock.reset()  # clock
    frameN = -1
    continueRoutine = True
    routineTimer.add(5.000000)
    textBox.setText(feedbackText)
    # update component parameters for each repeat
    # keep track of which components have finished
    feedbackComponents = [speechImage, star1, detectiveImage,textBox]
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED

    # -------Start Routine "feedback"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = feedbackClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame

        # *text* updates
        if t >= 0.0 and speechImage.status == NOT_STARTED:
            # keep track of start time/frame for later
            speechImage.tStart = t
            speechImage.frameNStart = frameN  # exact frame index
            speechImage.setAutoDraw(True)

        if t >= 0.0 and detectiveImage.status == NOT_STARTED:
            # keep track of start time/frame for later
            detectiveImage.tStart = t
            detectiveImage.frameNStart = frameN  # exact frame index
            detectiveImage.setAutoDraw(True)

        if t >= 0.0 and textBox.status == NOT_STARTED:
            # keep track of start time/frame for later
            textBox.tStart = t
            textBox.frameNStart = frameN  # exact frame index
            textBox.setAutoDraw(True)

        star1.setSize([0.005*(frameN%60),0.005*(frameN%60)])
        star1.setOri((frameN%360)*1)
        if frameN%60 == 0:
            left = random() < 0.5
            top = random() > 0.5

            xpos = float(randint(30, 70))/100
            ypos = float(randint(25, 60))/100

            if left:
                xpos = xpos * -1
            if top:
                ypos = ypos * -1
            pos = [xpos, ypos]
        star1.setPos(pos)

        if t >= 0.0 and star1.status == NOT_STARTED and corr == 1:
            star1.tStart = t
            star1.frameNStart = frameN
            star1.setAutoDraw(True)

        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in feedbackComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished

        # check for quit (the Esc key)
        if event.getKeys(keyList=["escape"]):
            core.quit()

        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()

    # -------Ending Routine "feedback"-------
    for thisComponent in feedbackComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)

# General function for Schubotz tasks
def schubotzRoutine(exptType, trialList, trigger):
    
    endExpNow = False

    filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], exptType, expInfo['date'])

    thisExp = data.ExperimentHandler(name=exptType, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath=None,
        savePickle=True, saveWideText=True,
        dataFileName=filename)

    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    displayPenguin(inst.taskExplan[exptType][0]) # Explanantion

    Fixation.setText('+')

    trials_Demo = data.TrialHandler(nReps=1, method='sequential',
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(trialList),
        seed=None, name='trials_Demo')
    thisTrials_Demo = trials_Demo.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrials_Prac.rgb)
    if thisTrials_Demo != None:
        for paramName in thisTrials_Demo.keys():
            exec(paramName + '= thisTrials_Demo.' + paramName)

    for thisTrials_Demo in trials_Demo:
        currentLoop = trials_Demo
        # abbreviate parameter names if possible (e.g. rgb = thisTrials_Prac.rgb)
        if thisTrials_Demo != None:
            for paramName in thisTrials_Demo.keys():
                exec(paramName + '= thisTrials_Demo.' + paramName)

        # set up handler to look after randomisation of conditions etc
        repeatingStims_Prac = data.TrialHandler(nReps=6, method='sequential',
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='repeatingStims_Prac')
        thisRepeatingStims_Prac = repeatingStims_Prac.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
        if thisRepeatingStims_Prac != None:
            for paramName in thisRepeatingStims_Prac.keys():
                exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

        for thisRepeatingStims_Prac in repeatingStims_Prac:
            currentLoop = repeatingStims_Prac

            # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
            if thisRepeatingStims_Prac != None:
                for paramName in thisRepeatingStims_Prac.keys():
                    exec(paramName + '= thisRepeatingStims_Prac.' + paramName)


            # ------Prepare to start Routine "stimTrial"-------
            t = 0
            stimTrialClock.reset()  # clock
            frameN = -1
            continueRoutine = True

            # update component parameters for each repeat
            if currentLoop.nRemaining == 1:
                s1_o1.setPos(test1pos1)
                s1_o1.setImage(test1obj1)
                s1_o2.setPos(test1pos2)
                s1_o2.setImage(test1obj2)
                s2_o1.setPos(test2pos1)
                s2_o1.setImage(test2obj1)
                s2_o2.setPos(test2pos2)
                s2_o2.setImage(test2obj2)
                stim1time = test1time
                stim2time = test2time
                stim1trig = test1trig
                stim2trig = test2trig
            elif currentLoop.nRemaining == 0:
                s1_o1.setPos(test3pos1)
                s1_o1.setImage(test3obj1)
                s1_o2.setPos(test3pos2)
                s1_o2.setImage(test3obj2)
                s2_o1.setPos(test4pos1)
                s2_o1.setImage(test4obj1)
                s2_o2.setPos(test4pos2)
                s2_o2.setImage(test4obj2)
                stim1time = test3time
                stim2time = test4time
                stim1trig = test3trig
                stim2trig = test4trig
            else:
                s1_o1.setPos(train1pos1)
                s1_o1.setImage(train1obj1)
                s1_o2.setPos(train1pos2)
                s1_o2.setImage(train1obj2)
                s2_o1.setPos(train2pos1)
                s2_o1.setImage(train2obj1)
                s2_o2.setPos(train2pos2)
                s2_o2.setImage(train2obj2)
                stim1time = train1time
                stim2time = train2time
                stim1trig = train1trig
                stim2trig = train2trig

            # keep track of which components have finished
            stimTrialComponents = [s1_o1, s1_o2, s2_o1, s2_o2, Fixation]
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "stimTrial"-------
            while continueRoutine:
                # get current time
                t = stimTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *s1_o1* updates
                if t >= 0.0 and s1_o1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    s1_o1.tStart = t
                    s1_o1.frameNStart = frameN  # exact frame index
                    s1_o1.setAutoDraw(True)
                frameRemains = 0.0 + stim1time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if s1_o1.status == STARTED and t >= frameRemains:
                    s1_o1.setAutoDraw(False)

                # *s1_o2* updates
                if t >= 0.0 and s1_o2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    s1_o2.tStart = t
                    s1_o2.frameNStart = frameN  # exact frame index
                    s1_o2.setAutoDraw(True)
                frameRemains = 0.0 + stim1time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if s1_o2.status == STARTED and t >= frameRemains:
                    s1_o2.setAutoDraw(False)

                # *s2_o1* updates
                if t >= stim1time and s2_o1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    s2_o1.tStart = t
                    s2_o1.frameNStart = frameN  # exact frame index
                    s2_o1.setAutoDraw(True)
                frameRemains = stim1time + stim2time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if s2_o1.status == STARTED and t >= frameRemains:
                    s2_o1.setAutoDraw(False)

                # *s2_o2* updates
                if t >= stim1time and s2_o2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    s2_o2.tStart = t
                    s2_o2.frameNStart = frameN  # exact frame index
                    s2_o2.setAutoDraw(True)
                frameRemains = stim1time + stim2time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if s2_o2.status == STARTED and t >= frameRemains:
                    s2_o2.setAutoDraw(False)

                # *Fixation* updates
                if t >= 0.0 and Fixation.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Fixation.tStart = t
                    Fixation.frameNStart = frameN  # exact frame index
                    Fixation.setAutoDraw(True)
                frameRemains = 0.0 + (stim1time+stim2time)- win.monitorFramePeriod * 0.75  # most of one frame period left
                if Fixation.status == STARTED and t >= frameRemains:
                    Fixation.setAutoDraw(False)

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "stimTrial"-------
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            #thisExp.nextEntry()

        # completed 5 repeats of 'repeatingStims_Prac'

        if trials_Demo.thisN == 0:
            displayPenguin(inst.taskExplan[exptType][1])
        elif trials_Demo.thisN == 1:
            displayPenguin(inst.brokenSeq)
            break

    for i in inst.gameRules:
        displayPenguin(i)

    displayPenguin(inst.ontoPractice)

    count = 0

    # set up handler to look after randomisation of conditions etc
    trials_Prac = data.TrialHandler(nReps=1, method='random',
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(trialList),
        seed=None, name='trials_Prac')
    thisTrials_Prac = trials_Prac.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrials_Prac.rgb)
    if thisTrials_Prac != None:
        for paramName in thisTrials_Prac.keys():
            exec(paramName + '= thisTrials_Prac.' + paramName)

    for thisTrials_Prac in trials_Prac:
        currentLoop = trials_Prac
        # abbreviate parameter names if possible (e.g. rgb = thisTrials_Prac.rgb)
        if thisTrials_Prac != None:
            for paramName in thisTrials_Prac.keys():
                exec(paramName + '= thisTrials_Prac.' + paramName)

        # set up handler to look after randomisation of conditions etc
        repeatingStims_Prac = data.TrialHandler(nReps=6, method='sequential',
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='repeatingStims_Prac')
#        thisExp.addLoop(repeatingStims_Prac)  # add the loop to the experiment
        thisRepeatingStims_Prac = repeatingStims_Prac.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
        if thisRepeatingStims_Prac != None:
            for paramName in thisRepeatingStims_Prac.keys():
                exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

        for thisRepeatingStims_Prac in repeatingStims_Prac:
            currentLoop = repeatingStims_Prac

            # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
            if thisRepeatingStims_Prac != None:
                for paramName in thisRepeatingStims_Prac.keys():
                    exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

            # ------Prepare to start Routine "stimTrial"-------
            t = 0
            stimTrialClock.reset()  # clock
            frameN = -1
            continueRoutine = True

            # update component parameters for each repeat
            if currentLoop.nRemaining == 1:
                s1_o1.setPos(test1pos1)
                s1_o1.setImage(test1obj1)
                s1_o2.setPos(test1pos2)
                s1_o2.setImage(test1obj2)
                s2_o1.setPos(test2pos1)
                s2_o1.setImage(test2obj1)
                s2_o2.setPos(test2pos2)
                s2_o2.setImage(test2obj2)
                stim1time = test1time
                stim2time = test2time
                stim1trig = test1trig
                stim2trig = test2trig
            elif currentLoop.nRemaining == 0:
                s1_o1.setPos(test3pos1)
                s1_o1.setImage(test3obj1)
                s1_o2.setPos(test3pos2)
                s1_o2.setImage(test3obj2)
                s2_o1.setPos(test4pos1)
                s2_o1.setImage(test4obj1)
                s2_o2.setPos(test4pos2)
                s2_o2.setImage(test4obj2)
                stim1time = test3time
                stim2time = test4time
                stim1trig = test3trig
                stim2trig = test4trig
            else:
                s1_o1.setPos(train1pos1)
                s1_o1.setImage(train1obj1)
                s1_o2.setPos(train1pos2)
                s1_o2.setImage(train1obj2)
                s2_o1.setPos(train2pos1)
                s2_o1.setImage(train2obj1)
                s2_o2.setPos(train2pos2)
                s2_o2.setImage(train2obj2)
                stim1time = train1time
                stim2time = train2time
                stim1trig = train1trig
                stim2trig = train2trig
                
            # keep track of which components have finished
            stimTrialComponents = [s1_o1, s1_o2, s2_o1, s2_o2, Fixation]
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "stimTrial"-------
            while continueRoutine:
                # get current time
                t = stimTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *s1_o1* updates
                if t >= 0.0 and s1_o1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    s1_o1.tStart = t
                    s1_o1.frameNStart = frameN  # exact frame index
                    s1_o1.setAutoDraw(True)
                frameRemains = 0.0 + stim1time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if s1_o1.status == STARTED and t >= frameRemains:
                    s1_o1.setAutoDraw(False)

                # *s1_o2* updates
                if t >= 0.0 and s1_o2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    s1_o2.tStart = t
                    s1_o2.frameNStart = frameN  # exact frame index
                    s1_o2.setAutoDraw(True)
                frameRemains = 0.0 + stim1time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if s1_o2.status == STARTED and t >= frameRemains:
                    s1_o2.setAutoDraw(False)

                # *s2_o1* updates
                if t >= stim1time and s2_o1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    s2_o1.tStart = t
                    s2_o1.frameNStart = frameN  # exact frame index
                    s2_o1.setAutoDraw(True)
                frameRemains = stim1time + stim2time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if s2_o1.status == STARTED and t >= frameRemains:
                    s2_o1.setAutoDraw(False)

                # *s2_o2* updates
                if t >= stim1time and s2_o2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    s2_o2.tStart = t
                    s2_o2.frameNStart = frameN  # exact frame index
                    s2_o2.setAutoDraw(True)
                frameRemains = stim1time + stim2time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if s2_o2.status == STARTED and t >= frameRemains:
                    s2_o2.setAutoDraw(False)

                # *Fixation* updates
                if t >= 0.0 and Fixation.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Fixation.tStart = t
                    Fixation.frameNStart = frameN  # exact frame index
                    Fixation.setAutoDraw(True)
                frameRemains = 0.0 + (stim1time+stim2time)- win.monitorFramePeriod * 0.75  # most of one frame period left
                if Fixation.status == STARTED and t >= frameRemains:
                    Fixation.setAutoDraw(False)

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "stimTrial"-------
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
#            thisExp.nextEntry()

        # completed 6 repeats of 'repeatingStims_Prac'

        # ------Prepare to start Routine "response"-------
        t = 0
        responseClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        key_resp_2 = event.BuilderKeyResponse()
        # keep track of which components have finished
        textBox.setText(inst.responsePrompt)
        responseComponents = [speechImage, detectiveImage, key_resp_2, textBox]
        for thisComponent in responseComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        # -------Start Routine "response"-------
        while continueRoutine:
            # get current time
            t = responseClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *responseText* updates
            if t >= 0.0 and speechImage.status == NOT_STARTED:
                # keep track of start time/frame for later
                speechImage.tStart = t
                speechImage.frameNStart = frameN  # exact frame index
                speechImage.setAutoDraw(True)

            if t >= 0.0 and detectiveImage.status == NOT_STARTED:
                # keep track of start time/frame for later
                detectiveImage.tStart = t
                detectiveImage.frameNStart = frameN  # exact frame index
                detectiveImage.setAutoDraw(True)

            if t >= 0.0 and textBox.status == NOT_STARTED:
                # keep track of start time/frame for later
                textBox.tStart = t
                textBox.frameNStart = frameN  # exact frame index
                textBox.setAutoDraw(True)

            # *key_resp_2* updates
            if t >= 0.0 and key_resp_2.status == NOT_STARTED:
                # keep track of start time/frame for later
                key_resp_2.tStart = t
                key_resp_2.frameNStart = frameN  # exact frame index
                key_resp_2.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if key_resp_2.status == STARTED:
                theseKeys = event.getKeys(keyList=respKeyList)

                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                    key_resp_2.rt = key_resp_2.clock.getTime()
                    # was this 'correct'?
                    if (key_resp_2.keys == str(seqBroken)) or (key_resp_2.keys == seqBroken):
                        key_resp_2.corr = 1
                    else:
                        key_resp_2.corr = 0
                    # a response ends the routine
                    continueRoutine = False

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in responseComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "response"-------
        for thisComponent in responseComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys=None
            # was no response the correct answer?!
            if str(seqBroken).lower() == 'none':
               key_resp_2.corr = 1  # correct non-response
            else:
               key_resp_2.corr = 0  # failed to respond (incorrectly)
        # store data for trials_Prac (TrialHandler)
        trials_Prac.addData('key_resp_2.keys',key_resp_2.keys)
        trials_Prac.addData('key_resp_2.corr', key_resp_2.corr)
        if key_resp_2.keys != None:  # we had a response
            trials_Prac.addData('key_resp_2.rt', key_resp_2.rt)
        # the Routine "response" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()

        if key_resp_2.corr == 1:
            feedbackRoutine(inst.posFB,1)
            count += 1
        else:
            feedbackRoutine(inst.negFB,0)

        # Repeat trials at a slower speed if incorrect response given
        if key_resp_2.corr == 0:

            # set up handler to look after randomisation of conditions etc
            repeatingStims_Prac = data.TrialHandler(nReps=6, method='sequential',
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='repeatingStims_Prac')
            #thisExp.addLoop(repeatingStims_Prac)  # add the loop to the experiment
            thisRepeatingStims_Prac = repeatingStims_Prac.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
            if thisRepeatingStims_Prac != None:
                for paramName in thisRepeatingStims_Prac.keys():
                    exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

            for thisRepeatingStims_Prac in repeatingStims_Prac:
                currentLoop = repeatingStims_Prac
                # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
                if thisRepeatingStims_Prac != None:
                    for paramName in thisRepeatingStims_Prac.keys():
                        exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

                # ------Prepare to start Routine "stimTrial"-------
                t = 0
                stimTrialClock.reset()  # clock
                frameN = -1
                continueRoutine = True

                # update component parameters for each repeat
                if currentLoop.nRemaining == 1:
                    s1_o1.setPos(test1pos1)
                    s1_o1.setImage(test1obj1)
                    s1_o2.setPos(test1pos2)
                    s1_o2.setImage(test1obj2)
                    s2_o1.setPos(test2pos1)
                    s2_o1.setImage(test2obj1)
                    s2_o2.setPos(test2pos2)
                    s2_o2.setImage(test2obj2)
                    stim1time = test1time * slowDown
                    stim2time = test2time * slowDown
                    stim1trig = test1trig
                    stim2trig = test2trig
                elif currentLoop.nRemaining == 0:
                    s1_o1.setPos(test3pos1)
                    s1_o1.setImage(test3obj1)
                    s1_o2.setPos(test3pos2)
                    s1_o2.setImage(test3obj2)
                    s2_o1.setPos(test4pos1)
                    s2_o1.setImage(test4obj1)
                    s2_o2.setPos(test4pos2)
                    s2_o2.setImage(test4obj2)
                    stim1time = test3time * slowDown
                    stim2time = test4time * slowDown
                    stim1trig = test3trig
                    stim2trig = test4trig
                else:
                    s1_o1.setPos(train1pos1)
                    s1_o1.setImage(train1obj1)
                    s1_o2.setPos(train1pos2)
                    s1_o2.setImage(train1obj2)
                    s2_o1.setPos(train2pos1)
                    s2_o1.setImage(train2obj1)
                    s2_o2.setPos(train2pos2)
                    s2_o2.setImage(train2obj2)
                    stim1time = train1time * slowDown
                    stim2time = train2time * slowDown
                    stim1trig = train1trig
                    stim2trig = train2trig

                # keep track of which components have finished
                stimTrialComponents = [s1_o1, s1_o2, s2_o1, s2_o2, Fixation]
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, 'status'):
                        thisComponent.status = NOT_STARTED# keep track of which components have finished
                    stimTrialComponents = [s1_o1, s1_o2, s2_o1, s2_o2, Fixation]

                # -------Start Routine "stimTrial"-------
                while continueRoutine:
                    # get current time
                    t = stimTrialClock.getTime()
                    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                    # update/draw components on each frame

                    # *s1_o1* updates
                    if t >= 0.0 and s1_o1.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        s1_o1.tStart = t
                        s1_o1.frameNStart = frameN  # exact frame index
                        s1_o1.setAutoDraw(True)
                    frameRemains = 0.0 + stim1time- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if s1_o1.status == STARTED and t >= frameRemains:
                        s1_o1.setAutoDraw(False)

                    # *s1_o2* updates
                    if t >= 0.0 and s1_o2.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        s1_o2.tStart = t
                        s1_o2.frameNStart = frameN  # exact frame index
                        s1_o2.setAutoDraw(True)
                    frameRemains = 0.0 + stim1time- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if s1_o2.status == STARTED and t >= frameRemains:
                        s1_o2.setAutoDraw(False)

                    # *s2_o1* updates
                    if t >= stim1time and s2_o1.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        s2_o1.tStart = t
                        s2_o1.frameNStart = frameN  # exact frame index
                        s2_o1.setAutoDraw(True)
                    frameRemains = stim1time + stim2time- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if s2_o1.status == STARTED and t >= frameRemains:
                        s2_o1.setAutoDraw(False)

                    # *s2_o2* updates
                    if t >= stim1time and s2_o2.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        s2_o2.tStart = t
                        s2_o2.frameNStart = frameN  # exact frame index
                        s2_o2.setAutoDraw(True)
                    frameRemains = stim1time + stim2time- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if s2_o2.status == STARTED and t >= frameRemains:
                        s2_o2.setAutoDraw(False)

                    # *stimFix* updates
                    if t >= 0.0 and Fixation.status == NOT_STARTED:
                        # keep track of start time/frame for later
                        Fixation.tStart = t
                        Fixation.frameNStart = frameN  # exact frame index
                        Fixation.setAutoDraw(True)
                    frameRemains = 0.0 + (stim1time+stim2time)- win.monitorFramePeriod * 0.75  # most of one frame period left
                    if Fixation.status == STARTED and t >= frameRemains:
                        Fixation.setAutoDraw(False)

                    # check if all components have finished
                    if not continueRoutine:  # a component has requested a forced-end of Routine
                        break
                    continueRoutine = False  # will revert to True if at least one component still running
                    for thisComponent in stimTrialComponents:
                        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                            continueRoutine = True
                            break  # at least one component has not yet finished

                    # check for quit (the Esc key)
                    if endExpNow or event.getKeys(keyList=["escape"]):
                        core.quit()

                    # refresh the screen
                    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                        win.flip()

                # -------Ending Routine "stimTrial"-------
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "setAutoDraw"):
                        thisComponent.setAutoDraw(False)
                # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
                routineTimer.reset()

            # completed 6 repeats of 'repeatingStims_Prac'

        # If participants get more than 2 correct then move onto the main experiment
        if count < Ncorr4prac:
            displayPenguin(inst.readyForNext)
        else:
            break

    # completed 5 repeats of 'trials_Prac'

    if RecConn:
        s.send("D")
        s.send("S")

    displayPenguin(inst.ontoTrials)

    sendTrigger(int(trigger))

    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=schubotzReps, method='fullRandom',
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(trialList),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)

    for thisTrial in trials:
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial.keys():
                exec(paramName + '= thisTrial.' + paramName)

        # set up handler to look after randomisation of conditions etc
        repeatingStims = data.TrialHandler(nReps=6, method='sequential',
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='repeatingStims')
        thisExp.addLoop(repeatingStims)  # add the loop to the experiment
        thisRepeatingStim = repeatingStims.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStim.rgb)
        if thisRepeatingStim != None:
            for paramName in thisRepeatingStim.keys():
                exec(paramName + '= thisRepeatingStim.' + paramName)

        for thisRepeatingStim in repeatingStims:
            currentLoop = repeatingStims
            # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStim.rgb)
            if thisRepeatingStim != None:
                for paramName in thisRepeatingStim.keys():
                    exec(paramName + '= thisRepeatingStim.' + paramName)

            t = 0
            stimTrialClock.reset()  # clock
            frameN = -1
            continueRoutine = True

            # update component parameters for each repeat
            if currentLoop.nRemaining == 1:
                s1_o1.setPos(test1pos1)
                s1_o1.setImage(test1obj1)
                s1_o2.setPos(test1pos2)
                s1_o2.setImage(test1obj2)
                s2_o1.setPos(test2pos1)
                s2_o1.setImage(test2obj1)
                s2_o2.setPos(test2pos2)
                s2_o2.setImage(test2obj2)
                stim1time = test1time
                stim2time = test2time
                stim1trig = test1trig
                stim2trig = test2trig
            elif currentLoop.nRemaining == 0:
                s1_o1.setPos(test3pos1)
                s1_o1.setImage(test3obj1)
                s1_o2.setPos(test3pos2)
                s1_o2.setImage(test3obj2)
                s2_o1.setPos(test4pos1)
                s2_o1.setImage(test4obj1)
                s2_o2.setPos(test4pos2)
                s2_o2.setImage(test4obj2)
                stim1time = test3time
                stim2time = test4time
                stim1trig = test3trig
                stim2trig = test4trig
            else:
                s1_o1.setPos(train1pos1)
                s1_o1.setImage(train1obj1)
                s1_o2.setPos(train1pos2)
                s1_o2.setImage(train1obj2)
                s2_o1.setPos(train2pos1)
                s2_o1.setImage(train2obj1)
                s2_o2.setPos(train2pos2)
                s2_o2.setImage(train2obj2)
                stim1time = train1time
                stim2time = train2time
                stim1trig = train1trig
                stim2trig = train2trig
            # keep track of which components have finished
            stimTrialComponents = [s1_o1, s1_o2, s2_o1, s2_o2, Fixation]
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "stimTrial"-------
            while continueRoutine:
                # get current time
                t = stimTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *s1_o1* updates
                if t >= 0.0 and s1_o1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    s1_o1.tStart = t
                    s1_o1.frameNStart = frameN  # exact frame index
                    s1_o1.setAutoDraw(True)
                    sendTrigger(stim1trig)
                frameRemains = 0.0 + stim1time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if s1_o1.status == STARTED and t >= frameRemains:
                    s1_o1.setAutoDraw(False)

                # *s1_o2* updates
                if t >= 0.0 and s1_o2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    s1_o2.tStart = t
                    s1_o2.frameNStart = frameN  # exact frame index
                    s1_o2.setAutoDraw(True)
                frameRemains = 0.0 + stim1time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if s1_o2.status == STARTED and t >= frameRemains:
                    s1_o2.setAutoDraw(False)

                # *s2_o1* updates
                if t >= stim1time and s2_o1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    s2_o1.tStart = t
                    s2_o1.frameNStart = frameN  # exact frame index
                    s2_o1.setAutoDraw(True)
                    sendTrigger(stim2trig)
                frameRemains = stim1time + stim2time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if s2_o1.status == STARTED and t >= frameRemains:
                    s2_o1.setAutoDraw(False)

                # *s2_o2* updates
                if t >= stim1time and s2_o2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    s2_o2.tStart = t
                    s2_o2.frameNStart = frameN  # exact frame index
                    s2_o2.setAutoDraw(True)
                frameRemains = stim1time + stim2time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if s2_o2.status == STARTED and t >= frameRemains:
                    s2_o2.setAutoDraw(False)

                # *Fixation* updates
                if t >= 0.0 and Fixation.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Fixation.tStart = t
                    Fixation.frameNStart = frameN  # exact frame index
                    Fixation.setAutoDraw(True)
                frameRemains = 0.0 + (stim1time+stim2time)- win.monitorFramePeriod * 0.75  # most of one frame period left
                if Fixation.status == STARTED and t >= frameRemains:
                    Fixation.setAutoDraw(False)

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "stimTrial"-------
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()

        # ------Prepare to start Routine "response"-------
        t = 0
        responseClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        key_resp_2 = event.BuilderKeyResponse()
        # keep track of which components have finished
        textBox.setText(inst.responsePrompt)
        responseComponents = [speechImage, textBox, detectiveImage, key_resp_2]
        for thisComponent in responseComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        # -------Start Routine "response"-------
        while continueRoutine:
            # get current time
            t = responseClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            if t >= 0.0 and detectiveImage.status == NOT_STARTED:
                # keep track of start time/frame for later
                detectiveImage.tStart = t
                detectiveImage.frameNStart = frameN  # exact frame index
                detectiveImage.setAutoDraw(True)

            if t >= 0.0 and speechImage.status == NOT_STARTED:
                # keep track of start time/frame for later
                speechImage.tStart = t
                speechImage.frameNStart = frameN  # exact frame index
                speechImage.setAutoDraw(True)
                
            # *responseText* updates
            if t >= 0.0 and textBox.status == NOT_STARTED:
                # keep track of start time/frame for later
                textBox.tStart = t
                textBox.frameNStart = frameN  # exact frame index
                textBox.setAutoDraw(True)

            # *key_resp_2* updates
            if t >= 0.0 and key_resp_2.status == NOT_STARTED:
                # keep track of start time/frame for later
                key_resp_2.tStart = t
                key_resp_2.frameNStart = frameN  # exact frame index
                key_resp_2.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if key_resp_2.status == STARTED:
                theseKeys = event.getKeys(keyList=respKeyList)

                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                    key_resp_2.rt = key_resp_2.clock.getTime()
                    # was this 'correct'?
                    if (key_resp_2.keys == str(seqBroken)) or (key_resp_2.keys == seqBroken):
                        key_resp_2.corr = 1
                    else:
                        key_resp_2.corr = 0
                    # a response ends the routine
                    continueRoutine = False

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in responseComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "response"-------
        for thisComponent in responseComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys=None
            # was no response the correct answer?!
            if str(seqBroken).lower() == 'none':
               key_resp_2.corr = 1  # correct non-response
            else:
               key_resp_2.corr = 0  # failed to respond (incorrectly)
        # store data for trials (TrialHandler)
        trials.addData('key_resp_2.keys',key_resp_2.keys)
        trials.addData('key_resp_2.corr', key_resp_2.corr)
        if key_resp_2.keys != None:  # we had a response
            trials.addData('key_resp_2.rt', key_resp_2.rt)
        # the Routine "response" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()

    # completed 1 repeats of 'trials'

    if RecConn:
        s.send("P")

    thisExp.saveAsWideText(filename+'.csv')
    thisExp.saveAsPickle(filename)
    logging.flush()

# Function for motor tasks
def motorRoutine(exptType, trialList, trigger):

    import Adafruit_GPIO as GPIO
    import Adafruit_GPIO.FT232H as FT232H

    incorrect = int("00010000",2)
    correct = int("00010001",2)

    FT232H.use_FT232H()

    ft232h = FT232H.FT232H()

    pins = {0: GPIO.OUT,
            1: GPIO.OUT,
            2: GPIO.OUT,
            3: GPIO.OUT,
            8: GPIO.IN,
            9: GPIO.IN,
            10: GPIO.IN,
            11: GPIO.IN}

    values =   {0: GPIO.LOW,
                1: GPIO.LOW,
                2: GPIO.LOW,
                3: GPIO.LOW}

    ft232h.setup_pins(pins, values)
    inPins = np.array([8,9,10,11])
    
    endExpNow = False

    filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], exptType, expInfo['date'])

    thisExp = data.ExperimentHandler(name=exptType, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath=None,
        savePickle=True, saveWideText=True,
        dataFileName=filename)

    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    displayPenguin(inst.taskExplan[exptType][0]) # Explanantion

    trials_Demo = data.TrialHandler(nReps=1, method='sequential',
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(trialList),
        seed=None, name='trials_Demo')
    #thisExp.addLoop(trials_Demo)  # add the loop to the experiment
    thisTrials_Demo = trials_Demo.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrials_Prac.rgb)
    if thisTrials_Demo != None:
        for paramName in thisTrials_Demo.keys():
            exec(paramName + '= thisTrials_Demo.' + paramName)

    for thisTrials_Demo in trials_Demo:
        currentLoop = trials_Demo
        # abbreviate parameter names if possible (e.g. rgb = thisTrials_Prac.rgb)
        if thisTrials_Demo != None:
            for paramName in thisTrials_Demo.keys():
                exec(paramName + '= thisTrials_Demo.' + paramName)

        # set up handler to look after randomisation of conditions etc
        repeatingStims_Prac = data.TrialHandler(nReps=6, method='sequential',
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='repeatingStims_Prac')
        thisRepeatingStims_Prac = repeatingStims_Prac.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
        if thisRepeatingStims_Prac != None:
            for paramName in thisRepeatingStims_Prac.keys():
                exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

        for thisRepeatingStims_Prac in repeatingStims_Prac:
            currentLoop = repeatingStims_Prac

            # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
            if thisRepeatingStims_Prac != None:
                for paramName in thisRepeatingStims_Prac.keys():
                    exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

            # update component parameters for each repeat
            if currentLoop.nRemaining == 1:
                t1pin = test1pin
                t2pin = test2pin
                t1corrResp = test1resp
                t2corrResp = test2resp
                stim1trig = test1trig
                stim2trig = test2trig
            elif currentLoop.nRemaining == 0:
                t1pin = test3pin
                t2pin = test4pin
                t1corrResp = test3resp
                t2corrResp = test4resp
                stim1trig = test3trig
                stim2trig = test4trig
            else:
                t1pin = trial1pin
                t2pin = trial2pin
                t1corrResp = trial1resp
                t2corrResp = trial2resp
                stim1trig = train1trig
                stim2trig = train2trig

            Fixation.setText('')
            # ------Prepare to start Routine "stimTrial"-------
            t = 0
            stimTrialClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            t1resp = event.BuilderKeyResponse()
            # keep track of which components have finished
            stimTrialComponents = [Fixation, t1resp]
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "stimTrial"-------
            while continueRoutine:
                # get current time
                t = stimTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *s1_o1* updates
                if t >= 0.0 and Fixation.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Fixation.tStart = t
                    Fixation.frameNStart = frameN  # exact frame index
                    Fixation.setAutoDraw(True)
                    ft232h.set_high(t1pin)
                # *t1resp* updates
                if t >= 0.0 and t1resp.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    t1resp.tStart = t
                    t1resp.frameNStart = frameN  # exact frame index
                    t1resp.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(t1resp.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                if t1resp.status == STARTED:
                    buttons = ft232h.input_pins(inPins)
                    theseKeys = event.getKeys(keyList=['escape'])

                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                        ft232h.set_low(t1pin)
                    if any(buttons):
                        t1resp.rt = t1resp.clock.getTime()
                        t1resp.keys = inPins[np.array(buttons)].tolist()
                        if t1resp.keys == t1corrResp:
                            t1resp.corr = 1
                        else:
                            t1resp.corr = 0
                        ft232h.set_low(t1pin)
                        continueRoutine = False
                        while any(ft232h.input_pins(inPins)):
                            pass

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "stimTrial"-------
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store data for stimReps (TrialHandler)
            repeatingStims_Prac.addData('t1resp.keys',t1resp.keys)
            repeatingStims_Prac.addData('t1resp.corr', t1resp.corr)
            if t1resp.keys != None:  # we had a response
                repeatingStims_Prac.addData('t1resp.rt', t1resp.rt)
            # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()

            t = 0
            stimTrialClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            t2resp = event.BuilderKeyResponse()
            # keep track of which components have finished
            stimTrialComponents = [Fixation, t2resp]
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "stimTrial"-------
            while continueRoutine:
                # get current time
                t = stimTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *s1_o1* updates
                if t >= 0.0 and Fixation.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Fixation.tStart = t
                    Fixation.frameNStart = frameN  # exact frame index
                    Fixation.setAutoDraw(True)
                    ft232h.set_high(t2pin)
                # *t1resp* updates
                if t >= 0.0 and t2resp.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    t2resp.tStart = t
                    t2resp.frameNStart = frameN  # exact frame index
                    t2resp.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(t2resp.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                if t2resp.status == STARTED:
                    buttons = ft232h.input_pins(inPins)
                    theseKeys = event.getKeys(keyList=['escape'])

                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                        ft232h.set_low(t2pin)
                    if any(buttons):
                        t2resp.rt = t2resp.clock.getTime()
                        t2resp.keys = inPins[np.array(buttons)].tolist()
                        if t2resp.keys == t2corrResp:
                            t2resp.corr = 1
                        else:
                            t2resp.corr = 0
                        ft232h.set_low(t2pin)
                        continueRoutine = False
                        while any(ft232h.input_pins(inPins)):
                            pass

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "stimTrial"-------
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store data for stimReps (TrialHandler)
            repeatingStims_Prac.addData('t2resp.keys',t2resp.keys)
            repeatingStims_Prac.addData('t2resp.corr', t2resp.corr)
            if t1resp.keys != None:  # we had a response
                repeatingStims_Prac.addData('t2resp.rt', t2resp.rt)
            # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()

        # completed 5 repeats of 'repeatingStims_Prac'

        if trials_Demo.thisN == 0:
            displayPenguin(inst.taskExplan[exptType][1])
        elif trials_Demo.thisN == 1:
            displayPenguin(inst.brokenSeq)
            break

    for i in inst.gameRules:
        displayPenguin(i)

    displayPenguin(inst.ontoPractice)

    count = 0

    # set up handler to look after randomisation of conditions etc
    trials_Prac = data.TrialHandler(nReps=1, method='random',
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(trialList),
        seed=None, name='trials_Prac')
    thisTrials_Prac = trials_Prac.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrials_Prac.rgb)
    if thisTrials_Prac != None:
        for paramName in thisTrials_Prac.keys():
            exec(paramName + '= thisTrials_Prac.' + paramName)

    for thisTrials_Prac in trials_Prac:
        currentLoop = trials_Prac
        # abbreviate parameter names if possible (e.g. rgb = thisTrials_Prac.rgb)
        if thisTrials_Prac != None:
            for paramName in thisTrials_Prac.keys():
                exec(paramName + '= thisTrials_Prac.' + paramName)

        # set up handler to look after randomisation of conditions etc
        repeatingStims_Prac = data.TrialHandler(nReps=6, method='sequential',
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='repeatingStims_Prac')
        thisRepeatingStims_Prac = repeatingStims_Prac.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
        if thisRepeatingStims_Prac != None:
            for paramName in thisRepeatingStims_Prac.keys():
                exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

        for thisRepeatingStims_Prac in repeatingStims_Prac:
            currentLoop = repeatingStims_Prac

            # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
            if thisRepeatingStims_Prac != None:
                for paramName in thisRepeatingStims_Prac.keys():
                    exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

            # update component parameters for each repeat
            if currentLoop.nRemaining == 1:
                t1pin = test1pin
                t2pin = test2pin
                t1corrResp = test1resp
                t2corrResp = test2resp
                stim1trig = test1trig
                stim2trig = test2trig
            elif currentLoop.nRemaining == 0:
                t1pin = test3pin
                t2pin = test4pin
                t1corrResp = test3resp
                t2corrResp = test4resp
                stim1trig = test3trig
                stim2trig = test4trig
            else:
                t1pin = trial1pin
                t2pin = trial2pin
                t1corrResp = trial1resp
                t2corrResp = trial2resp
                stim1trig = train1trig
                stim2trig = train2trig

            Fixation.setText('')
            # ------Prepare to start Routine "stimTrial"-------
            t = 0
            stimTrialClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            t1resp = event.BuilderKeyResponse()
            # keep track of which components have finished
            stimTrialComponents = [Fixation, t1resp]
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "stimTrial"-------
            while continueRoutine:
                # get current time
                t = stimTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *s1_o1* updates
                if t >= 0.0 and Fixation.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Fixation.tStart = t
                    Fixation.frameNStart = frameN  # exact frame index
                    Fixation.setAutoDraw(True)
                    ft232h.set_high(t1pin)
                # *t1resp* updates
                if t >= 0.0 and t1resp.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    t1resp.tStart = t
                    t1resp.frameNStart = frameN  # exact frame index
                    t1resp.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(t1resp.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                if t1resp.status == STARTED:
                    buttons = ft232h.input_pins(inPins)
                    theseKeys = event.getKeys(keyList=['escape'])

                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                        ft232h.set_low(t1pin)
                    if any(buttons):
                        t1resp.rt = t1resp.clock.getTime()
                        t1resp.keys = inPins[np.array(buttons)].tolist()
                        if t1resp.keys == t1corrResp:
                            t1resp.corr = 1
                        else:
                            t1resp.corr = 0
                        ft232h.set_low(t1pin)
                        continueRoutine = False
                        while any(ft232h.input_pins(inPins)):
                            pass

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "stimTrial"-------
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store data for stimReps (TrialHandler)
            repeatingStims_Prac.addData('t1resp.keys',t1resp.keys)
            repeatingStims_Prac.addData('t1resp.corr', t1resp.corr)
            if t1resp.keys != None:  # we had a response
                repeatingStims_Prac.addData('t1resp.rt', t1resp.rt)
            # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            
            t = 0
            stimTrialClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            t2resp = event.BuilderKeyResponse()
            # keep track of which components have finished
            stimTrialComponents = [Fixation, t2resp]
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "stimTrial"-------
            while continueRoutine:
                # get current time
                t = stimTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *s1_o1* updates
                if t >= 0.0 and Fixation.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Fixation.tStart = t
                    Fixation.frameNStart = frameN  # exact frame index
                    Fixation.setAutoDraw(True)
                    ft232h.set_high(t2pin)
                # *t1resp* updates
                if t >= 0.0 and t2resp.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    t2resp.tStart = t
                    t2resp.frameNStart = frameN  # exact frame index
                    t2resp.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(t2resp.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                if t2resp.status == STARTED:
                    buttons = ft232h.input_pins(inPins)
                    theseKeys = event.getKeys(keyList=['escape'])

                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                        ft232h.set_low(t2pin)
                    if any(buttons):
                        t2resp.rt = t2resp.clock.getTime()
                        t2resp.keys = inPins[np.array(buttons)].tolist()
                        if t2resp.keys == t2corrResp:
                            t2resp.corr = 1
                        else:
                            t2resp.corr = 0
                        ft232h.set_low(t2pin)
                        continueRoutine = False
                        while any(ft232h.input_pins(inPins)):
                            pass

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "stimTrial"-------
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store data for stimReps (TrialHandler)
            repeatingStims_Prac.addData('t2resp.keys',t2resp.keys)
            repeatingStims_Prac.addData('t2resp.corr', t2resp.corr)
            if t1resp.keys != None:  # we had a response
                repeatingStims_Prac.addData('t2resp.rt', t2resp.rt)
            # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()

        # completed 5 repeats of 'repeatingStims_Prac'


        # ------Prepare to start Routine "response"-------
        t = 0
        responseClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        key_resp_2 = event.BuilderKeyResponse()
        # keep track of which components have finished
        textBox.setText(inst.responsePrompt)
        responseComponents = [speechImage, detectiveImage, key_resp_2, textBox]
        for thisComponent in responseComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        # -------Start Routine "response"-------
        while continueRoutine:
            # get current time
            t = responseClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *responseText* updates
            if t >= 0.0 and speechImage.status == NOT_STARTED:
                # keep track of start time/frame for later
                speechImage.tStart = t
                speechImage.frameNStart = frameN  # exact frame index
                speechImage.setAutoDraw(True)

            if t >= 0.0 and detectiveImage.status == NOT_STARTED:
                # keep track of start time/frame for later
                detectiveImage.tStart = t
                detectiveImage.frameNStart = frameN  # exact frame index
                detectiveImage.setAutoDraw(True)

            if t >= 0.0 and textBox.status == NOT_STARTED:
                # keep track of start time/frame for later
                textBox.tStart = t
                textBox.frameNStart = frameN  # exact frame index
                textBox.setAutoDraw(True)

            # *key_resp_2* updates
            if t >= 0.0 and key_resp_2.status == NOT_STARTED:
                # keep track of start time/frame for later
                key_resp_2.tStart = t
                key_resp_2.frameNStart = frameN  # exact frame index
                key_resp_2.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if key_resp_2.status == STARTED:
                theseKeys = event.getKeys(keyList=respKeyList)

                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                    key_resp_2.rt = key_resp_2.clock.getTime()
                    # was this 'correct'?
                    if (key_resp_2.keys == str(seqBroken)) or (key_resp_2.keys == seqBroken):
                        key_resp_2.corr = 1
                    else:
                        key_resp_2.corr = 0
                    # a response ends the routine
                    continueRoutine = False

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in responseComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "response"-------
        for thisComponent in responseComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys=None
            # was no response the correct answer?!
            if str(seqBroken).lower() == 'none':
               key_resp_2.corr = 1  # correct non-response
            else:
               key_resp_2.corr = 0  # failed to respond (incorrectly)
        # store data for trials_Prac (TrialHandler)
        trials_Prac.addData('key_resp_2.keys',key_resp_2.keys)
        trials_Prac.addData('key_resp_2.corr', key_resp_2.corr)
        if key_resp_2.keys != None:  # we had a response
            trials_Prac.addData('key_resp_2.rt', key_resp_2.rt)
        # the Routine "response" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()

        if key_resp_2.corr == 1:
            feedbackRoutine(inst.posFB,1)
            count += 1
        else:
            feedbackRoutine(inst.negFB_M,0)

        # If participants get more than 2 correct then move onto the main experiment
        if count < Ncorr4prac:
            displayPenguin(inst.readyForNext)
        else:
            break

    # completed 5 repeats of 'trials_Prac'

    if RecConn:
        s.send("D")
        s.send("S")

    displayPenguin(inst.ontoTrials)

    sendTrigger(int(trigger))

    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=motorReps, method='fullRandom',
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(trialList),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)

    for thisTrial in trials:
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial.keys():
                exec(paramName + '= thisTrial.' + paramName)

        # set up handler to look after randomisation of conditions etc
        repeatingStims = data.TrialHandler(nReps=6, method='sequential',
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='repeatingStims')
        thisExp.addLoop(repeatingStims)  # add the loop to the experiment
        thisRepeatingStim = repeatingStims.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStim.rgb)
        if thisRepeatingStim != None:
            for paramName in thisRepeatingStim.keys():
                exec(paramName + '= thisRepeatingStim.' + paramName)

        for thisRepeatingStim in repeatingStims:
            currentLoop = repeatingStims

            # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
            if thisRepeatingStim != None:
                for paramName in thisRepeatingStim.keys():
                    exec(paramName + '= thisRepeatingStim.' + paramName)


            # update component parameters for each repeat
            if currentLoop.nRemaining == 1:
                t1pin = test1pin
                t2pin = test2pin
                t1corrResp = test1resp
                t2corrResp = test2resp
                stim1trig = test1trig
                stim2trig = test2trig
            elif currentLoop.nRemaining == 0:
                t1pin = test3pin
                t2pin = test4pin
                t1corrResp = test3resp
                t2corrResp = test4resp
                stim1trig = test3trig
                stim2trig = test4trig
            else:
                t1pin = trial1pin
                t2pin = trial2pin
                t1corrResp = trial1resp
                t2corrResp = trial2resp
                stim1trig = train1trig
                stim2trig = train2trig

            # ------Prepare to start Routine "stimTrial"-------
            t = 0
            stimTrialClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            t1resp = event.BuilderKeyResponse()
            # keep track of which components have finished
            stimTrialComponents = [Fixation, t1resp]
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "stimTrial"-------
            while continueRoutine:
                # get current time
                t = stimTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *s1_o1* updates
                if t >= 0.0 and Fixation.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Fixation.tStart = t
                    Fixation.frameNStart = frameN  # exact frame index
                    Fixation.setAutoDraw(True)
                    ft232h.set_high(t1pin)
                    sendTrigger(stim1trig)
                # *t1resp* updates
                if t >= 0.0 and t1resp.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    t1resp.tStart = t
                    t1resp.frameNStart = frameN  # exact frame index
                    t1resp.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(t1resp.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                if t1resp.status == STARTED:
                    buttons = ft232h.input_pins(inPins)
                    theseKeys = event.getKeys(keyList=['escape'])

                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                        ft232h.set_low(t1pin)
                    if any(buttons):
                        t1resp.rt = t1resp.clock.getTime()
                        t1resp.keys = inPins[np.array(buttons)].tolist()
                        if t1resp.keys == t1corrResp:
                            t1resp.corr = 1
                            sendTrigger(correct)
                        else:
                            t1resp.corr = 0
                            sendTrigger(incorrect)
                        ft232h.set_low(t1pin)
                        continueRoutine = False
                        while any(ft232h.input_pins(inPins)):
                            pass

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "stimTrial"-------
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store data for stimReps (TrialHandler)
            repeatingStims.addData('t1resp.keys',t1resp.keys)
            repeatingStims.addData('t1resp.corr', t1resp.corr)
            if t1resp.keys != None:  # we had a response
                repeatingStims.addData('t1resp.rt', t1resp.rt)
            # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()

            t = 0
            stimTrialClock.reset()  # clock
            frameN = -1
            continueRoutine = True
            t2resp = event.BuilderKeyResponse()
            # keep track of which components have finished
            stimTrialComponents = [Fixation, t2resp]
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "stimTrial"-------
            while continueRoutine:
                # get current time
                t = stimTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # *s1_o1* updates
                if t >= 0.0 and Fixation.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Fixation.tStart = t
                    Fixation.frameNStart = frameN  # exact frame index
                    Fixation.setAutoDraw(True)
                    ft232h.set_high(t2pin)
                    sendTrigger(stim2trig)
                # *t1resp* updates
                if t >= 0.0 and t2resp.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    t2resp.tStart = t
                    t2resp.frameNStart = frameN  # exact frame index
                    t2resp.status = STARTED
                    # keyboard checking is just starting
                    win.callOnFlip(t2resp.clock.reset)  # t=0 on next screen flip
                    event.clearEvents(eventType='keyboard')
                if t2resp.status == STARTED:
                    buttons = ft232h.input_pins(inPins)
                    theseKeys = event.getKeys(keyList=['escape'])

                    # check for quit:
                    if "escape" in theseKeys:
                        endExpNow = True
                        ft232h.set_low(t2pin)
                    if any(buttons):
                        t2resp.rt = t2resp.clock.getTime()
                        t2resp.keys = inPins[np.array(buttons)].tolist()
                        if t2resp.keys == t2corrResp:
                            t2resp.corr = 1
                            sendTrigger(correct)
                        else:
                            t2resp.corr = 0
                            sendTrigger(incorrect)
                        ft232h.set_low(t2pin)
                        continueRoutine = False
                        while any(ft232h.input_pins(inPins)):
                            pass

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "stimTrial"-------
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # store data for stimReps (TrialHandler)
            repeatingStims.addData('t2resp.keys',t2resp.keys)
            repeatingStims.addData('t2resp.corr', t2resp.corr)
            if t1resp.keys != None:  # we had a response
                repeatingStims.addData('t2resp.rt', t2resp.rt)
            # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()

        # completed 5 repeats of 'repeatingStims_Prac'

        # ------Prepare to start Routine "response"-------
        t = 0
        responseClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        key_resp_2 = event.BuilderKeyResponse()
        # keep track of which components have finished
        textBox.setText(inst.responsePrompt)
        responseComponents = [speechImage, textBox, detectiveImage, key_resp_2]
        for thisComponent in responseComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        # -------Start Routine "response"-------
        while continueRoutine:
            # get current time
            t = responseClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            if t >= 0.0 and detectiveImage.status == NOT_STARTED:
                # keep track of start time/frame for later
                detectiveImage.tStart = t
                detectiveImage.frameNStart = frameN  # exact frame index
                detectiveImage.setAutoDraw(True)

            if t >= 0.0 and speechImage.status == NOT_STARTED:
                # keep track of start time/frame for later
                speechImage.tStart = t
                speechImage.frameNStart = frameN  # exact frame index
                speechImage.setAutoDraw(True)

            # *responseText* updates
            if t >= 0.0 and textBox.status == NOT_STARTED:
                # keep track of start time/frame for later
                textBox.tStart = t
                textBox.frameNStart = frameN  # exact frame index
                textBox.setAutoDraw(True)

            # *key_resp_2* updates
            if t >= 0.0 and key_resp_2.status == NOT_STARTED:
                # keep track of start time/frame for later
                key_resp_2.tStart = t
                key_resp_2.frameNStart = frameN  # exact frame index
                key_resp_2.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if key_resp_2.status == STARTED:
                theseKeys = event.getKeys(keyList=respKeyList)

                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                    key_resp_2.rt = key_resp_2.clock.getTime()
                    # was this 'correct'?
                    if (key_resp_2.keys == str(seqBroken)) or (key_resp_2.keys == seqBroken):
                        key_resp_2.corr = 1
                    else:
                        key_resp_2.corr = 0
                    # a response ends the routine
                    continueRoutine = False

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in responseComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "response"-------
        for thisComponent in responseComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys=None
            # was no response the correct answer?!
            if str(seqBroken).lower() == 'none':
               key_resp_2.corr = 1  # correct non-response
            else:
               key_resp_2.corr = 0  # failed to respond (incorrectly)
        # store data for trials (TrialHandler)
        trials.addData('key_resp_2.keys',key_resp_2.keys)
        trials.addData('key_resp_2.corr', key_resp_2.corr)
        if key_resp_2.keys != None:  # we had a response
            trials.addData('key_resp_2.rt', key_resp_2.rt)
        # the Routine "response" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
        displayPenguin("Ready for the next one?")


    # completed 4 repeats of 'trials'

    if RecConn:
        s.send("P")

# Function for linguistic tasks
def linguisticRoutine(exptType, trialList, trigger):
    import csv

    ITI = 0.5
    ISI = 0.2

    with open('WordList.csv', 'rb') as f:
        reader = csv.reader(f)
        wordList = list(reader)

    listCount = -1
    
    endExpNow = False

    filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participant'], exptType, expInfo['date'])

    thisExp = data.ExperimentHandler(name=exptType, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath=None,
        savePickle=True, saveWideText=True,
        dataFileName=filename)

    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log', level=logging.EXP)
    logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

    displayPenguin(inst.taskExplan[exptType][0]) # Explanantion

    startBlank = Blank
    midBlank = Blank
    endBlank = Blank

    trials_Demo = data.TrialHandler(nReps=1, method='sequential',
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(trialList),
        seed=None, name='trials_Demo')
    #thisExp.addLoop(trials_Demo)  # add the loop to the experiment
    thisTrials_Demo = trials_Demo.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrials_Prac.rgb)
    if thisTrials_Demo != None:
        for paramName in thisTrials_Demo.keys():
            exec(paramName + '= thisTrials_Demo.' + paramName)

    for thisTrials_Demo in trials_Demo:
        currentLoop = trials_Demo
        # abbreviate parameter names if possible (e.g. rgb = thisTrials_Prac.rgb)
        if thisTrials_Demo != None:
            for paramName in thisTrials_Demo.keys():
                exec(paramName + '= thisTrials_Demo.' + paramName)

        # set up handler to look after randomisation of conditions etc
        repeatingStims_Prac = data.TrialHandler(nReps=6, method='sequential',
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='repeatingStims_Prac')
        thisExp.addLoop(repeatingStims_Prac)  # add the loop to the experiment
        thisRepeatingStims_Prac = repeatingStims_Prac.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
        if thisRepeatingStims_Prac != None:
            for paramName in thisRepeatingStims_Prac.keys():
                exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

        for thisRepeatingStims_Prac in repeatingStims_Prac:
            currentLoop = repeatingStims_Prac

            # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
            if thisRepeatingStims_Prac != None:
                for paramName in thisRepeatingStims_Prac.keys():
                    exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

            # ------Prepare to start Routine "stimTrial"-------
            t = 0
            stimTrialClock.reset()  # clock
            frameN = -1
            continueRoutine = True

            # update component parameters for each repeat
            listCount += 1
            if currentLoop.nRemaining == 0 and seqType != 0:
                stimText1.setText(wordList[listCount][1])
                stimText2.setText(wordList[listCount][0])
                stimSound1.setSound("sounds/" + wordList[listCount][1] + ".wav")
                stimSound2.setSound("sounds/" + wordList[listCount][0] + ".wav")
            else:
                stimText1.setText(wordList[listCount][0])
                stimText2.setText(wordList[listCount][1])
                stimSound1.setSound("sounds/" + wordList[listCount][0] + ".wav")
                stimSound2.setSound("sounds/" + wordList[listCount][1] + ".wav")

            # keep track of which components have finished
            stimTrialComponents = [stimText1, stimText2, startBlank, midBlank, endBlank, Fixation, stimSound1, stimSound2]
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "stimTrial"-------
            while continueRoutine:
                # get current time
                t = stimTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # Draw first blank screen
                if t >= 0.0 and startBlank.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    startBlank.tStart = t
                    startBlank.frameNStart = frameN  # exact frame index
                    startBlank.setAutoDraw(True)
                frameRemains = 0.0 + ISI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if startBlank.status == STARTED and t >= frameRemains:
                    startBlank.setAutoDraw(False)

                # display and play stimulus 1
                if t >= ISI and stimText1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimText1.tStart = t
                    stimText1.frameNStart = frameN  # exact frame index
                    stimText1.setAutoDraw(True)
                frameRemains = ISI + stim1time - win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimText1.status == STARTED and t >= frameRemains:
                    stimText1.setAutoDraw(False)
                    
                if t >= ISI and stimSound1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimSound1.tStart = t
                    stimSound1.frameNStart = frameN  # exact frame index
                    stimSound1.play()  # start the sound (it finishes automatically)
                frameRemains = ISI + stim1time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimSound1.status == STARTED and t >= frameRemains:
                    stimSound1.stop()  # stop the sound (if longer than duration)

                # Draw middle blank screen
                if t >= (ISI + stim1time) and midBlank.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    midBlank.tStart = t
                    midBlank.frameNStart = frameN  # exact frame index
                    midBlank.setAutoDraw(True)
                frameRemains = (ISI + stim1time) + ISI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if midBlank.status == STARTED and t >= frameRemains:
                    midBlank.setAutoDraw(False)

                # display and play stimulus 2
                if t >= (ISI*2 + stim1time) and stimText2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimText2.tStart = t
                    stimText2.frameNStart = frameN  # exact frame index
                    stimText2.setAutoDraw(True)
                frameRemains = (ISI*2 + stim1time) + stim2time - win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimText2.status == STARTED and t >= frameRemains:
                    stimText2.setAutoDraw(False)
                    
                if t >= (ISI*2 + stim1time) and stimSound2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimSound2.tStart = t
                    stimSound2.frameNStart = frameN  # exact frame index
                    stimSound2.play()  # start the sound (it finishes automatically)
                frameRemains = (ISI*2 + stim1time) + stim2time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimSound2.status == STARTED and t >= frameRemains:
                    stimSound2.stop()  # stop the sound (if longer than duration)

                # Draw final blank screen
                if t >= (ISI*2 + stim1time + stim2time) and endBlank.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    endBlank.tStart = t
                    endBlank.frameNStart = frameN  # exact frame index
                    endBlank.setAutoDraw(True)
                frameRemains = (ISI*2 + stim1time + stim2time) + ISI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if endBlank.status == STARTED and t >= frameRemains:
                    endBlank.setAutoDraw(False)

                # Draw intertrial fixation screen
                if t >= (ISI*3 + stim1time + stim2time) and Fixation.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Fixation.tStart = t
                    Fixation.frameNStart = frameN  # exact frame index
                    Fixation.setAutoDraw(True)
                frameRemains = (ISI*3 + stim1time + stim2time) + ITI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if Fixation.status == STARTED and t >= frameRemains:
                    Fixation.setAutoDraw(False)

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "stimTrial"-------
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()

        # completed 5 repeats of 'repeatingStims_Prac'

        if trials_Demo.thisN == 0:
            displayPenguin(inst.taskExplan[exptType][1])
        elif trials_Demo.thisN == 1:
            displayPenguin(inst.brokenSeq)
            break

    for i in inst.gameRules:
        displayPenguin(i)

    displayPenguin(inst.ontoPractice)

    count = 0

    # set up handler to look after randomisation of conditions etc
    trials_Prac = data.TrialHandler(nReps=1, method='random',
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(trialList),
        seed=None, name='trials_Prac')
    thisExp.addLoop(trials_Prac)  # add the loop to the experiment
    thisTrials_Prac = trials_Prac.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrials_Prac.rgb)
    if thisTrials_Prac != None:
        for paramName in thisTrials_Prac.keys():
            exec(paramName + '= thisTrials_Prac.' + paramName)

    for thisTrials_Prac in trials_Prac:
        currentLoop = trials_Prac
        # abbreviate parameter names if possible (e.g. rgb = thisTrials_Prac.rgb)
        if thisTrials_Prac != None:
            for paramName in thisTrials_Prac.keys():
                exec(paramName + '= thisTrials_Prac.' + paramName)

        # set up handler to look after randomisation of conditions etc
        repeatingStims_Prac = data.TrialHandler(nReps=6, method='sequential',
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='repeatingStims_Prac')
        thisExp.addLoop(repeatingStims_Prac)  # add the loop to the experiment
        thisRepeatingStims_Prac = repeatingStims_Prac.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
        if thisRepeatingStims_Prac != None:
            for paramName in thisRepeatingStims_Prac.keys():
                exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

        for thisRepeatingStims_Prac in repeatingStims_Prac:
            currentLoop = repeatingStims_Prac

            # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
            if thisRepeatingStims_Prac != None:
                for paramName in thisRepeatingStims_Prac.keys():
                    exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

            # ------Prepare to start Routine "stimTrial"-------
            t = 0
            stimTrialClock.reset()  # clock
            frameN = -1
            continueRoutine = True

            # update component parameters for each repeat
            listCount += 1
            if currentLoop.nRemaining == 0 and seqType != 0:
                stimText1.setText(wordList[listCount][1])
                stimText2.setText(wordList[listCount][0])
                stimSound1.setSound("sounds/" + wordList[listCount][1] + ".wav")
                stimSound2.setSound("sounds/" + wordList[listCount][0] + ".wav")
            else:
                stimText1.setText(wordList[listCount][0])
                stimText2.setText(wordList[listCount][1])
                stimSound1.setSound("sounds/" + wordList[listCount][0] + ".wav")
                stimSound2.setSound("sounds/" + wordList[listCount][1] + ".wav")
            # keep track of which components have finished
            stimTrialComponents = [stimText1, stimText2, startBlank, midBlank, endBlank, Fixation, stimSound1,stimSound2]
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "stimTrial"-------
            while continueRoutine:
                # get current time
                t = stimTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # Draw first blank screen
                if t >= 0.0 and startBlank.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    startBlank.tStart = t
                    startBlank.frameNStart = frameN  # exact frame index
                    startBlank.setAutoDraw(True)
                frameRemains = 0.0 + ISI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if startBlank.status == STARTED and t >= frameRemains:
                    startBlank.setAutoDraw(False)

                # display and play stimulus 1
                if t >= ISI and stimText1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimText1.tStart = t
                    stimText1.frameNStart = frameN  # exact frame index
                    stimText1.setAutoDraw(True)
                frameRemains = ISI + stim1time - win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimText1.status == STARTED and t >= frameRemains:
                    stimText1.setAutoDraw(False)
                    
                if t >= ISI and stimSound1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimSound1.tStart = t
                    stimSound1.frameNStart = frameN  # exact frame index
                    stimSound1.play()  # start the sound (it finishes automatically)
                frameRemains = ISI + stim1time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimSound1.status == STARTED and t >= frameRemains:
                    stimSound1.stop()  # stop the sound (if longer than duration)

                # Draw middle blank screen
                if t >= (ISI + stim1time) and midBlank.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    midBlank.tStart = t
                    midBlank.frameNStart = frameN  # exact frame index
                    midBlank.setAutoDraw(True)
                frameRemains = (ISI + stim1time) + ISI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if midBlank.status == STARTED and t >= frameRemains:
                    midBlank.setAutoDraw(False)

                # display and play stimulus 2
                if t >= (ISI*2 + stim1time) and stimText2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimText2.tStart = t
                    stimText2.frameNStart = frameN  # exact frame index
                    stimText2.setAutoDraw(True)
                frameRemains = (ISI*2 + stim1time) + stim2time - win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimText2.status == STARTED and t >= frameRemains:
                    stimText2.setAutoDraw(False)
                    
                if t >= (ISI*2 + stim1time) and stimSound2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimSound2.tStart = t
                    stimSound2.frameNStart = frameN  # exact frame index
                    stimSound2.play()  # start the sound (it finishes automatically)
                frameRemains = (ISI*2 + stim1time) + stim2time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimSound2.status == STARTED and t >= frameRemains:
                    stimSound2.stop()  # stop the sound (if longer than duration)

                # Draw final blank screen
                if t >= (ISI*2 + stim1time + stim2time) and endBlank.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    endBlank.tStart = t
                    endBlank.frameNStart = frameN  # exact frame index
                    endBlank.setAutoDraw(True)
                frameRemains = (ISI*2 + stim1time + stim2time) + ISI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if endBlank.status == STARTED and t >= frameRemains:
                    endBlank.setAutoDraw(False)

                # Draw intertrial fixation screen
                if t >= (ISI*3 + stim1time + stim2time) and Fixation.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Fixation.tStart = t
                    Fixation.frameNStart = frameN  # exact frame index
                    Fixation.setAutoDraw(True)
                frameRemains = (ISI*3 + stim1time + stim2time) + ITI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if Fixation.status == STARTED and t >= frameRemains:
                    Fixation.setAutoDraw(False)

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "stimTrial"-------
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()

        # completed 6 repeats of 'repeatingStims_Prac'

        # ------Prepare to start Routine "response"-------
        t = 0
        responseClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        key_resp_2 = event.BuilderKeyResponse()
        # keep track of which components have finished
        textBox.setText(inst.responsePrompt)
        responseComponents = [speechImage, detectiveImage, key_resp_2, textBox]
        for thisComponent in responseComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        # -------Start Routine "response"-------
        while continueRoutine:
            # get current time
            t = responseClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *responseText* updates
            if t >= 0.0 and speechImage.status == NOT_STARTED:
                # keep track of start time/frame for later
                speechImage.tStart = t
                speechImage.frameNStart = frameN  # exact frame index
                speechImage.setAutoDraw(True)

            if t >= 0.0 and detectiveImage.status == NOT_STARTED:
                # keep track of start time/frame for later
                detectiveImage.tStart = t
                detectiveImage.frameNStart = frameN  # exact frame index
                detectiveImage.setAutoDraw(True)

            if t >= 0.0 and textBox.status == NOT_STARTED:
                # keep track of start time/frame for later
                textBox.tStart = t
                textBox.frameNStart = frameN  # exact frame index
                textBox.setAutoDraw(True)

            # *key_resp_2* updates
            if t >= 0.0 and key_resp_2.status == NOT_STARTED:
                # keep track of start time/frame for later
                key_resp_2.tStart = t
                key_resp_2.frameNStart = frameN  # exact frame index
                key_resp_2.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if key_resp_2.status == STARTED:
                theseKeys = event.getKeys(keyList=respKeyList)

                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                    key_resp_2.rt = key_resp_2.clock.getTime()
                    # was this 'correct'?
                    if (key_resp_2.keys == str(brokenSeq)) or (key_resp_2.keys == brokenSeq):
                        key_resp_2.corr = 1
                    else:
                        key_resp_2.corr = 0
                    # a response ends the routine
                    continueRoutine = False

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in responseComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "response"-------
        for thisComponent in responseComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys=None
            # was no response the correct answer?!
            if str(seqBroken).lower() == 'none':
               key_resp_2.corr = 1  # correct non-response
            else:
               key_resp_2.corr = 0  # failed to respond (incorrectly)
        # store data for trials_Prac (TrialHandler)
        trials_Prac.addData('key_resp_2.keys',key_resp_2.keys)
        trials_Prac.addData('key_resp_2.corr', key_resp_2.corr)
        if key_resp_2.keys != None:  # we had a response
            trials_Prac.addData('key_resp_2.rt', key_resp_2.rt)
        # the Routine "response" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()

        if key_resp_2.corr == 1:
            feedbackRoutine(inst.posFB,1)
            count += 1
        else:
            feedbackRoutine(inst.negFB,0)

        # Repeat trials at a slower speed if incorrect response given
        if key_resp_2.corr == 0:
            
            listCount -= 6
            
            repeatingStims_Prac = data.TrialHandler(nReps=6, method='sequential',
                extraInfo=expInfo, originPath=-1,
                trialList=[None],
                seed=None, name='repeatingStims_Prac')
            thisExp.addLoop(repeatingStims_Prac)  # add the loop to the experiment
            thisRepeatingStims_Prac = repeatingStims_Prac.trialList[0]  # so we can initialise stimuli with some values
            # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
            if thisRepeatingStims_Prac != None:
                for paramName in thisRepeatingStims_Prac.keys():
                    exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

            for thisRepeatingStims_Prac in repeatingStims_Prac:
                currentLoop = repeatingStims_Prac

                # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStims_Prac.rgb)
                if thisRepeatingStims_Prac != None:
                    for paramName in thisRepeatingStims_Prac.keys():
                        exec(paramName + '= thisRepeatingStims_Prac.' + paramName)

                # ------Prepare to start Routine "stimTrial"-------
                t = 0
                stimTrialClock.reset()  # clock
                frameN = -1
                continueRoutine = True

            listCount += 1
            if currentLoop.nRemaining == 0 and type != 0:
                stimText1.setText(wordList[listCount][1])
                stimText2.setText(wordList[listCount][0])
                stimSound1.setSound("sounds/" + wordList[listCount][1] + ".wav")
                stimSound2.setSound("sounds/" + wordList[listCount][0] + ".wav")
            else:
                stimText1.setText(wordList[listCount][0])
                stimText2.setText(wordList[listCount][1])
                stimSound1.setSound("sounds/" + wordList[listCount][0] + ".wav")
                stimSound2.setSound("sounds/" + wordList[listCount][1] + ".wav")
            # keep track of which components have finished
            stimTrialComponents = [stimText1, stimText2, startBlank, midBlank, endBlank, Fixation, stimSound1,stimSound2]
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "stimTrial"-------
            while continueRoutine:
                # get current time
                t = stimTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # Draw first blank screen
                if t >= 0.0 and startBlank.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    startBlank.tStart = t
                    startBlank.frameNStart = frameN  # exact frame index
                    startBlank.setAutoDraw(True)
                frameRemains = 0.0 + ISI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if startBlank.status == STARTED and t >= frameRemains:
                    startBlank.setAutoDraw(False)

                # display and play stimulus 1
                if t >= ISI and stimText1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimText1.tStart = t
                    stimText1.frameNStart = frameN  # exact frame index
                    stimText1.setAutoDraw(True)
                frameRemains = ISI + stim1time - win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimText1.status == STARTED and t >= frameRemains:
                    stimText1.setAutoDraw(False)
                    
                if t >= ISI and stimSound1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimSound1.tStart = t
                    stimSound1.frameNStart = frameN  # exact frame index
                    stimSound1.play()  # start the sound (it finishes automatically)
                frameRemains = ISI + stim1time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimSound1.status == STARTED and t >= frameRemains:
                    stimSound1.stop()  # stop the sound (if longer than duration)

                # Draw middle blank screen
                if t >= (ISI + stim1time) and midBlank.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    midBlank.tStart = t
                    midBlank.frameNStart = frameN  # exact frame index
                    midBlank.setAutoDraw(True)
                frameRemains = (ISI + stim1time) + ISI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if midBlank.status == STARTED and t >= frameRemains:
                    midBlank.setAutoDraw(False)

                # display and play stimulus 2
                if t >= (ISI*2 + stim1time) and stimText2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimText2.tStart = t
                    stimText2.frameNStart = frameN  # exact frame index
                    stimText2.setAutoDraw(True)
                frameRemains = (ISI*2 + stim1time) + stim2time - win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimText2.status == STARTED and t >= frameRemains:
                    stimText2.setAutoDraw(False)
                    
                if t >= (ISI*2 + stim1time) and stimSound2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimSound2.tStart = t
                    stimSound2.frameNStart = frameN  # exact frame index
                    stimSound2.play()  # start the sound (it finishes automatically)
                frameRemains = (ISI*2 + stim1time) + stim2time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimSound2.status == STARTED and t >= frameRemains:
                    stimSound2.stop()  # stop the sound (if longer than duration)

                # Draw final blank screen
                if t >= (ISI*2 + stim1time + stim2time) and endBlank.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    endBlank.tStart = t
                    endBlank.frameNStart = frameN  # exact frame index
                    endBlank.setAutoDraw(True)
                frameRemains = (ISI*2 + stim1time + stim2time) + ISI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if endBlank.status == STARTED and t >= frameRemains:
                    endBlank.setAutoDraw(False)

                # Draw intertrial fixation screen
                if t >= (ISI*3 + stim1time + stim2time) and Fixation.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Fixation.tStart = t
                    Fixation.frameNStart = frameN  # exact frame index
                    Fixation.setAutoDraw(True)
                frameRemains = (ISI*3 + stim1time + stim2time) + ITI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if Fixation.status == STARTED and t >= frameRemains:
                    Fixation.setAutoDraw(False)

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "stimTrial"-------
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()

            # completed 5 repeats of 'repeatingStims_Prac'

        # If participants get more than 2 correct then move onto the main experiment
        if count < Ncorr4prac:
            displayPenguin(inst.readyForNext)
        else:
            break

    # completed 5 repeats of 'trials_Prac'

    if RecConn:
        s.send("D")
        s.send("S")

    displayPenguin(inst.ontoTrials)

    listCount = 64

    sendTrigger(int(trigger))

    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler(nReps=linguisticReps, method='fullRandom',
        extraInfo=expInfo, originPath=-1,
        trialList=data.importConditions(trialList),
        seed=None, name='trials')
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)

    for thisTrial in trials:
        currentLoop = trials
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial.keys():
                exec(paramName + '= thisTrial.' + paramName)

        # set up handler to look after randomisation of conditions etc
        repeatingStims = data.TrialHandler(nReps=6, method='sequential',
            extraInfo=expInfo, originPath=-1,
            trialList=[None],
            seed=None, name='repeatingStims')
        thisExp.addLoop(repeatingStims)  # add the loop to the experiment
        thisRepeatingStim = repeatingStims.trialList[0]  # so we can initialise stimuli with some values
        # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStim.rgb)
        if thisRepeatingStim != None:
            for paramName in thisRepeatingStim.keys():
                exec(paramName + '= thisRepeatingStim.' + paramName)

        for thisRepeatingStim in repeatingStims:
            currentLoop = repeatingStims
            # abbreviate parameter names if possible (e.g. rgb = thisRepeatingStim.rgb)
            if thisRepeatingStim != None:
                for paramName in thisRepeatingStim.keys():
                    exec(paramName + '= thisRepeatingStim.' + paramName)

            # ------Prepare to start Routine "stimTrial"-------
            t = 0
            stimTrialClock.reset()  # clock
            frameN = -1
            continueRoutine = True

            # update component parameters for each repeat
            if currentLoop.nRemaining == 1 and (seqType == 1 or seqType == 0):
                listCount += 1
                stimText1.setText(wordList[listCount][0])
                stimText2.setText(wordList[listCount][1])
                stimSound1.setSound("sounds/" + wordList[listCount][0] + ".wav")
                stimSound2.setSound("sounds/" + wordList[listCount][1] + ".wav")
                stim1trig = train1trig
                stim2trig = train2trig
            elif currentLoop.nRemaining == 0 and (seqType == 1 or seqType == 0):
                stimText1.setText(test1word)
                stimText2.setText(test2word)
                stimSound1.setSound("sounds/" + test1word + ".wav")
                stimSound2.setSound("sounds/" + test2word + ".wav")
                stim1trig = test1trig
                stim2trig = test2trig
            elif currentLoop.nRemaining == 1 and seqType == 2:
                listCount += 1
                stimText1.setText(wordList[listCount][0])
                stimText2.setText(test2word)
                stimSound1.setSound("sounds/" + wordList[listCount][0] + ".wav")
                stimSound2.setSound("sounds/" + test2word + ".wav")
                stim1trig = train1trig
                stim2trig = test4trig
            elif currentLoop.nRemaining == 0 and seqType == 2:
                stimText1.setText(test1word)
                stimSound1.setSound("sounds/" + test1word + ".wav")
                stimText2.setText(wordList[listCount][1])
                stimSound2.setSound("sounds/" + wordList[listCount][1] + ".wav")
                stim1trig = test3trig
                stim2trig = train2trig
            else:
                listCount += 1
                stimText1.setText(wordList[listCount][0])
                stimText2.setText(wordList[listCount][1])
                stimSound1.setSound("sounds/" + wordList[listCount][0] + ".wav")
                stimSound2.setSound("sounds/" + wordList[listCount][1] + ".wav")
                stim1trig = train1trig
                stim2trig = train2trig

            # keep track of which components have finished
            stimTrialComponents = [stimText1, stimText2, startBlank, midBlank, endBlank, Fixation, stimSound1,stimSound2]
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, 'status'):
                    thisComponent.status = NOT_STARTED

            # -------Start Routine "stimTrial"-------
            while continueRoutine:
                # get current time
                t = stimTrialClock.getTime()
                frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
                # update/draw components on each frame

                # Draw first blank screen
                if t >= 0.0 and startBlank.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    startBlank.tStart = t
                    startBlank.frameNStart = frameN  # exact frame index
                    startBlank.setAutoDraw(True)
                frameRemains = 0.0 + ISI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if startBlank.status == STARTED and t >= frameRemains:
                    startBlank.setAutoDraw(False)

                # display and play stimulus 1
                if t >= ISI and stimText1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimText1.tStart = t
                    stimText1.frameNStart = frameN  # exact frame index
                    stimText1.setAutoDraw(True)
                    sendTrigger(stim1trig)
                frameRemains = ISI + stim1time - win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimText1.status == STARTED and t >= frameRemains:
                    stimText1.setAutoDraw(False)
                    
                if t >= ISI and stimSound1.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimSound1.tStart = t
                    stimSound1.frameNStart = frameN  # exact frame index
                    stimSound1.play()  # start the sound (it finishes automatically)
                frameRemains = ISI + stim1time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimSound1.status == STARTED and t >= frameRemains:
                    stimSound1.stop()  # stop the sound (if longer than duration)

                # Draw middle blank screen
                if t >= (ISI + stim1time) and midBlank.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    midBlank.tStart = t
                    midBlank.frameNStart = frameN  # exact frame index
                    midBlank.setAutoDraw(True)
                frameRemains = (ISI + stim1time) + ISI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if midBlank.status == STARTED and t >= frameRemains:
                    midBlank.setAutoDraw(False)

                # display and play stimulus 2
                if t >= (ISI*2 + stim1time) and stimText2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimText2.tStart = t
                    stimText2.frameNStart = frameN  # exact frame index
                    stimText2.setAutoDraw(True)
                    sendTrigger(stim2trig)
                frameRemains = (ISI*2 + stim1time) + stim2time - win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimText2.status == STARTED and t >= frameRemains:
                    stimText2.setAutoDraw(False)
                    
                if t >= (ISI*2 + stim1time) and stimSound2.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    stimSound2.tStart = t
                    stimSound2.frameNStart = frameN  # exact frame index
                    stimSound2.play()  # start the sound (it finishes automatically)
                frameRemains = (ISI*2 + stim1time) + stim2time- win.monitorFramePeriod * 0.75  # most of one frame period left
                if stimSound2.status == STARTED and t >= frameRemains:
                    stimSound2.stop()  # stop the sound (if longer than duration)

                # Draw final blank screen
                if t >= (ISI*2 + stim1time + stim2time) and endBlank.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    endBlank.tStart = t
                    endBlank.frameNStart = frameN  # exact frame index
                    endBlank.setAutoDraw(True)
                frameRemains = (ISI*2 + stim1time + stim2time) + ISI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if endBlank.status == STARTED and t >= frameRemains:
                    endBlank.setAutoDraw(False)

                # Draw intertrial fixation screen
                if t >= (ISI*3 + stim1time + stim2time) and Fixation.status == NOT_STARTED:
                    # keep track of start time/frame for later
                    Fixation.tStart = t
                    Fixation.frameNStart = frameN  # exact frame index
                    Fixation.setAutoDraw(True)
                frameRemains = (ISI*3 + stim1time + stim2time) + ITI - win.monitorFramePeriod * 0.75  # most of one frame period left
                if Fixation.status == STARTED and t >= frameRemains:
                    Fixation.setAutoDraw(False)

                # check if all components have finished
                if not continueRoutine:  # a component has requested a forced-end of Routine
                    break
                continueRoutine = False  # will revert to True if at least one component still running
                for thisComponent in stimTrialComponents:
                    if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                        continueRoutine = True
                        break  # at least one component has not yet finished

                # check for quit (the Esc key)
                if endExpNow or event.getKeys(keyList=["escape"]):
                    core.quit()

                # refresh the screen
                if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                    win.flip()

            # -------Ending Routine "stimTrial"-------
            for thisComponent in stimTrialComponents:
                if hasattr(thisComponent, "setAutoDraw"):
                    thisComponent.setAutoDraw(False)
            # the Routine "stimTrial" was not non-slip safe, so reset the non-slip timer
            routineTimer.reset()
            thisExp.nextEntry()

        # ------Prepare to start Routine "response"-------
        t = 0
        responseClock.reset()  # clock
        frameN = -1
        continueRoutine = True
        # update component parameters for each repeat
        key_resp_2 = event.BuilderKeyResponse()
        # keep track of which components have finished
        textBox.setText(inst.responsePrompt)
        responseComponents = [speechImage, detectiveImage, key_resp_2, textBox]
        for thisComponent in responseComponents:
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED

        # -------Start Routine "response"-------
        while continueRoutine:
            # get current time
            t = responseClock.getTime()
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame

            # *responseText* updates
            if t >= 0.0 and speechImage.status == NOT_STARTED:
                # keep track of start time/frame for later
                speechImage.tStart = t
                speechImage.frameNStart = frameN  # exact frame index
                speechImage.setAutoDraw(True)

            if t >= 0.0 and detectiveImage.status == NOT_STARTED:
                # keep track of start time/frame for later
                detectiveImage.tStart = t
                detectiveImage.frameNStart = frameN  # exact frame index
                detectiveImage.setAutoDraw(True)

            if t >= 0.0 and textBox.status == NOT_STARTED:
                # keep track of start time/frame for later
                textBox.tStart = t
                textBox.frameNStart = frameN  # exact frame index
                textBox.setAutoDraw(True)

            # *key_resp_2* updates
            if t >= 0.0 and key_resp_2.status == NOT_STARTED:
                # keep track of start time/frame for later
                key_resp_2.tStart = t
                key_resp_2.frameNStart = frameN  # exact frame index
                key_resp_2.status = STARTED
                # keyboard checking is just starting
                win.callOnFlip(key_resp_2.clock.reset)  # t=0 on next screen flip
                event.clearEvents(eventType='keyboard')
            if key_resp_2.status == STARTED:
                theseKeys = event.getKeys(keyList=respKeyList)

                # check for quit:
                if "escape" in theseKeys:
                    endExpNow = True
                if len(theseKeys) > 0:  # at least one key was pressed
                    key_resp_2.keys = theseKeys[-1]  # just the last key pressed
                    key_resp_2.rt = key_resp_2.clock.getTime()
                    # was this 'correct'?
                    if (key_resp_2.keys == str(brokenSeq)) or (key_resp_2.keys == brokenSeq):
                        key_resp_2.corr = 1
                    else:
                        key_resp_2.corr = 0
                    # a response ends the routine
                    continueRoutine = False

            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in responseComponents:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished

            # check for quit (the Esc key)
            if endExpNow or event.getKeys(keyList=["escape"]):
                core.quit()

            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()

        # -------Ending Routine "response"-------
        for thisComponent in responseComponents:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # check responses
        if key_resp_2.keys in ['', [], None]:  # No response was made
            key_resp_2.keys=None
            # was no response the correct answer?!
            if str(seqBroken).lower() == 'none':
               key_resp_2.corr = 1  # correct non-response
            else:
               key_resp_2.corr = 0  # failed to respond (incorrectly)
        # store data for trials (TrialHandler)
        trials.addData('key_resp_2.keys',key_resp_2.keys)
        trials.addData('key_resp_2.corr', key_resp_2.corr)
        if key_resp_2.keys != None:  # we had a response
            trials.addData('key_resp_2.rt', key_resp_2.rt)
        # the Routine "response" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        thisExp.nextEntry()
        
    if RecConn:
        s.send("P")


# Setup the Window
win = visual.Window(
    size=(1280, 1024), fullscr=True, screen=0,
    allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True)
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# Initialize components for Penguin Routine
penguinClock = core.Clock()
detectiveImage = visual.ImageStim(
    win=win, name='detectiveImage',
    image=u'images/detective_penguin.png', mask=None,
    ori=0, pos=(0, -0.5), size=(0.30, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
speechImage = visual.ImageStim(
    win=win, name = 'speechImage',
    image='images/speechBubble.png', mask=None,
    ori=0, pos=(0,0), size=(1, 1),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
textBox = visual.TextStim(win=win,
    name='textBox',
    text='Default text',
    font='Arial',
    pos=(0, 0.05), height=0.04, wrapWidth=0.4, ori=0,
    color='black', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for trials
stimTrialClock = core.Clock()
s1_o1 = visual.ImageStim(
    win=win, name='s1_o1',
    image='sin', mask=None,
    ori=0, pos=[0,0], size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)
s1_o2 = visual.ImageStim(
    win=win, name='s1_o2',
    image='sin', mask=None,
    ori=0, pos=[0,0], size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-1.0)
s2_o1 = visual.ImageStim(
    win=win, name='s2_o1',
    image='sin', mask=None,
    ori=0, pos=[0,0], size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-2.0)
s2_o2 = visual.ImageStim(
    win=win, name='s2_o2',
    image='sin', mask=None,
    ori=0, pos=[0,0], size=(0.5, 0.5),
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=-3.0)

# Will need text and sound stims for Linguistic task
stimText1 = visual.TextStim(win=win,
    name='textStim1',
    text='Default text',
    font='Arial',
    pos=(0, 0), height=0.15, wrapWidth=1, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

stimText2 = visual.TextStim(win=win,
    name='textStim2',
    text='Default text',
    font='Arial',
    pos=(0, 0), height=0.15, wrapWidth=1, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

stimSound1 = sound.Sound('A', secs=-1)
stimSound1.setVolume(1)

stimSound2 = sound.Sound('B', secs=-1)
stimSound2.setVolume(1)

# Initialize components for Routine "feedback"
feedbackClock = core.Clock()
star1 = visual.ImageStim(
    win=win, name='star1',
    image='images/Starry star.png', mask=None,
    color=[1,1,1], colorSpace='rgb', opacity=1,
    flipHoriz=False, flipVert=False,
    texRes=128, interpolate=True, depth=0.0)

Fixation = visual.TextStim(win=win, name='stimFix',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.15, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);
    
Blank = visual.TextStim(win=win, name='Blank',
    text='',
    font='Arial',
    pos=(0, 0), height=0.2, wrapWidth=None, ori=0,
    color='white', colorSpace='rgb', opacity=1,
    depth=0.0);

# Initialize components for Routine "response"
responseClock = core.Clock()

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine

if RecConn:
    s.send("2" + expName)
    s.send("3" + expInfo['participant'])

displayPenguin(inst.startGames)

for i in inst.introText:
    displayPenguin(i)

# Visual task
#schubotzRoutine('visual', 'trialList_V.csv', 1)

# RS1
#restingState(inst.RSEO, RSEO)

#displayPenguin(inst.nextBlock)

# Control task
#schubotzRoutine('control', 'trialList_C.csv', 2)

# RS2
#restingState(inst.RSEC, RSEC)

#displayPenguin(inst.nextBlock)

# Temporal task
#schubotzRoutine('temporal', 'trialList_T.csv', 3)

# RS3
#restingState(inst.RSEO, RSEO)

# Start Break
#displayPenguin(inst.breakTime)

# End Break
#displayPenguin(inst.startGames)

# RS4
#restingState(inst.RSEC, RSEC)

#displayPenguin(inst.nextBlock)

# Motor task
#motorRoutine('motor', 'trialList_M.csv', 4)

# RS5
#restingState(inst.RSEO, RSEO)

#displayPenguin(inst.nextBlock)

# Linguistic task
#linguisticRoutine('linguistic', 'trialList_L.csv', 5)

# RS6
restingState(inst.RSEC, RSEC)

displayPenguin(inst.nextBlock)

# Spatial task
schubotzRoutine('spatial', 'trialList_S.csv', 6)

displayPenguin(inst.finishedStudy)

if RecConn:
    s.send("Q")
    s.close()

#thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()
