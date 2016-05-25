'''
Created on May 24, 2016

@author: Aicey
'''
import MemoryNetwork
import numpy
import math

class FakeParticipant(object):
    '''
    classdocs
    '''
    def __init__(self, pID, parameters):
        '''
        Constructor
        '''
        self.pID = pID
        
        self.parameters = parameters
        self.memory_network = MemoryNetwork.MemoryNetwork(self.parameters)
        
        self.set_size = 6
        self.simulation_iteration = 1000
        
        self.createItems()
        self.createSerialPositions()
        self.createEncodingStrength()
        
    def createItems(self):
        self._createItemPrototype()
        self._createItemFromPrototype()
    
    def _createItemPrototype(self):
        self.itemPrototype = numpy.random.choice([-1, 1], self.parameters.NUMBER_OF_ITEM_NODES)
        
    def _createItemFromPrototype(self):
        modifier = numpy.random.choice([-1, 1], [self.parameters.NUMBER_OF_ITEMS, self.parameters.NUMBER_OF_ITEM_NODES], True, [self.parameters.si, 1-self.parameters.si])
        self.item_pool = modifier * numpy.tile(self.itemPrototype, [self.parameters.NUMBER_OF_ITEMS, 1])
    
    def createSerialPositions(self):
        self._calcSerialPositionSimilarity()
        weight_matrix = self._createWeightMatrix()
        
        hadamard_matrix = createHadamardMatrix(self.parameters.NUMBER_OF_SERIAL_POSITION_NODES)
        
        serial_positions = numpy.dot(weight_matrix, hadamard_matrix)
        for i in range(len(serial_positions)):
            serial_positions[i] /= numpy.sqrt(numpy.dot(serial_positions[i], serial_positions[i]))
        
        self.serial_positions = serial_positions
    
    def _calcSerialPositionSimilarity(self):
        serial_positions = numpy.arange(1, self.set_size)
        
        sp_p = numpy.power(self.parameters.sp_p, serial_positions)
        sp_r = numpy.power(self.parameters.sp_r, max(serial_positions) - serial_positions + 1)
        
        sp = sp_p + sp_r
        sp[sp > .99] = .99
#         sp[sp < .1] = .1
        sp = numpy.insert(sp, 0, 0.0)
        self.sp = 1.0 - sp
        
    def _createWeightMatrix(self):
        weight_matrix = numpy.zeros([self.set_size, self.parameters.NUMBER_OF_SERIAL_POSITION_NODES])
        first_row = 1
        for i in range(self.set_size):
            weight_matrix[i][0] = self.sp[i] * first_row
            first_row *= self.sp[i]
            _tmp = first_row
            for l in range(i):
                _tmp = _tmp / self.sp[l+1]
                weight_matrix[i][l+1] = _tmp * numpy.sqrt(1 - self.sp[l+1]**2)
                
        return weight_matrix
    
    def createEncodingStrength(self):
        serial_positions = numpy.arange(1, self.set_size+1)
        
        eta_p = numpy.power(self.parameters.eta_p, serial_positions)
        eta_r = numpy.power(self.parameters.eta_r, max(serial_positions) - serial_positions + 1)
        
        eta = eta_p + eta_r
#         eta[eta > .9] = .9
#         eta[eta < .1] = .1
        
        self.eta = eta
    
    def simulateTrials(self):
        self.trials = []
        stm = MemoryNetwork.MemoryNetwork(self.parameters)
        
        for i in range(self.simulation_iteration):
            current_trial = Trial()
            self._choiceProbeType(current_trial)
            self._choiceItems(current_trial)
            self._choiceProbe(current_trial)
            
            self._encodeStimulus(current_trial, stm)
            self._recall(current_trial, stm)
            
            self.trials.append(current_trial)
            
            stm.resetNetwork()
        
    def _encodeStimulus(self, trial, stm):
        for sp in range(self.set_size):
            stm.encode(trial.stimulus_vector[sp], self.serial_positions[sp], self.eta[sp])

    def _recall(self, trial, stm):
        if trial.probe_type == 'item':
            p_recall = stm.recallOrder(trial.probe_vector, trial.response_candidates_vector)
        elif trial.probe_type == 'order':
            p_recall = stm.recallItem(trial.probe_vector, trial.response_candidates_vector)
        
        trial.response = numpy.random.choice(trial.response_candidates, p = p_recall)
        trial.checkCorrectness()
    
    def _choiceProbeType(self, trial):
        trial.probe_type = numpy.random.choice(['item', 'order'])
    
    def _choiceItems(self, trial):
        if trial.probe_type == 'item':
            trial.stimulus = numpy.random.choice(range(self.parameters.NUMBER_OF_ITEMS), self.set_size, replace = False)
            trial.response_candidates = -1*(numpy.arange(self.set_size) + 1)
            
            trial.response_candidates_vector = self.serial_positions
        elif trial.probe_type == 'order':
            trial.response_candidates = numpy.random.choice(range(self.parameters.NUMBER_OF_ITEMS), self.set_size * 3, replace = False)
            trial.stimulus = trial.response_candidates[0:self.set_size]
            
            trial.response_candidates_vector = [self.item_pool[i] for i in trial.response_candidates]
        
        
        trial.stimulus_vector = [self.item_pool[i] for i in trial.stimulus]
        
    def _choiceProbe(self, trial):
        trial.serial_position = numpy.random.choice(numpy.arange(self.set_size)+1)
        
        if trial.probe_type == 'item':
            trial.probe = trial.stimulus[trial.serial_position-1]
            trial.probe_vector = trial.stimulus_vector[trial.serial_position-1]
        elif trial.probe_type == 'order':
            trial.probe = trial.serial_position
            trial.probe_vector = self.serial_positions[trial.serial_position-1]
        
    def getTrialsMetConstraints(self, constraints):
        final_pool = []
        
        for trial in self.trials:
            if trial.isMetConstraints(constraints):
                final_pool.append(trial)
                
        return final_pool
    
class Trial(object):
    def __init__(self):
        pass
            
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
    
    def getTransposition(self):
        if self.probe_type == 'order': # recall item
            respond_sp = -1
            
            for i, stimulus in enumerate(self.stimulus):
                if stimulus == self.response:
                    respond_sp = i+1
                    
                    
            if respond_sp != -1:
                return respond_sp - self.serial_position
            else:
                return numpy.NaN
            
        if self.probe_type == 'item': # recall order
            respond_sp = self.response * -1
            return respond_sp - self.serial_position
    
    
def createHadamardMatrix(n):
    hadamardBasis = numpy.array([[1, -1], [1, 1]])
    hadamard = numpy.array(hadamardBasis)
    nRepeat = math.log(n, 2) - 1
    for rep in range(int(nRepeat)):
        hadamardNew = numpy.tile(numpy.zeros(hadamard.shape), [2, 2])
        for i in range(2):
            for l in range(2): # the outer 2 loops handles the basic matrix
                for i2 in range(len(hadamard)):
                    for l2 in range(len(hadamard)):
                        x = i2 + i*len(hadamard)
                        y = l2 + l*len(hadamard)
                        hadamardNew[x][y] = hadamard[i2][l2] * hadamardBasis[i][l]
        hadamard = hadamardNew
         
    return hadamard
