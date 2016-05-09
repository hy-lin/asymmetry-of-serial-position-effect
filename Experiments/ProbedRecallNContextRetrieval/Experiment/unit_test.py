'''
Created on 13.10.2015

@author: Hsuan-Yu Lin
'''
import unittest
import myClasses
import ExpParameters

class Test(unittest.TestCase):


    def testTrial(self):
        exp_parameters = ExpParameters.ExpParameters()
        avaliable_list = range(15)
        context_trial = myClasses.ContextRecallTrial(avaliable_list, exp_parameters)
        context_trial.createProbe(5)
        for stimulus in context_trial.stimulus:
            print stimulus
        print context_trial.probe
        pass
    
    def testFile(self):
        f_head = open('RESOURCES\\wordlist.txt', 'r')

        for line in f_head:
            print line.split()


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()