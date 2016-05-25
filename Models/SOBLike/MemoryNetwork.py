'''
Created on 10.05.2016

@author: Hsuan-Yu Lin
'''

import numpy

class MemoryNetwork(object):
    '''
    This is the main memory network for the simulation.
    '''


    def __init__(self, parameters):
        '''
        Constructor
        '''
        
        self.parameters = parameters
        self.resetNetwork()
        
    def encode(self, item, serial_position, encoding_strength):
        self.blendShadow(serial_position)
        self.network += (numpy.outer(item, self.shadow) * encoding_strength)
    
    def blendShadow(self, serial_position):
        self.shadow = (1-self.parameters.r) * serial_position + self.parameters.r * self.shadow
        self.shadow /= numpy.sqrt(numpy.dot(self.shadow, self.shadow))
    
    def retrieveSerialPosition(self, item):
        return numpy.inner(item, numpy.transpose(self.network))
    
    def retrieveItem(self, serial_position):
        return numpy.dot(self.network, serial_position)
    
    def resetNetwork(self):
        self.network = numpy.zeros([self.parameters.NUMBER_OF_ITEM_NODES, self.parameters.NUMBER_OF_SERIAL_POSITION_NODES])
        self.shadow = numpy.zeros(self.parameters.NUMBER_OF_SERIAL_POSITION_NODES)
        
    def recallItem(self, serial_position, response_candidates):
        retrieved_item = self.retrieveItem(serial_position)
        
        return self.getRecallProbability(retrieved_item, response_candidates, self.parameters.c_i)
    
    def recallOrder(self, probe_item, response_candidates):
        retrieved_order = self.retrieveSerialPosition(probe_item)
        
        return self.getRecallProbability(retrieved_order, response_candidates, self.parameters.c_p)
    
    def getRecallProbability(self, retrieved_memory, response_candidates, c):
        similarity_list = numpy.zeros(len(response_candidates))
        
        for i, response_candidate in enumerate(response_candidates):
            similarity_list[i] = VectorCosine(retrieved_memory, response_candidate)
            
        return numpy.exp(c * similarity_list) / numpy.sum(numpy.exp(c * similarity_list)) 
        

def VectorCosine(v1, v2):
    return numpy.inner(v1, v2) / numpy.sqrt(numpy.inner(v1, v1) * numpy.inner(v2, v2))
