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
        self.network += numpy.outer(item, serial_position) * encoding_strength
        
    def retrieveSerialPosition(self, item):
        return numpy.inner(item, self.network)
    
    def retrieveItem(self, serial_position):
        return numpy.dot(self.network, serial_position)
    
    def resetNetwork(self):
        self.network = numpy.zeros([self.parameters.NUMBER_OF_ITEM_NODES, self.parameters.NUMBER_OF_SERIAL_POSITION_NODES])
        
    def recallItem(self, serial_position, response_candidates):
        retrieved_item = self.retrieveItem(serial_position)
        

def VectorCosine(v1, v2):
    return numpy.inner(v1, v2) / numpy.sqrt(numpy.inner(v1, v1) * numpy.inner(v2, v2))
