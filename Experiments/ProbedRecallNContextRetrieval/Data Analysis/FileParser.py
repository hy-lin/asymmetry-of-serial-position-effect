'''
Created on 10.11.2015

@author: Hsuan-Yu Lin
'''

import myClasses

class ColumnsDefinition(object):
    def __init__(self):
        self.pID = 0
        self.session = 1
        
        self.tID = 2
        self.stimulus = range(3, 9)
        self.probe_type = 9
        self.sp = 10
        self.probe_item = 11
        self.response = 12

class TrialParser(object):
    '''
    classdocs
    '''

    def __init__(self, columns, exp_parameters):
        '''
        Constructor
        '''
        self.columns = columns
        self.exp_parameters = exp_parameters
        
    def parse(self, line):
        val = line.split()
        
        pID = int(val[self.columns.pID])
#         session = int(val[self.columns.session])
        tID = int(val[self.columns.tID])
        setsize = 6
        
        trial = myClasses.Trial(self.exp_parameters)
        
        stimulus = [int(val[self.columns.stimulus[i]]) for i in range(setsize)]
        trial.stimulus = stimulus
        
        trial.probe_type = val[self.columns.probe_type]
        trial.serial_position = int(int(val[self.columns.sp]))
        trial.probe = int(val[self.columns.probe_item])
        
        trial.response = int(val[self.columns.response])
        
        trial.checkCorrectness()

        return pID, tID, trial

class FileParser(object):
    '''
    This object parses the whole file instead of just one trial
    '''
    
    def __init__(self, columns, exp_parameters):
        self.columns = columns
        self.exp_parameters = exp_parameters
        
    def parse(self, file_handle, ban_list = []):
        '''
        Parse each line of data into a dictionary of participants.
        Return the dictionary which has pID as key, Participant class as content.
        '''
        participants = {}
        trial_parser = TrialParser(self.columns, self.exp_parameters)
        
        for line in file_handle:
            pID, _, trial = trial_parser.parse(line)
            
            if pID in ban_list:
                continue
            
            if pID not in participants.keys():
                participants[pID] = myClasses.Participant(pID)
                
            participants[pID].addTrial(trial)
            
        return participants