#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Title: Reconsolidation 'finger tapping' sequence learning task [replication of Walker et al. 2003]
Author: Tom Hardwicke, UCL
Last edit date: 14/04/2014

"""

# import useful modules
import time
import pandas as pd
import numpy as np
import sys
import os
from psychopy import visual, event, core, gui, data
from pyglet.window import key
from num2words import num2words

os.chdir(os.path.abspath(''))  # change working directory to script directory
globalClock = core.Clock()  # create timer to track the time since experiment started

### set up some useful routines ###

# A routine to save messages to a log file recording everything the exp is doing
def saveToLog(logString, timeStamp=1):
    f = open(logFile, 'a')  # open our log file in append mode so don't overwrite with each new log
    f.write(logString)  # write the string they typed
    if timeStamp != 0:  # if timestamp has not been turned off
        f.write('// logged at %iseconds' % globalClock.getTime())  # write a timestamp (very coarse)
    f.write('\n')  # create new line
    f.close()  # close and "save" the log file

# An exit routine to initiate if escape is pressed
def quitExp():
    if 'logFile' in globals():  # if a log file has been created
        saveToLog('User aborted experiment')
    if 'win' in globals():  # if a window has been created
        win.close()  # close the window
    core.quit()  # quit the program

# Finger tapping task routine
def fingerTapping(trials, targetSequence, store, sequenceType, sessionType):
    ## Intro screen ##
    saveToLog('Presenting introduction screen') # save info to log
    win.setColor('#000000')  # set background colour to black
    win.flip()  # display
    generalText.setText(
        'Place the fingers of your LEFT hand on the keys 1, 2, 3, and 4. You will be shown a string of 5 digits %(sequence)s, and the computer will start counting down until you start. \n\nOnce the countdown has completed and the screen turns green, type %(sequence)s over and over as quickly as you can. Try not to make errors, but overall you should emphasise speed over accuracy. \n\nYou will have 30 seconds to type %(sequence)s as many times as possible. Stop when the screen turns red again. You will get 30 seconds to rest before the next trial. \n\nPress the spacebar when you are ready for the countdown to begin.' % {'sequence': targetSequence})
    generalText.draw()
    win.flip()  # display
    event.waitKeys(keyList=["space"])  # wait for a spacebar press before continuing
    event.clearEvents()  # clear the event buffer

    win.flip()  # blank the screen first
    trials = range(1, trials + 1)
    saveToLog('Running finger tapping task. %i trials with target sequence %s' % (
        len(trials), targetSequence))  # save info to log

    for thisTrial in trials:

        # begin rest block
        win.setColor('#ff0000')  # set background colour to red
        win.flip()  # display
        if thisTrial == 1:  # if this is first trial
            restClock = core.CountdownTimer(10) # start timer counting down from 10
        else:  # for all other trials
            saveToLog('Resting')  # save info to log
            restClock = core.CountdownTimer(30)  # start timer counting down from 30
        sequenceText.setText(targetSequence)  # set up sequence text
        sequenceText.setAutoDraw(True)  # display sequence text continuously
        timerText.setAutoDraw(True)  #  display timer text continuously
        win.flip()  # display
        while restClock.getTime() > 0:  # loop continues until trial timer ends
            count = restClock.getTime()  # get current time from clock
            timerText.setText(num2words(np.ceil(count)))  # set timer text to the current time
            win.flip()  # display
            if event.getKeys(['escape']):  # checks for the key 'escape' on every refresh so user can quit at any point
                quitExp()  # initiate quit routine

        # begin tapping
        saveToLog('Trial: %i' % thisTrial) # save info to log
        win.setColor('#89ba00')  # set background colour to green
        win.flip()  # display
        stream = []  # clear any existing response stream info
        event.clearEvents()  # this makes sure the key buffer is cleared, otherwise old key presses might be recorded
        trialClock = core.CountdownTimer(30)  # start timer counting down from 30
        timerText.setText('Tap as fast as you can!')  # set timer text to the current time
        win.flip()  # display

        k = 0  # set up marker index
        endTrial = False  # a trigger to end the trial (deployed when the timer runs out)
        while endTrial == False:  # while trigger has not been deployed
            # display incremental markers across the screen from left to right as the user presses accepted keys
            if k == 0:  # start at beginning of marker index
                # start markers incrementing from left to right
                while k < len(
                        listOfMarkers) - 1 and endTrial == False:  # until the markers reach the far side of the screen
                    if trialClock.getTime() <= 0:  # if timer has run out
                        endTrial = True  # deploy the trigger to end the trial
                        break  # and break out of this loop
                    elif event.getKeys(['escape']):  # if user presses escape key
                        quitExp()  # quit the program
                    elif event.getKeys('1'):  # checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(True)  # turn this marker on
                        win.flip()  # display
                        stream.append(1)  # record the key press
                        k += 1  # move on to the next marker
                    elif event.getKeys('2'):  # checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(True)  # turn this marker on
                        win.flip()  # display
                        stream.append(2)  # record the key press
                        k += 1  # move on to the next marker
                    elif event.getKeys('3'):  # checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(True)  # turn this marker on
                        win.flip()  # display
                        stream.append(3)  # record the key press
                        k += 1  # move on to the next marker
                    elif event.getKeys('4'):  # checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(True)  # turn this marker on
                        win.flip()  # display
                        stream.append(4)  # record the key press
                        k += 1  # move on to the next marker


            elif k == len(listOfMarkers) - 1 and endTrial == False:
                # start going down
                while k > 0:
                    if trialClock.getTime() <= 0:  # if timer has run out
                        endTrial = True  # deploy the trigger to end the trial
                        break  # and break out of this loop
                    elif event.getKeys(['escape']):   # if user presses escape key
                        quitExp()  # quit the program
                    elif event.getKeys('1'):  # checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(False)  # turn this marker off
                        win.flip()  # display contents of video buffer
                        stream.append(1)  # record the key press
                        k -= 1  # move on to the next marker
                    elif event.getKeys('2'): #checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(False)  # turn this marker off
                        win.flip()  # display contents of video buffer
                        stream.append(2)  # record the key press
                        k -= 1  # move on to the next marker
                    elif event.getKeys('3'): #checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(False)  # turn this marker off
                        win.flip()  # display contents of video buffer
                        stream.append(3)  # record the key press
                        k -= 1  # move on to the next marker
                    elif event.getKeys('4'): #checks for key on every refresh
                        listOfMarkers[k].setAutoDraw(False)  # turn this marker off
                        win.flip()  # display contents of video buffer
                        stream.append(4)  # record the key press
                        k -= 1  # move on to the next marker

        # turn off all markers during the rest block
        for marker in listOfMarkers:  # for each marker
            marker.setAutoDraw(False)  # turn off

        win.setColor('#ff0000')  # set background colour to red
        win.flip()  # display

        if not metaData['practice mode']:  # if it is not practice mode

            output = patternDetect(stream, targetSequence)  # run the pattern detector to calculate speed and errors

            #  gather all relevant data for this trial
            newRow = {'participant': participant,
                      'session': sessionType,
                      'targetSequence': targetSequence,
                      'sequenceType': sequenceType,
                      'trial': thisTrial,
                      'stream': stream,
                      'speed': output['speed'],
                      'errors': output['errors'],
                      'accuracy': output['accuracy']}

            # record data in store
            store = store.append(newRow, ignore_index=True)

    sequenceText.setAutoDraw(False)  # turn off the sequence text
    timerText.setAutoDraw(False)  # turn off the timer text
    win.flip()  # display

    return store

# Routine for analysing the response stream
def patternDetect(stream, targetSequence):
    # pre-load some variables
    targetSequence = map(int, list(targetSequence))
    stream = list(stream)
    speed = float(0) # store for complete sequences(i.e. speed)
    contiguousError = 0 # store for contiguous incorrect items
    errors = float(0) # store for errors
    i = 0  # start at position 1

    # start pattern detector

    while i < len(stream):  # search through every item in stream

        # for all expect final items (which are anything less than a whole sequence at the end of the stream)
        if i <= len(stream) - len(targetSequence):

            # if the next sequence length of items in the stream matches the target sequence
            if stream[i:(i + len(targetSequence))] == targetSequence:

                speed += 1  # record a pattern completed
                i += len(targetSequence)  # adjust position to skip forward by length of targetSequence

                # CHECK ERRORS need to reset contiguous error counter and add any accumulated errors to the total count
                if contiguousError >= 1:  # check if there are contiguous errors we have not yet accounted for

                    errors += 1 # add an error to the total count
                    contiguousError = 0 # reset contiguous error count

            # else if the next sequence length of items in the stream does not match the target sequence
            elif stream[i:(i + len(targetSequence))] != targetSequence:

                contiguousError += 1  # record a 'contiguous error'
                i += 1  # adjust index forward by 1

                # CHECK ERRORS when contiguous error count reaches 5 or if this is the final item of the stream
                if contiguousError == 5 or i == len(stream):
                    errors += 1 # add an error to the total count
                    contiguousError = 0 # reset contiguous error count
        # now deal with last items of the stream (a special case, see 'method' above)
        else:

            # get last items
            lastItems = stream[i:]

            # get subset of target sequence of same length as last items
            sequenceSubset = targetSequence[:len(lastItems)]

            while lastItems != None:  # while there are additional items left to check

                if lastItems == sequenceSubset:  # if lastItems match target sequence subset

                    speed += float(len(lastItems)) / float(len(targetSequence))  # record fractional sequence

                    if contiguousError >= 1:  # check if there are errors we have not yet recorded

                        errors += 1  # add an error to total

                        contiguousError = 0  # reset contiguous error count

                    lastItems = None  # force failure of inner while loop by updating lastItems

                    i = len(stream)  # force failure of outer while loop by updating i

                else:  # if lastItems do not match target sequence

                    contiguousError += 1  # add 1 to contiguous error count

                    # when contiguous error count reaches 5 or if this is final item
                    if contiguousError == 5 or len(lastItems) == 1:
                        errors += 1  # add an error to total
                        contiguousError = 0  # reset contiguous error count

                    if len(lastItems) == 1:  # if this is the final item

                        lastItems = None  # force failure of inner while loop by updating lastItems

                        i = len(stream)  # force failure of outer while loop by updating i

                    else:  # else if there are still items left to check

                        lastItems = lastItems[1:]  # drop the first item from lastItems

                        sequenceSubset = sequenceSubset[:-1]  # drop the last item from the sequence subset

    # integrity check
    if speed == 0:
        print('Issue with this stream - speed is zero')
        accuracy = float('nan')
    else:
        accuracy = 1 - errors / speed  # calculate accuracy

    return {'speed': speed, 'errors': errors, 'accuracy': accuracy}

### Collect and store meta-data about the experiment session ###
expName = 'Sequence learning task'  # define experiment name
date = time.strftime("%d %b %Y %H:%M:%S", time.localtime())  # get date and time
metaData = {'participant': '',
            'practice mode': False,
            'override automated counter-balancing': False,
            'researcher': 'TH',
            'location': '204F, UCL, London'}  # set up info for infoBox gui
infoBox = gui.DlgFromDict(dictionary=metaData,
                          title=expName,
                          order=['participant', 'practice mode','override automated counter-balancing'])  # display gui to get info from user
if not infoBox.OK:  # if user hit cancel
    quitExp()  # quit




if not metaData['practice mode']:  # if this is not practice mode:
    participant = metaData['participant']
    fileName = 'data' + os.path.sep + 'P%s.csv' % (participant)  # build filename for this participant's data

    # is this an existing participant? If so we will read in their existing files and identify the next session
    if os.path.exists(fileName):  # if existing participant, read in existing store

        store = pd.read_csv(fileName,
                            usecols=['participant', 'session', 'targetSequence', 'sequenceType', 'trial', 'stream',
                                     'speed',
                                     'errors', 'accuracy'])

        # get last session and increment by one
        session = int(store['session'].irow(-1)[0]) + 1

        # check user knows this is an existing participant
        myDlg = gui.Dlg()
        myDlg.addText(
            "This participant has existing files in the directory! Click ok to continue with session %i or cancel to abort." %session)
        myDlg.show()  # show dialog and wait for OK or Cancel
        if not myDlg.OK:  # if the user pressed cancel
            quitExp()

        if session > 3:
            myDlg = gui.Dlg()
            myDlg.addText('This participant has already completed 3 sessions - are you sure you want to run more?')
            myDlg.show()  # show dialog and wait for OK or Cancel
            if not myDlg.OK:  # if the user pressed cancel
                quitExp()

    else:  # if this is a new participant set up new store

        # set up a new data store
        store = pd.DataFrame(
            columns=['participant', 'session', 'targetSequence', 'sequenceType', 'trial', 'stream', 'speed', 'errors',
                     'accuracy'])

        # designate as first session
        session = 1

        # collect some demographic details about the user

        metaData2 = {'age': '', 'gender': ['male', 'female']}
        infoBox = gui.DlgFromDict(dictionary=metaData2, title='Additional participant details', order=['age', 'gender'])
        if infoBox.OK:  # this will be True (user hit OK) or False (cancelled)
            metaData.update(metaData2) # add new metaData to existing metaData
        else:
            sys.exit("User cancelled gui.")

    # set up counterbalancing
    if metaData['override automated counter-balancing'] == True:  # user has chosen to override automated counter-balancing
        cb = {'sequenceOrder': ['X', 'Y'], 'testOrder': ['A', 'B']}  # set up info for infoBox gui
        infoBox = gui.DlgFromDict(dictionary=cb,
                                  title='Choose counter-balancing parameters')  # display gui to get info from user
        sequenceOrder = cb['sequenceOrder']
        testOrder = cb['testOrder']
        if not infoBox.OK:  # if user hit cancel
            quitExp()  # quit
    else:  # otherwise use automated counter-balancing
        trialList = data.createFactorialTrialList(
            {'sequenceOrder': ['X', 'Y'], 'testOrder': ['A', 'B']}) # get counter balancing conditions
        # assign to counter-balanced conditions [the 4 unique arrangements are assigned cyclically]
        sequenceOrder = trialList[int(metaData['participant']) % 4]['sequenceOrder']
        testOrder = trialList[int(metaData['participant']) % 4]['testOrder']

    metaData.update({'expName': expName, 'date': date, 'session': session, 'sequenceOrder': sequenceOrder,
                     'testOrder': testOrder})  # record the counterbalancing info in the metaData

    # Customise sequences for this participant
    if sequenceOrder == 'X':
        oldSequence = '41324'
        newSequence = '23142'
    elif sequenceOrder == 'Y':
        oldSequence = '23142'
        newSequence = '41324'

    # set up filename for saving log, each P and S saved as separate file
    logFile = 'data' + os.path.sep + 'P' + str(metaData['participant']) + 'S' + str(metaData['session']) + '_log.txt'

    # check if a previous log exists with this name and if it does ask user to resolve before continuing
    while os.path.exists(logFile):
        myDlg = gui.Dlg()
        myDlg.addText(
            "There is already a log file stored for this participant/session - please resolve before continuing.")
        myDlg.show()  # show dialog and wait for OK or Cancel
        if not myDlg.OK:  # if the user pressed cancel
            quitExp()


    # save metaData to log
    saveToLog('experiment: %s' % (metaData['expName']), 0)
    saveToLog('researcher: %s' % (metaData['researcher']), 0)
    saveToLog('location: %s' % (metaData['location']), 0)
    saveToLog('date: %s' % (metaData['date']), 0)
    saveToLog('participant: %s' % (metaData['participant']), 0)
    if session==1:
        saveToLog('gender: %s' % (metaData['gender']), 0)
        saveToLog('age: %s' % (metaData['age']), 0)
    saveToLog('session: %s' % (metaData['session']), 0)
    saveToLog('sequence Order:%s' % (metaData['sequenceOrder']), 0)
    saveToLog('testOrder: %s' % (metaData['testOrder']), 0)
    saveToLog('..........................................', 0)
else:  # if it is practice mode
    # set up practice log file
    logFile = 'data' + os.path.sep + 'practice_log.txt'

### Prepare stimuli etc ###
win = visual.Window(size=(1280, 1024), fullscr=True, screen=0, allowGUI=False, allowStencil=False,
                    monitor='testMonitor', color='black', colorSpace='rgb', units='pix') # setup the Window
generalText = visual.TextStim(win=win, ori=0, name='generalText', text='', font=u'Arial', pos=[0, 0], height=35,
                              wrapWidth=920, color=u'white', colorSpace=u'rgb', opacity=1, depth=0.0)  # general text
sequenceText = visual.TextStim(win=win, ori=0, name='sequenceText', text='', font=u'Arial', pos=[0, 250], height=90,
                               wrapWidth=None, color=u'white', colorSpace=u'rgb', opacity=1, depth=0.0)  # sequence text
timerText = visual.TextStim(win=win, ori=0, name='sequenceText', text='', font=u'Arial', pos=[0, -130], height=40,
                            wrapWidth=800, color=u'white', colorSpace=u'rgb', opacity=1, depth=0.0)  # timer text

# set up the markers that increment across the screen - generate enough so that they cover the full range of the window
listOfMarkers = []  # store for white markers
windowSize = list(win.size) # get window size
for i in range(-windowSize[0] / 2, windowSize[0] / 2, windowSize[0] / 40):  # generate markers to cover whole screen
    i += 25  # add a slight horizontal adjustment to ensure markers do not go off screen
    listOfMarkers.append(visual.Circle(win, radius=15, edges=32, pos=[i, 0], fillColor='white'))  # generate the markers

# for monitoring key state (only need this if using markers)
keys = key.KeyStateHandler()
win.winHandle.push_handlers(keys)

saveToLog('Set up complete') # save info to log
### set-up complete ###

### run the experiment ###

if metaData['practice mode']:  # if user has chosen practice mode
    practiceSequence = '32413'
    fingerTapping(1, practiceSequence, store=[], sequenceType=[], sessionType ='1a')  # run 1 trial of the task with a practice sequence

elif session == 1:
    store = fingerTapping(12, oldSequence, store=store,
                          sequenceType='old', sessionType = '1a')  # run 12 trials of the task with the old sequence

elif session == 2:
    store = fingerTapping(3, oldSequence, store=store,
                          sequenceType='old', sessionType = '2a')  # run 3 trials of the task with the old sequence
    store = fingerTapping(12, newSequence, store=store,
                          sequenceType='new', sessionType = '2b')  # run 12 trials of the task with the new sequence

elif session == 3:
    if testOrder == 'A':
        store = fingerTapping(3, oldSequence, store=store,
                              sequenceType='old', sessionType = '3a')  # run 3 trials of the task with the old sequence
        store = fingerTapping(3, newSequence, store=store,
                              sequenceType='new', sessionType = '3b')  # run 3 trials of the task with the new sequence

    elif testOrder == 'B':
        store = fingerTapping(3, newSequence, store=store,
                              sequenceType='new', sessionType = '3a')  # run 3 trials of the task with the new sequence

        store = fingerTapping(3, oldSequence, store=store,
                              sequenceType='old', sessionType = '3b')  # run 3 trials of the task with the old sequence

## End screen ##
saveToLog('Presenting end screen')  # save info to log
win.setColor('#000000')  # set background colour to black
win.flip()
generalText.setText(u'Thank you. That is the end of this section. Please inform the researcher you have finished.')
generalText.draw()
win.flip()  # present video buffer
event.waitKeys() # wait for a key press before continuing
event.clearEvents() # clear the event buffer

saveToLog('Experiment presentation over')  # save info to log
### Finished running the experiment ###

if metaData['practice mode']:  # if user has chosen practice mode
    quitExp()  # quit

### Save and clean up ###

win.close()

# save the data as a csv file
# the loop below also checks if saving is not possible, usually because the file is already open, and asks user to close if this is the case
# if this does not resolve the situation, attempt is made to save the data with a different filename
while True:
    try:
        store.to_csv(fileName)
        saveToLog('Data saved with file name: %s' % fileName) # save info to log
        break
    except: # if cannot save data, likely because file is already open, ask user to close
        saveToLog('Problem encountered saving data - requesting user close open data files...') # save info to log
        myDlg = gui.Dlg()
        myDlg.addText(
                "Unable to store data. Try closing open excel files and then click ok. Press cancel to attempt data storage to new file.")
        myDlg.show()  # show dialog and wait for OK or Cancel
        if not myDlg.OK:  # if the user pressed cancel
            fileName = 'data' + os.path.sep + 'P%s_problemSaving.csv' % (participant)  # build filename for this participant's data
            saveToLog('Attempting to save data with different filename: %s' %fileName) # save info to log
            try:
                store.to_csv(fileName)
                print('Data was saved with a different filename: %s' %fileName)
                saveToLog('Data saved with file name: %s' % fileName) # save info to log
                break
            except:
                saveToLog('Major error: Data could not be saved') # save info to log
                quitExp() # quit the experiment

t = globalClock.getTime() # get run time of experiment
saveToLog('Total experiment runtime was %i seconds' % t) # record runtime to log

# Shut down:
core.quit()