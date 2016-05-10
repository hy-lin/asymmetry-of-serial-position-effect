'''
Created on 10.05.2016

@author: Hsuan-Yu Lin
'''

import numpy

class Parameters(object):
    '''
    The parameters of the SOBLike model.
    '''


    def __init__(self, set_to_default = True):
        '''
        if set_to_default is false, a random set of parameters will be generated
        according to the range of parameters. 
        '''
        
        # constants
        self.NUMBER_OF_ITEM_NODES = 200
        self.NUMBER_OF_SERIAL_POSITION_NODES = 16
        
        self.NUMBER_OF_ITEMS = 400
        
        self.eta_p = 0.5
        self.eta_r = 0.5
        
        self.sp_p = 0.5
        self.sp_r = 0.5
        
        self.si = 0.25
        
        self.c_p = 10.0
        self.c_i = 10.0
        
        self.eta_p_range = [0.0, 1.0]
        self.eta_r_range = [0.0, 1.0]
        
        self.sp_p_range = [0.0, 1.0]
        self.sp_r_range = [0.0, 1.0]
        
        self.si_range = [0.15, 0.5]
        
        self.c_p_range = [5.0, 20.0]
        self.c_i_range = [5.0, 20.0]
        
        if set_to_default == False:
            self.generateRandomParameters()
            
    def generateRandomParameters(self):
        self.eta_p = numpy.random.uniform(self.eta_p_range[0], self.eta_p_range[1])
        self.eta_r = numpy.random.uniform(self.eta_r_range[0], self.eta_r_range[1])
        
        self.sp_p = numpy.random.uniform(self.sp_p_range[0], self.sp_p_range[1])
        self.sp_r = numpy.random.uniform(self.sp_r_range[0], self.sp_r_range[1])
        
        self.si = numpy.random.uniform(self.si_range[0], self.si_range[1])
        
        self.c_p = numpy.random.uniform(self.c_p_range[0], self.c_p_range[1])
        self.c_i = numpy.random.uniform(self.c_i_range[0], self.c_i_range[1])
        