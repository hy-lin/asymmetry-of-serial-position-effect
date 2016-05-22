'''
Created on May 22, 2016

@author: Aicey
'''
import FileParser
import ExpParameters
import numpy
import figures
import matplotlib.pyplot as plt


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

def processItemRecallSerialPosition(participants, processedData):
    setsize = 6
    
    var_name = ['ItemRecallSP_{}'.format(sp+1) for sp in range(setsize)]
    processedData['var_name'] += var_name
    
    for pID, pKey in enumerate(participants.keys()):
        if pID not in processedData.keys():
            processedData[pID] = []
        
        pCor = [0.0 for i in range(setsize)]
        for sp in range(1, setsize + 1):
            trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['item'], 'serial_position': [sp]})
            for trial in trials:
                pCor[sp-1] += trial.correctness
                
            pCor[sp-1] /= len(trials)
            
        processedData[pID] += pCor
        
def processOrderRecallSerialPosition(participants, processedData):
    setsize = 6
    
    var_name = ['OrderRecallSP_{}'.format(sp+1) for sp in range(setsize)]
    processedData['var_name'] += var_name
    
    for pID, pKey in enumerate(participants.keys()):
        if pID not in processedData.keys():
            processedData[pID] = []
        
        pCor = [0.0 for i in range(setsize)]
        
        for sp in range(1, setsize+1):
            trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['order'], 'serial_position': [sp]})
            for trial in trials:
                pCor[sp-1] += trial.correctness
                
            pCor[sp-1] /= len(trials)
            
        processedData[pID] += pCor

def processItemRecallTransposition(participants, processedData):
    setsize = 6
    
    var_name = ['ItemRecallTrans_{}'.format(trans+1) for trans in range(-setsize+1, setsize)]
    processedData['var_name'] += var_name
    
    for pID, pKey in enumerate(participants.keys()):
        if pID not in processedData.keys():
            processedData[pID] = []
            
        pRecall = [0.0 for i in range(setsize*2-1)]
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['item']})
        for trial in trials:
            displacement = trial.getTransposition()
            if not numpy.isnan(displacement):
                pRecall[displacement+setsize-1] += 1
                
        pRecall = [pRecall[i] / len(trials) for i in range(setsize*2-1)]
        
        processedData[pID] += pRecall
        
def processOrderRecallTransposition(participants, processedData):
    setsize = 6
    
    var_name = ['OrderRecallTrans_{}'.format(trans+1) for trans in range(-setsize+1, setsize)]
    processedData['var_name'] += var_name
    
    for pID, pKey in enumerate(participants.keys()):
        if pID not in processedData.keys():
            processedData[pID] = []
        
        pRecall = [0.0 for i in range(setsize*2-1)]
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['order']})
        for trial in trials:
            displacement = trial.getTransposition()
            if not numpy.isnan(displacement):
                print displacement+setsize-1
                pRecall[displacement+setsize-1] += 1
                
        pRecall = [pRecall[i] / len(trials) for i in range(setsize*2-1)]
        
        processedData[pID] += pRecall
        
def processItemRecallSPAsymmetry(participants, processedData):
    setsize = 6
    
    processedData['var_name'] += ['ItemRecallSPAsymmetry']
    
    for pID, pKey in enumerate(participants.keys()):
        if pID not in processedData.keys():
            processedData[pID] = []
        
        pCorPrimacy = 0.0
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['item'], 'serial_position': [1]})
        for trial in trials:
            pCorPrimacy += trial.correctness
                
        pCorPrimacy /= len(trials)
        
        pCorRecency = 0.0
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['item'], 'serial_position': [setsize]})
        for trial in trials:
            pCorRecency += trial.correctness
                
        pCorRecency /= len(trials)
        
        if pCorPrimacy <= 0.5/len(trials):
            pCorPrimacy = 0.5/len(trials)
        if pCorRecency <= 0.5/len(trials):
            pCorRecency = 0.5/len(trials)
            
        asymmetry_score = pCorRecency / pCorPrimacy
        
        processedData[pID] += [asymmetry_score]
        
def processOrderRecallSPAsymmetry(participants, processedData):
    setsize = 6
    
    processedData['var_name'] += ['OrderRecallSPAsymmetry']
    
    for pID, pKey in enumerate(participants.keys()):
        if pID not in processedData.keys():
            processedData[pID] = []
        
        pCorPrimacy = 0.0
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['order'], 'serial_position': [1]})
        for trial in trials:
            pCorPrimacy += trial.correctness
                
        pCorPrimacy /= len(trials)
        
        pCorRecency = 0.0
        trials = participants[pKey].getTrialsMetConstraints({'probe_type': ['order'], 'serial_position': [setsize]})
        for trial in trials:
            pCorRecency += trial.correctness
                
        pCorRecency /= len(trials)
        
        if pCorPrimacy <= 0.5/len(trials):
            pCorPrimacy = 0.5/len(trials)
        if pCorRecency <= 0.5/len(trials):
            pCorRecency = 0.5/len(trials)

        asymmetry_score = pCorRecency / pCorPrimacy
        
        processedData[pID] += [asymmetry_score]
        
def processItemRecallTranspositionAsymmetry(participants, processedData):
    setsize = 6
    
    processedData['var_name'] += ['ItemRecallTransAsymmetry']
    
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
                    pCorRecency += 1.0
                elif displacement >= 1:
                    pCorPrimacy += 1.0
                
        pCorRecency /= len(trials)
        pCorPrimacy /= len(trials)
        
        
        if pCorPrimacy <= 0.5/len(trials):
            pCorPrimacy = 0.5/len(trials)
        if pCorRecency <= 0.5/len(trials):
            pCorRecency = 0.5/len(trials)

        asymmetry_score = pCorRecency / pCorPrimacy
        
        processedData[pID] += [asymmetry_score]

def processOrderRecallTranspositionAsymmetry(participants, processedData):
    setsize = 6
    
    processedData['var_name'] += ['OrderRecallTransAsymmetry']
    
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
                    pCorRecency += 1.0
                elif displacement >= 1:
                    pCorPrimacy += 1.0
                
        pCorRecency /= len(trials)
        pCorPrimacy /= len(trials)
        
        
        if pCorPrimacy <= 0.5/len(trials):
            pCorPrimacy = 0.5/len(trials)
        if pCorRecency <= 0.5/len(trials):
            pCorRecency = 0.5/len(trials)

        asymmetry_score = pCorRecency / pCorPrimacy
        
        processedData[pID] += [asymmetry_score]
        
def outputData(file_name, processedData):
    f_handle = open(file_name, 'w')
    
    for val in processedData['var_name']:
        f_handle.write('{}\t'.format(val))
        
    f_handle.write('\n')
    
    for pID in processedData.keys():
        if pID != 'var_name':
            f_handle.write('{}\t'.format(pID))
            for val in processedData[pID]:
                f_handle.write('{}\t'.format(val))
                
        f_handle.write('\n')
    
    f_handle.close()

def main():
    participants = loadData('probedrecallNcontextrecall.dat')
    
    processedData = {'var_name': []}
    
#     processItemRecallSerialPosition(participants, processedData)
#     processOrderRecallSerialPosition(participants, processedData)
#     processItemRecallTransposition(participants, processedData)
#     processOrderRecallTransposition(participants, processedData)
    
    processItemRecallSPAsymmetry(participants, processedData)
    processOrderRecallSPAsymmetry(participants, processedData)
    processItemRecallTranspositionAsymmetry(participants, processedData)
    processOrderRecallTranspositionAsymmetry(participants, processedData)
    
    outputData('test.txt', processedData)


if __name__ == '__main__':
    main()