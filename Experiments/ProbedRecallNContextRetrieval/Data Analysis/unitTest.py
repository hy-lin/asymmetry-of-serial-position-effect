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

def plotItemSP(participants, aggregate_mode = 'all'):
    setsize = 6
    nParticipants = len(participants)
    
    pCor = numpy.zeros([nParticipants, setsize])
    for pID, pKey in enumerate(participants.keys()):
        print pID
        for sp in range(1, setsize + 1):
            trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['order'], 'serial_position': [sp]})
            for trial in trials:
                pCor[pID, sp-1] += trial.correctness
                
            pCor[pID, sp-1] /= len(trials)
    
    if aggregate_mode == 'all':
        data = {'order': numpy.array([range(1, setsize+1),numpy.mean(pCor, 0)])}
        
        agg_figure = figures.LineFigure(data)
        agg_figure.setTitle('Position Probed Item Recall')
        agg_figure.setXLabel('serial position')
        agg_figure.setYLabel('Proportion of Correct')
        agg_figure.setXLim([0.5, setsize+0.5])
        agg_figure.setYLim([0.5, 1.0])
        agg_figure.legend = False
        agg_figure.update()
        
         
    elif aggregate_mode == 'individual':
        for pID in range(len(participants)):
            data = {'order': numpy.array([range(1, setsize+1),pCor[pID]])}
            
            idv_figure = figures.LineFigure(data)
            idv_figure.setTitle('Position Probed Item Recall, pID = {}'.format(pID), True)
        
    pass

def plotOrderTransposition(participants, aggregate_mode = 'all'):
    setsize = 6
    nParticipants = len(participants)
    
    pRecall = numpy.zeros([nParticipants, setsize*2-1])
    for pID, pKey in enumerate(participants.keys()):
        print pID
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['item'], 'serial_position': [2, 3, 4, 5]})
        for trial in trials:
            displacement = trial.getTransposition()
            if displacement != numpy.NaN:
                pRecall[pID, displacement+setsize-1] += 1
                
        pRecall[pID] /= len(trials)
            
    if aggregate_mode == 'all':
        data = {'item': numpy.array([range(-setsize+1, setsize),numpy.mean(pRecall, 0)])}
        
        agg_figure = figures.LineFigure(data)
        agg_figure.setTitle('Item Probed Position Recall')
        agg_figure.setXLabel('displacement (recalled position - correct position)')
        agg_figure.setYLabel('Proportion of response')
        agg_figure.setXLim([0.5-setsize, setsize-0.5])
        agg_figure.setYLim([0.0, 0.8])
        agg_figure.legend = False
        agg_figure.update()
        
        
    elif aggregate_mode == 'individual':
        for pID in range(len(participants)):
            data = {'order': numpy.array([range(-setsize+1, setsize), pRecall[pID]])}
            
            idv_figure = figures.LineFigure(data)
            idv_figure.setTitle('Item Probed Position Recall, pID = {}'.format(pID), True)
        
    pass

def plotItemTransposition(participants, aggregate_mode = 'all'):
    setsize = 6
    nParticipants = len(participants)
    
    pRecall = numpy.zeros([nParticipants, setsize*2-1])
    for pID, pKey in enumerate(participants.keys()):
        print pID
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['order'], 'serial_position': [2, 3, 4, 5]})
        for trial in trials:
            displacement = trial.getTransposition()
            print displacement
            if not numpy.isnan(displacement):
                pRecall[pID, displacement+setsize-1] += 1
                
        pRecall[pID] /= len(trials)
            
    if aggregate_mode == 'all':
        data = {'order': numpy.array([range(-setsize+1, setsize),numpy.mean(pRecall, 0)])}
        
        agg_figure = figures.LineFigure(data)
        agg_figure.setTitle('Position Probed Item Recall', update = True)
        agg_figure.setXLabel('displacement (recalled position - correct position)')
        agg_figure.setYLabel('Proportion of response')
        agg_figure.setXLim([0.5-setsize, setsize-0.5])
        agg_figure.setYLim([0.0, 0.8])
        agg_figure.legend = False
        agg_figure.update()
        
    elif aggregate_mode == 'individual':
        for pID in range(len(participants)):
            data = {'order': numpy.array([range(-setsize+1, setsize), pRecall[pID]])}
            
            idv_figure = figures.LineFigure(data)
            idv_figure.setTitle('Position Probed Item Recall, pID = {}'.format(pID), True)
        
    pass


def plotOrderSP(participants, aggregate_mode = 'all'):
    setsize = 6
    nParticipants = len(participants)
    
    pCor = numpy.zeros([nParticipants, setsize])
    for pID, pKey in enumerate(participants.keys()):
        print pID
        for sp in range(1, setsize+1):
            trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['item'], 'serial_position': [sp]})
            for trial in trials:
                pCor[pID, sp-1] += trial.correctness
                
            pCor[pID, sp-1] /= len(trials)
    
    if aggregate_mode == 'all':
        data = {'item': numpy.array([range(1, setsize+1),numpy.mean(pCor, 0)])}
        
        agg_figure = figures.LineFigure(data)
        agg_figure.setTitle('Item Probed Position Recall')
        
        agg_figure.setXLabel('serial position')
        agg_figure.setYLabel('Proportion of Correct')
        agg_figure.setXLim([0.5, setsize+0.5])
        agg_figure.setYLim([0.5, 1.0])
        agg_figure.legend = False
        agg_figure.update()
         
    elif aggregate_mode == 'individual':
        for pID in range(len(participants)):
            data = {'item': numpy.array([range(1, setsize+1),pCor[pID]])}
            
            idv_figure = figures.LineFigure(data)
            idv_figure.setTitle('Item Probed Position Recall, pID = {}'.format(pID), True)
        
    pass

def testModel():
    model = SerialPositionModel.SerialPositionModel(.5, .8)
    print model.getSerialPositionEffect(8)
        

if __name__ == '__main__':
#     testModel()
    participants = loadData('probedrecallNcontextrecall.dat')
    print len(participants)

    for pID in participants.keys():
        trials = participants[pID].getTrialsMetConstraints({'probe_type': ['item']})
        pCor = 0.0
        for trial in trials:
#             print trial.serial_position
            pCor += trial.correctness
            
        print pCor / len(trials), len(trials)
        
    plotOrderSP(participants, 'all')
    plotItemSP(participants, 'all')
    
    plotOrderTransposition(participants, 'all')
    plotItemTransposition(participants, 'all')
    
    plt.show()
    
    pass