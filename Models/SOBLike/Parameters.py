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
        
#         self.eta_p = 0.434799886474
#         self.eta_r = 0.615076522129
#         
#         self.sp_p = 0.840514487874
#         self.sp_r = 0.327408601945
#         
#         self.si = 0.202085301445
#         
#         self.c_p = 9.22785235733
#         self.c_i = 14.3237418447
        
        self.eta_p = 0.5
        self.eta_r = 0.5
         
        self.sp_p = 0.5
        self.sp_r = 0.5
         
        self.si = 0.25
         
        self.c_p = 10.0
        self.c_i = 10.0
        
        self.r = .15
        
        self.eta_p_range = [0.2, 0.8]
        self.eta_r_range = [0.2, 0.8]
        
        self.sp_p_range = [0.2, 0.8]
        self.sp_r_range = [0.2, 0.8]
        
        self.si_range = [0.15, 0.5]
        
        self.c_p_range = [6.0, 10.0]
        self.c_i_range = [10.0, 14.0]
        
        self.r_range = [0.2, 0.3]
        
        if set_to_default == False:
            self.generateRandomParameters()
            
    def generateRandomParameters(self):
        self.eta_p = numpy.random.uniform(self.eta_p_range[0], self.eta_p_range[1])
        self.eta_r = numpy.random.uniform(self.eta_r_range[0], self.eta_r_range[1])
#         self.eta_r = 1.0 - self.eta_p
        
        self.sp_p = numpy.random.uniform(self.sp_p_range[0], self.sp_p_range[1])
        self.sp_r = numpy.random.uniform(self.sp_r_range[0], self.sp_r_range[1])
#         self.sp_r = 1.0 - self.sp_r
        
        self.si = numpy.random.uniform(self.si_range[0], self.si_range[1])
        
        self.c_p = numpy.random.uniform(self.c_p_range[0], self.c_p_range[1])
        self.c_i = numpy.random.uniform(self.c_i_range[0], self.c_i_range[1])
        
        self.r = numpy.random.uniform(self.r_range[0], self.r_range[1])
        
    def __str__(self):
        return 'eta_p:{}\neta_r:{}\nsp_p:{}\nsp_r:{}\nsi:{}\nc_p:{}\nc_i{}\n'.format(self.eta_p, \
                                                                                     self.eta_r, \
                                                                                     self.sp_p, \
                                                                                     self.sp_r, \
                                                                                     self.si, \
                                                                                     self.c_p, \
                                                                                     self.c_i)
        