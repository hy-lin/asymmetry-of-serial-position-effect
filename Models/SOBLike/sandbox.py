'''
Created on 10.05.2016

@author: Hsuan-Yu Lin
'''

import Parameters
import matplotlib.pyplot as plt
import numpy

def testGradient():
    n_iteration = 100
    
    serial_positions = numpy.arange(1, 7)
    
    for i in range(n_iteration):
        parameters_set = Parameters.Parameters(False)
        
        eta_p = numpy.power(parameters_set.eta_p, serial_positions)
        eta_r = numpy.power(parameters_set.eta_r, max(serial_positions) - serial_positions + 1)
        
        sp_p = numpy.power(parameters_set.sp_p, serial_positions)
        sp_r = numpy.power(parameters_set.sp_r, max(serial_positions) - serial_positions + 1)
        
        eta = eta_p + eta_r
        eta[eta>.9] = .9
#         plt.figure()
        
        plt.subplot(10, 10, i)
        
        plt.plot(eta)
        plt.tick_params(axis = 'both', which = 'both', labelbottom = 'off', labeltop = 'off', labelleft = 'off', labelright = 'off')
        plt.ylim([0, 1])

        
    plt.show()


if __name__ == '__main__':
    testGradient()
    
    pass