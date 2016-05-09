# coding= latin-1
'''
Created on 15.10.2015

@author: Hsuan-Yu Lin
'''
import Display
import ExpParameters
import Recorder
import myClasses
import os
os.environ['PYSDL2_DLL_PATH'] = 'sdl_dll\\'
import sdl2.ext
import random
import numpy
import datetime

class Experiment(object):
    def __init__(self):
        self.data_file = open('Data\\probedrecallNcontextrecall2b.dat', 'a', 0)
        self.logger = open('Data\\log.dat', 'a', 0)
        
        self.exp_parameters = ExpParameters.ExpParameters()
        self.resources = sdl2.ext.Resources('.', 'resources')
        self.display = Display.Display(self.resources, self.exp_parameters)
        self.recorder = Recorder.Recorder(self.exp_parameters)
        self.exp_parameters.updateDisplayScale(self.display)
        self.exp_parameters.loadWordList(self.resources)
        
        self.pID = 999
        self.session = 1
        
        self.avaliable_pool = range(self.exp_parameters.word_n)
        
        self._setupPracticeTrials()
        self._setupExperimentTrials()
        
        self.log('experiment created.')
    
    def log(self, msg):
        current_time = datetime.datetime.now()
        time_str = current_time.strftime('%d-%b-%Y %I-%M-%S')
        
        self.logger.write('{}\t{}\n'.format(time_str, msg))
        
    def _saveTrial(self, tInd, trial):
        for i in range(trial.exp_parameters.set_size):
            output_line = trial.getSaveString(i)
            output_line = '{}\t{}\t{}\t{}\t{}\n'.format(self.pID, self.session, tInd, i, output_line)
            print output_line
            
            self.data_file.write(output_line)
            
        self.log('saved trial {}.'.format(tInd))
    
    def _getPIDNSession(self):
        pID = self.display.getString(self.recorder, 'Participant ID: ', 20, 20)
        session = self.display.getString(self.recorder, 'Session: ', 20, 20)
        
        self.pID = pID
        self.session = session
    
    def _testRun(self):
        avaliable_pool = range(15)
        trials = []
        context_recall = myClasses.ContextRecallTrial(avaliable_pool, self.exp_parameters, self.display)
        context_recall.createProbe(2)
        trials.append(context_recall)
        
        avaliable_pool = range(15)
        probed_recall = myClasses.ProbedRecallTrial(avaliable_pool, self.exp_parameters, self.display)
        probed_recall.createProbe(2)
        trials.append(probed_recall)
        
        for trial in trials:
            trial.displayTrial()
            trial.getResponse(self.recorder)
            print trial.getSaveString()
            
    def _checkNResetPool(self):
        if len(self.avaliable_pool) < self.exp_parameters.n_recall_candidate:
            self.avaliable_pool = range(self.exp_parameters.word_n)
            self.log('pool reseted')
    
    def _setupPracticeTrials(self):
        trial_types = ['content', 'context']
        conditions = [trial_type for trial_type in trial_types for rep in range(self.exp_parameters.n_practice_rep)]
        numpy.random.shuffle(conditions)
        
        self.practice_trials = []

        for condition in conditions:
            trial_type = condition
            if trial_type == 'content':
                probed_recall = myClasses.ProbedRecallTrial(self.avaliable_pool, self.exp_parameters, self.display)
                probed_recall.createProbe()
                
                self.practice_trials.append(probed_recall)
            elif trial_type == 'context':
                context_recall = myClasses.ContextRecallTrial(self.avaliable_pool, self.exp_parameters, self.display)
                context_recall.createProbe()
                
                self.practice_trials.append(context_recall)
            else:
                print 'Unexpected trial type: {} while creating trials.'.format(type)
                raise(ValueError)
            
            self._checkNResetPool()
            
    def _setupExperimentTrials(self):
        trial_types = ['content', 'context']
        conditions = [trial_type for trial_type in trial_types for rep in range(self.exp_parameters.n_experiment_rep)]
        numpy.random.shuffle(conditions)
        
        self.experiment_trials = []

        for condition in conditions:
            trial_type = condition
            if trial_type == 'content':
                probed_recall = myClasses.ProbedRecallTrial(self.avaliable_pool, self.exp_parameters, self.display)
                probed_recall.createProbe()
                
                self.experiment_trials.append(probed_recall)
            elif trial_type == 'context':
                context_recall = myClasses.ContextRecallTrial(self.avaliable_pool, self.exp_parameters, self.display)
                context_recall.createProbe()
                
                self.experiment_trials.append(context_recall)
            else:
                print 'Unexpected trial type: {} while creating trials.'.format(type)
                raise(ValueError)
            
            self._checkNResetPool()
            
    def _runPractice(self):
        self.log('beginning practice trials:')
        
        self.display.clear()
        self.display.drawText(u'Mit Leertaste weiter zu den Übungsaufgaben')
        self.display.refresh()
        self.recorder.recordKeyboard(['space'])
        self.recorder.hideCursor()
        
        for tInd, trial in enumerate(self.practice_trials):
            self.log('presenting practice trial {}.'.format(tInd))
            self.display.wait(1000)
            trial.displayEncoding()
            
            self.recorder.showCursor()
            for i in range(trial.exp_parameters.set_size):
                trial.displayTesting(i)
                trial.getResponse(i, self.recorder)
                
                print trial.getSaveString(i)
                
            self.recorder.hideCursor()
            self.display.clear(refresh = True)
            
            
    def _runExperiment(self):
        self.log('beginning trials:')
        
        self.display.clear()
        self.display.drawText(u'Mit Leertaste weiter zu den Testaufgaben')
        self.display.refresh()
        self.recorder.recordKeyboard(['space'])
        self.display.clear(refresh = True)
        
        for tInd, trial in enumerate(self.experiment_trials):
            self.log('presenting experiment trial {}.'.format(tInd))
            self.display.wait(1000)
            trial.displayEncoding()
            
            self.recorder.showCursor()
            for i in range(trial.exp_parameters.set_size):
                trial.displayTesting(i)
                trial.getResponse(i, self.recorder)
            
            self._saveTrial(tInd, trial)
            
            self.display.clear(refresh = True)
            
            if tInd % (len(self.experiment_trials) / self.exp_parameters.n_breaks) == 0 and tInd != 0:
                self._takingBreak()
                
    def _endOfExperiment(self):
        self.log('experiment finished, closing files.')
        self.data_file.close()
        
        self.display.clear()
        self.display.drawText(u'Ende des Experiments: Bitte Versuchsleiter rufen')
        self.display.refresh()
        self.recorder.recordKeyboard(['space'])
        
        self.log('exiting program.')
        self.logger.close()
    
    def _takingBreak(self):
        self.log('taking a break')
        
        self.display.clear()
        self.display.drawText(u'Gelegenheit für kurze Pause. Weiter mit Leertaste')
        self.display.refresh()
        self.recorder.recordKeyboard(['space'])
        self.display.clear(refresh = True)
        
    def run(self):
        self._getPIDNSession()
        self._runPractice()
        self._runExperiment()
        self._endOfExperiment()

if __name__ == '__main__':
    experiment = Experiment()
    experiment.run()
    pass