'''
Created on 21.04.2015

@author: Hsuan-Yu Lin
'''

class ExpParameters(object):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        self.set_size = 5
        self.n_recall_candidate = 15
        
        self.candidate_width_unscale = 180
        self.candidate_height_unscale = 40
        self.thin_line_unscale = 2
        self.thick_line_unscale = 5
        self.font_size_unscaled = 36
        
        self.n_practice_rep = 1
        self.n_experiment_rep = 20
        self.n_breaks = 20
        self.word_list = []
        self.word_n = 0
        
    def updateDisplayScale(self, display):
        x, y = display.window.size
        x_scale = x / 1280.0
        y_scale = y / 720.0
        
        print 'x:y = ', x, y
        print 'x:y scale = ', x_scale, y_scale
        self.scale = min(x_scale, y_scale)
        
        self.window_center = (x/2, y/2)
        self.window_size = (x * self.scale, y * self.scale)
        
        self.candidate_width = self.candidate_width_unscale * self.scale
        self.candidate_height = self.candidate_height_unscale * self.scale
        self.thin_line = self.thin_line_unscale * self.scale
        self.thick_line = self.thick_line_unscale * self.scale
        self.font_size = self.font_size_unscaled * self.scale
        
    def loadWordList(self, resources):
        self.word_list = []
        with open(resources.get_path('wordlist.txt'), 'r') as f:
            for line in f:
                words = line.split()
                self.word_list.append(words[0])
                
        self.word_n = len(self.word_list)
