'''
Created on 10.05.2016

@author: Hsuan-Yu Lin
'''

import Parameters
import matplotlib.pyplot as plt
import numpy
import SimulationBatch
import figures
import math

def simulateParticipants():
    n_participants = 100
    participants = {}
    for pID in range(n_participants):
        parameters_set = Parameters.Parameters(False)
        participant = SimulationBatch.FakeParticipant(1, parameters_set)
        participant.simulateTrials()
        
        participants[pID] = participant
        
#         print participant.parameters
    
    return participants    
    

def testSimulation():
    participants = simulateParticipants()
    
    plotOrderSP(participants, 'all')
    plotItemSP(participants, 'all')
    
    plotOrderTransposition(participants, 'all')
    plotItemTransposition(participants, 'all')
    
    plt.show()
    
    
def plotItemSP(participants, aggregate_mode = 'all'):
    setsize = 6
    nParticipants = len(participants)
    
    pCor = numpy.zeros([nParticipants, setsize])
    for pID, pKey in enumerate(participants.keys()):
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
        agg_figure.setYLim([0.0, 1.0])
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
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['order'], 'serial_position': [2, 3, 4, 5]})
        for trial in trials:
            displacement = trial.getTransposition()
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

def processItemRecallSPAsymmetry(participants, processedData):
    setsize = 6
    
    for pID, pKey in enumerate(participants.keys()):
        if pID not in processedData.keys():
            processedData[pID] = []
        
        pCorPrimacy = 0.0
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['order'], 'serial_position': [1, 2, 3]})
        for trial in trials:
            pCorPrimacy += trial.correctness
                
        pCorPrimacy /= len(trials)
        
        pCorRecency = 0.0
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['order'], 'serial_position': [4, 5, setsize]})
        for trial in trials:
            pCorRecency += trial.correctness
                
        pCorRecency /= len(trials)
        
        if pCorPrimacy <= 0.5/len(trials):
            pCorPrimacy = 0.5/len(trials)
        if pCorRecency <= 0.5/len(trials):
            pCorRecency = 0.5/len(trials)
            
        asymmetry_score = pCorPrimacy / pCorRecency
        
        processedData[pID] += [asymmetry_score]
        
def processOrderRecallSPAsymmetry(participants, processedData):
    setsize = 6
    
    for pID, pKey in enumerate(participants.keys()):
        if pID not in processedData.keys():
            processedData[pID] = []
        
        pCorPrimacy = 0.0
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['item'], 'serial_position': [1, 2, 3]})
        for trial in trials:
            pCorPrimacy += trial.correctness
                
        pCorPrimacy /= len(trials)
        
        pCorRecency = 0.0
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['item'], 'serial_position': [4, 5, setsize]})
        for trial in trials:
            pCorRecency += trial.correctness
                
        pCorRecency /= len(trials)
        
        if pCorPrimacy <= 0.5/len(trials):
            pCorPrimacy = 0.5/len(trials)
        if pCorRecency <= 0.5/len(trials):
            pCorRecency = 0.5/len(trials)

        asymmetry_score = pCorPrimacy / pCorRecency
        
        processedData[pID] += [asymmetry_score]
        
def processItemRecallTranspositionAsymmetry(participants, processedData):
    setsize = 6
    
    for pID, pKey in enumerate(participants.keys()):
        if pID not in processedData.keys():
            processedData[pID] = []
            
        pCorPrimacy = 0.0
        pCorRecency = 0.0
        
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['order']})
        for trial in trials:
            displacement = trial.getTransposition()
            if not numpy.isnan(displacement):
                if displacement <= -1:
                    pCorPrimacy += 1.0
                elif displacement >= 1:
                    pCorRecency += 1.0
                
        pCorRecency /= len(trials)
        pCorPrimacy /= len(trials)
        
        
        if pCorPrimacy <= 0.5/len(trials):
            pCorPrimacy = 0.5/len(trials)
        if pCorRecency <= 0.5/len(trials):
            pCorRecency = 0.5/len(trials)

        asymmetry_score = pCorPrimacy / pCorRecency
        
        processedData[pID] += [asymmetry_score]

def processOrderRecallTranspositionAsymmetry(participants, processedData):
    setsize = 6
    
    for pID, pKey in enumerate(participants.keys()):
        if pID not in processedData.keys():
            processedData[pID] = []
            
        pCorPrimacy = 0.0
        pCorRecency = 0.0
        
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['item']})
        for trial in trials:
            displacement = trial.getTransposition()
            if not numpy.isnan(displacement):
                if displacement <= -1:
                    pCorPrimacy += 1.0
                elif displacement >= 1:
                    pCorRecency += 1.0
                
        pCorRecency /= len(trials)
        pCorPrimacy /= len(trials)
        
        
        if pCorPrimacy <= 0.5/len(trials):
            pCorPrimacy = 0.5/len(trials)
        if pCorRecency <= 0.5/len(trials):
            pCorRecency = 0.5/len(trials)

        asymmetry_score = pCorPrimacy / pCorRecency
        
        processedData[pID] += [asymmetry_score]

