'''
Created on 07.10.2015

@author: Hsuan-Yu Lin
'''

import numpy

class Stimulus(object):
    def __init__(self, word_index, exp_parameters):
        self.word_index = word_index
        if word_index >= 0:
            self.word = exp_parameters.word_list[self.word_index]
        else:
            self.word = str(word_index * -1)
        
    def draw(self, display):
        x, y = display.getStimulusCoord()
        display.drawText(self.word, x, y)
        
    def __str__(self):
        return '{}'.format(self.word_index)
    
class Probe(object):
    def __init__(self, probe_type, serial_position, stimulus):
        self.serial_position = serial_position
        self.probe_type = probe_type
        self.stimulus = stimulus
        
    def draw(self, display):
        x, y = display.getProbeCoord()
        display.drawText(self.stimulus.word, x, y)
        
    def __str__(self):
        return '{}\t{}\t{}'.format(self.probe_type, self.serial_position, self.stimulus.word_index)
    
class ResponseCandidate(object):
    def __init__(self, stimulus, position):
        self.stimulus = stimulus
        self.position = position
        
    def isMouseOver(self, mx, my, display):
        x0, y0, x1, y1 = display.getResponseCandidateRect(self.position)
        if x0 < mx < x1 and y0 < my < y1:
            return True
        
        return False
    
    def draw(self, display, mouse_over = False):
        x0, y0, x1, y1 = display.getResponseCandidateRect(self.position)
        display.drawText(self.stimulus.word, (x0+x1)/2, (y0+y1)/2)
        
        if mouse_over:
            display.drawThickFrame(x0, y0, x1, y1, display.exp_parameters.thick_line)
        else:
            display.drawThickFrame(x0, y0, x1, y1, display.exp_parameters.thin_line)
            
    def __str__(self):
        return str(self.stimulus)

class Trial(object):
    def __init__(self, avaliable_pool, exp_parameters, display = None):
        self.exp_parameters = exp_parameters
        self.display = display
        
        self.probes = range(exp_parameters.set_size)
        self.response = range(exp_parameters.set_size)
        
        self._createStimulus(avaliable_pool)
        
    def _createStimulus(self, avaliable_pool):
        self.stimulus = []
        for i in range(self.exp_parameters.set_size):
            picked_index = numpy.random.randint(len(avaliable_pool))
            stimulus = Stimulus(avaliable_pool.pop(picked_index), self.exp_parameters)
            self.stimulus.append(stimulus)
            
    def getSaveString(self, output_index):
        output_line = ''
        for stimulus in self.stimulus:
            output_line += '{}\t'.format(stimulus)
            
        output_line += '{}\t'.format(self.probes[output_index])
        output_line += '{}\t'.format(self.response[output_index])
            
        return output_line
        
 
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
    
    def displayEncoding(self):
        self.display.clear(refresh = True)
        self.display.wait(500)
        
        for stimulus in self.stimulus:
            self.display.clear()
            stimulus.draw(self.display)
            self.display.refresh()
            self.display.wait(500)
            
    def displayTesting(self, output_index):
        self.display.clear()
        self.display.refresh()
        self.display.wait(750)
        
        self.probes[output_index].draw(self.display)
        for candidate in self.response_candidates:
            candidate.draw(self.display)
            
        self.display.refresh()
        
    def getResponse(self, output_index, recorder):
        button = ''
        mouse_overed_candidate = None
        while button != 'left' or mouse_overed_candidate is None:
            self.display.clear()
            x, y, button = recorder.getMouse()
            
            self.probes[output_index].draw(self.display)
            for candidate in self.response_candidates:
                mouse_over = candidate.isMouseOver(x, y, self.display)
                candidate.draw(self.display, mouse_over)
                
            mouse_overed_candidate = None
                
            for candidate in self.response_candidates:
                if candidate.isMouseOver(x, y, self.display):
                    mouse_overed_candidate = candidate
                
            self.display.refresh()
            self.display.waitFPS()
            
        self.response[output_index] = mouse_overed_candidate
    
class ProbedRecallTrial(Trial):
    def __init__(self, avaliable_pool, exp_parameters, display = None):
        super(ProbedRecallTrial, self).__init__(avaliable_pool, exp_parameters, display)
        
        self._createCandidates(avaliable_pool)
        
    def _createCandidates(self, avaliable_pool):
        position_list = range(1, self.exp_parameters.n_recall_candidate+1)
        numpy.random.shuffle(position_list)
        self.response_candidates = []
        
        for sp in range(self.exp_parameters.set_size):
            position_index = numpy.random.randint(len(position_list))
            position = position_list.pop(position_index)
            
            self.response_candidates.append(ResponseCandidate(self.stimulus[sp], position))
            
        for _ in range(self.exp_parameters.n_recall_candidate - self.exp_parameters.set_size):
            picked_index = numpy.random.randint(len(avaliable_pool))
            stimulus = Stimulus(avaliable_pool.pop(picked_index), self.exp_parameters)
            
            position_index = numpy.random.randint(len(position_list))
            position = position_list.pop(position_index)
            
            self.response_candidates.append(ResponseCandidate(stimulus, position))
            
    def createProbe(self):
        serial_positions = numpy.arange(self.exp_parameters.set_size) + 1
        numpy.random.shuffle(serial_positions)
        
        for i, serial_position in enumerate(serial_positions):
            probe_type = 'order'
            stimulus = Stimulus(serial_position * -1, self.exp_parameters)
            
            self.probes[i] = Probe(probe_type, serial_position, stimulus)
        
class ContextRecallTrial(Trial):
    def __init__(self, avaliable_pool, exp_parameters, display = None):
        super(ContextRecallTrial, self).__init__(avaliable_pool, exp_parameters, display)
        
        self._createCandidates()
        
    def _createCandidates(self):
        self.response_candidates = []
        for sp in range(1, self.exp_parameters.set_size+1):
            stimulus = Stimulus(sp * -1, self.exp_parameters)
            position = sp
            
            self.response_candidates.append(ResponseCandidate(stimulus, position))
            
    def createProbe(self):
        serial_positions = numpy.arange(self.exp_parameters.set_size) + 1
        numpy.random.shuffle(serial_positions)
        
        for i, serial_position in enumerate(serial_positions):
            probe_type = 'item'
            self.probes[i] = Probe(probe_type, serial_position, self.stimulus[serial_position-1])


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