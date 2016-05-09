'''
Created on Mar 31, 2016

@author: Aicey
'''
import numpy

class SerialPositionModel(object):
    '''
    classdocs
    '''


    def __init__(self, p, r):
        '''
        Constructor
        '''
        self.p = p
        self.r = r
        
    def getSerialPositionEffect(self, setsize):
        serial_position = numpy.arange(1, setsize+1)
        primacy = self.p**serial_position
        recency = self.r**(setsize+1 - serial_position)
        
        pc = primacy + recency
        pc[pc>1.0] = 1.0
        return pc