def getPositionAsymmetry(participants, processedData):
    for pID, pKey in enumerate(participants.keys()):
        if pID not in processedData.keys():
            processedData[pID] = []
            
        processedData[pID] += [participants[pKey].parameters.sp_p / participants[pKey].parameters.sp_r]
        
def getEncodingStrengthAsymmetry(participants, processedData):
    for pID, pKey in enumerate(participants.keys()):
        if pID not in processedData.keys():
            processedData[pID] = []
            
        processedData[pID] += [participants[pKey].parameters.eta_p / participants[pKey].parameters.eta_r]

def plotParameterAndAsymmetryCorrelation():
    participants = simulateParticipants()
    
    processedData = {}
    processItemRecallSPAsymmetry(participants, processedData) # 0
    processOrderRecallSPAsymmetry(participants, processedData) # 1
    processItemRecallTranspositionAsymmetry(participants, processedData) # 2
    processOrderRecallTranspositionAsymmetry(participants, processedData) # 3
    
    getPositionAsymmetry(participants, processedData) # 4
    getEncodingStrengthAsymmetry(participants, processedData) # 5
    
    position_item = plotScatterFromProcessed(processedData, 4, 0, 'Item Recall')
    position_item.setXLabel('position parameters')
    position_item.setYLabel('recall asymmetry')
#     position_item.setYLim([-1.0, 1.0])
    position_item.update()
    position_order = plotScatterFromProcessed(processedData, 4, 1, 'Position Recall')
    position_order.setXLabel('position parameters')
    position_order.setYLabel('recall asymmetry')
#     position_order.setYLim([-1.0, 1.0])
    position_order.update()
    strength_item = plotScatterFromProcessed(processedData, 5, 0, 'Item Recall')
    strength_item.setXLabel('strength parameters')
    strength_item.setYLabel('recall asymmetry')
#     strength_item.setYLim([-1.0, 1.0])
    strength_item.update()
    strength_order = plotScatterFromProcessed(processedData, 5, 1, 'Position Recall')
    strength_order.setXLabel('strength parameters')
    strength_order.setYLabel('recall asymmetry')
#     strength_order.setYLim([-1.0, 1.0])
    strength_order.update()
    
    position_asymmetry = plotRatioScatterFromProcessed(processedData, 4, 0, 1, 'reflexive score')
    position_asymmetry.setXLabel('position parameters')
    position_asymmetry.setYLabel('recall reflexive')
#     position_asymmetry.setYLim([-1.0, 1.0])
    position_asymmetry.update()
    strength_asymmetry = plotRatioScatterFromProcessed(processedData, 5, 0, 1, 'reflexive score')
    strength_asymmetry.setXLabel('strength parameters')
    strength_asymmetry.setYLabel('recall reflexive')
#     strength_asymmetry.setYLim([-1.0, 1.0])
    strength_asymmetry.update()
    
    plt.show()
    
def plotScatterFromProcessed(processedData, x_ind, y_ind, label):
    scatter_data = {label: []}
    for pID in processedData.keys():
        scatter_data[label].append((math.log(processedData[pID][x_ind]), math.log(processedData[pID][y_ind])))
    
    return figures.ScatterFigure(scatter_data)

def plotRatioScatterFromProcessed(processedData, x_ind, y_ind1, y_ind2, label):
    scatter_data = {label: []}
    for pID in processedData.keys():
        scatter_data[label].append((math.log(processedData[pID][x_ind]), math.log(processedData[pID][y_ind1]/processedData[pID][y_ind2])))
    
    return figures.ScatterFigure(scatter_data)

def testGradient():
    n_iteration = 100
    
    serial_positions = numpy.arange(1, 7)
    
    for i in range(n_iteration):
        parameters_set = Parameters.Parameters(False)
        
        eta_p = numpy.power(parameters_set.eta_p, serial_positions)
        eta_r = numpy.power(parameters_set.eta_r, max(serial_positions) - serial_positions + 1)
        
        sp_p = numpy.power(parameters_set.sp_p, serial_positions)
        sp_r = numpy.power(parameters_set.sp_r, max(serial_positions) - serial_positions + 1)
        
        eta = sp_p + sp_r
        eta[eta>.9] = .9
        eta[eta<.1] = .1
#         plt.figure()
        
        plt.subplot(10, 10, i+1)
        
        plt.plot(range(1, 6+1), eta, 'k')
        if i != 90:
            plt.tick_params(axis = 'both', which = 'both', labelbottom = 'off', labeltop = 'off', labelleft = 'off', labelright = 'off')
        plt.ylim([0, 1])

        
    plt.show()


if __name__ == '__main__':
#     testGradient()
    testSimulation()
#     plotParameterAndAsymmetryCorrelation()
    
    pass