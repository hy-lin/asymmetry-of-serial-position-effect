'''
Created on 10.11.2015
Simplified class for data analysis

@author: Hsuan-Yu Lin
'''

import numpy

class Stimulus(object):
    def __init__(self, word_index, serial_position):
        self.word_index = word_index
        self.serial_position = serial_position

    def __str__(self):
        return '{}'.format(self.word_index)
    
    def __eq__(self, target):
        if target.word_index == self.word_index and target.serial_position == self.serial_position:
            return True
        
        return False
    
class Probe(object):
    def __init__(self, probe_type, serial_position, stimulus):
        self.serial_position = serial_position
        self.probe_type = probe_type
        self.stimulus = stimulus
        
    def __str__(self):
        return '{}\t{}\t{}'.format(self.probe_type, self.serial_position, self.stimulus.word_index)
    
class ResponseCandidate(object):
    def __init__(self, stimulus):
        self.stimulus = stimulus
            
    def __str__(self):
        return str(self.stimulus)

class Trial(object):
    def __init__(self, exp_parameters):
        self.exp_parameters = exp_parameters
            
    def isMetConstraints(self, constaints):
        passed = True
        
        for argument in constaints.keys():
            if argument in self.__dict__.keys():
                if self.__dict__[argument] not in constaints[argument]:
                    passed = False
            else:
                passed = False
                
            if not passed:
                break
            
        return passed
    
    def checkCorrectness(self):
        if self.probe_type == 'order': # recall item
#             self.correctness = 'extralist'
            respond_sp = -1
            
            for i, stimulus in enumerate(self.stimulus):
                if stimulus == self.response:
                    respond_sp = i+1
                    
                    
            if respond_sp == self.serial_position:
                self.correctness = 1
            else:
                self.correctness = 0
                
        if self.probe_type == 'item': # recall order
            if self.response * -1 == self.serial_position:
                self.correctness = 1
            else:
                self.correctness = 0
                
        return self.correctness
    

class Participant(object):
    def __init__(self, pID):
        self.pID = pID
        self.trials = []
        
    def addTrial(self, trial):
        self.trials.append(trial)
        
    def getTrialsMetConstraints(self, constraints):
        final_pool = []
        
        for trial in self.trials:
            if trial.isMetConstraints(constraints):
                final_pool.append(trial)
                
        return final_pool