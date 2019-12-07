#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build a trial loop Step 2
Use this template to turn Step 1 into a loop
@author: katherineduncan
"""


#%% Required set up 

import numpy as np
import pandas as pd
import os, sys
import random
from psychopy import visual, core, event, gui, logging



#%% identify who the data belongs to 

# show the dialog box, create a field for subject ID and session number
subgui = gui.Dlg()
subgui.addField("Subject ID:")
subgui.addField("Session Number:")

# show the gui
subgui.show()

# put the inputted data in easy to use variables
subjID = subgui.data[0]
sessNum = subgui.data[1]

# if the file name already exists, give a notification and exit out of the experiment
ouputFileName = 'sub'+subjID+'_'+'sess'+sessNum+'.csv'
if os.path.isfile(ouputFileName) :
    sys.exit("data for this session already exists")



#%% set up study  

# pressing q will quit 
event.globalKeys.add(key='q', func=core.quit)

# open a white full screen window
win = visual.Window(fullscr=True, allowGUI=False, color='white', unit='height') 

# a list called "stim" that contains trial-specific info (stimulus, etc)
stim = ['A','B','C','D','F','G','H','J','K','L','M','N','P','Q','R','S','T','U','W','X','Y','Z']

# randomly shuffle the stimuli so the order is no predictable 
random.shuffle(stim)

#define the number of stimuli
nstim = len(stim)

# read in experiment info - indicates what is the correct response for each letter stimulus
trialInfo = pd.read_csv('letterConds.csv')

# components for the stimulus display 
myTextquestion = visual.TextStim(win, text="Was this letter on the study list?", pos = (0,0.5), color="black") 
myTextF = visual.TextStim(win, text="f = yes", pos = (-0.25,-0.5), color="black") 
myTextJ = visual.TextStim(win, text="j = no", pos = (0.25,-0.5), color="black") 

# feedback display
corFeedback = visual.TextStim(win, text='correct!', pos=(0,0), color="black")
incFeedback = visual.TextStim(win, text='wrong!', pos=(0,0), color="black")

# fixation display 
fixation = visual.TextStim(win, text="+", color="black")

# output pandas dataframe 
out = pd.DataFrame(columns=['trial','response','rt','correct'])

# define sum_acc, sum_rt, and num_trials for generating summary statistics 
sum_acc = 0 
sum_rt = 0  
num_trials = 0 



#%% task instructions before starting the loop 

instructions = visual.ImageStim(win, image='instructions.jpg', pos=(0,0), size=(1.5,1.5)) 
instructions.draw()
win.flip()
event.waitKeys(keyList=['f'])



#%% my loop here

for trial in np.arange(nstim): 
    num_trials += 1
    thisStimName = stim[trial] # index the items in the stimulus list 
    
    # define the stimuli and text to use for the experiment 
    thisStim = visual.ImageStim(win, image='letters'+'/'+ thisStimName + '.jpg', pos=(0,0), size=(1.5,1.5)) # give path to stimulus (using thisStimName)
    
    # draw the text and the stimulus 
    thisStim.draw() 
    myTextquestion.draw()
    myTextF.draw()
    myTextJ.draw()
    
    # flip it
    win.flip()
    
    # define the clock to record time
    trialClock = core.Clock()

    # define which keys are valid responses and record the amount of time it takes to make a response 
    keys = event.waitKeys(keyList=['f','j'], timeStamped=trialClock)
    thisRT = keys[0][1]
    
    # reset the trial clock 
    trialClock.reset()
    
    # PROVIDE FEEDBACK
     
    # compare the participant's key response to the correct key response for that stimulus 
    # if they are the same, the response is correct 
    # if they are different, the response is wrong 
    filtered = trialInfo.loc[trialInfo['letter'] == thisStimName]
    
    if keys[0][0] == 'j' and (filtered.corr_resp == 'j').any(): 
        out.loc[trial,'correct'] = 1 # save the accuracy information to the output file, 1 is correct, 0 is incorrect
        corFeedback.draw()
    elif keys[0][0] == 'f' and (filtered.corr_resp == 'f').any(): 
        out.loc[trial,'correct'] = 1
        corFeedback.draw()
    else:
        out.loc[trial,'correct'] = 0
        incFeedback.draw()
    win.flip()
    core.wait(1)
    
    # print out of rt and acc on each trial, so the experimenter can get a sense of participant performance 
    sum_rt +=  thisRT
    sum_acc += out.correct[trial]
    print('rt:',round(thisRT,2),'sec',',','correct:',out.correct[trial])  
    
    #record relevant trial info & save it to a csv file 
    out.loc[trial,'trial'] = trial+1
    out.loc[trial,'response'] = keys[0][0]
    out.loc[trial,'rt'] = keys[0][1]
    out.loc[[trial]].to_csv(ouputFileName,mode='a',header=False,index=False)
    
    # clear the events
    event.clearEvents()  
    
    # show a fixation after each letter stimulus 
    fixation.draw()
    win.flip()


core.wait(1)
win.close()


#%% print participant's average RT and accuracy to get a sense of performance 

print('mean rt:', round(sum_rt/num_trials,2),'sec',',','mean acc:',sum_acc/num_trials*100,'%') 



