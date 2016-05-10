'''
Created on 17.11.2015

@author: Hsuan-Yu Lin
'''

import FileParser
import ExpParameters
import numpy
import figures
import matplotlib.pyplot as plt
import SerialPositionModel


def _openFile(file_name):
    '''
    Open the data file, returns the file handle
    '''
    file_handle = open(file_name, 'r')
    
    return file_handle

def loadData(file_name, ban_list = []):
    file_handle = _openFile(file_name)

    columns_definition = FileParser.ColumnsDefinition()
    exp_parameters = ExpParameters.ExpParameters()
    file_parser = FileParser.FileParser(columns_definition, exp_parameters)
    
    participants = file_parser.parse(file_handle, ban_list)

    for pID in participants.keys():
        print participants[pID]
        
    return participants

def plotOrderSP(participants, aggregate_mode = 'all'):
    setsize = 6
    nParticipants = len(participants)
    
    pCor = numpy.zeros([nParticipants, setsize])
    for pID, pKey in enumerate(participants.keys()):
        print pID
        for sp in range(1, setsize + 1):
            trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['order'], 'serial_position': [sp], 'output_position': [1, 2, 3, 4, 5]})
            for trial in trials:
                pCor[pID, sp-1] += trial.correctness
                
            pCor[pID, sp-1] /= len(trials)
    
    if aggregate_mode == 'all':
        data = {'order': numpy.array([range(1, setsize+1),numpy.mean(pCor, 0)])}
        
        agg_figure = figures.LineFigure(data)
        agg_figure.setTitle('Order recall', update = True)
        
        plt.show()
        
         
    elif aggregate_mode == 'individual':
        for pID in range(len(participants)):
            data = {'order': numpy.array([range(1, setsize+1),pCor[pID]])}
            
            idv_figure = figures.LineFigure(data)
            idv_figure.setTitle('Order Recall, pID = {}'.format(pID), True)
            plt.show()
        
    pass

def plotItemSP(participants, aggregate_mode = 'all'):
    setsize = 6
    nParticipants = len(participants)
    
    pCor = numpy.zeros([nParticipants, setsize])
    for pID, pKey in enumerate(participants.keys()):
        print pID
        for sp in range(1, setsize + 1):
            trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['item'], 'serial_position': [sp], 'output_position': [1, 2, 3, 4, 5]})
            for trial in trials:
                pCor[pID, sp-1] += trial.correctness
                
            pCor[pID, sp-1] /= len(trials)
    
    if aggregate_mode == 'all':
        data = {'item': numpy.array([range(1, setsize+1),numpy.mean(pCor, 0)])}
        
        agg_figure = figures.LineFigure(data)
        agg_figure.setTitle('Probe recall', update = True)
        
        plt.show()
        
         
    elif aggregate_mode == 'individual':
        for pID in range(len(participants)):
            data = {'item': numpy.array([range(1, setsize+1),pCor[pID]])}
            
            idv_figure = figures.LineFigure(data)
            idv_figure.setTitle('Probed Recall, pID = {}'.format(pID), True)
            plt.show()
        
    pass

def testModel():
    model = SerialPositionModel.SerialPositionModel(.5, .8)
    print model.getSerialPositionEffect(8)
        

if __name__ == '__main__':
#     testModel()
    participants = loadData('probedrecallNcontextrecall.dat')

#     for pID in participants.keys():
#         trials = participants[pID].getTrialsMetConstraints({'probe_type': ['item']})
#         pCor = 0.0
#         for trial in trials:
# #             print trial.serial_position
#             pCor += trial.correctness
#             
#         print pCor / len(trials), len(trials)
        
    plotOrderSP(participants, 'individual')
    plotItemSP(participants, 'individual')
    
    pass