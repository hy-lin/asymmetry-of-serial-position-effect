'''
Created on 23.04.2015

@author: Hsuan-Yu Lin
'''

import os
os.environ['PYSDL2_DLL_PATH'] = 'sdl_dll\\'

import sdl2.ext
import sdl2.sdlgfx
import sdl2.surface
import sdl2.sdlttf
import sdl2.timer

class Display(object):
    '''
    classdocs
    '''


    def __init__(self, RESOURCES, exp_parameters):
        '''
        Constructor
        '''
        self.RESOURCES = RESOURCES
        self.exp_parameters = exp_parameters
        
        sdl2.ext.init()
        
        self.fps = sdl2.sdlgfx.FPSManager()
        sdl2.sdlgfx.SDL_initFramerate(self.fps)
        self.window = sdl2.ext.Window('Probed recall and Order recall, Exp 1', (1280, 720), flags = sdl2.SDL_WINDOW_FULLSCREEN_DESKTOP)
        self.window_surface = self.window.get_surface()
        self.renderer = sdl2.ext.Renderer(self.window_surface)

        
        self.t0 = sdl2.timer.SDL_GetTicks()
        
        sdl2.sdlttf.TTF_Init()
        self.font = None
        
        self.running = True
        
    def clear(self, refresh = False):
        self.renderer.clear(sdl2.ext.Color(200, 200, 200))
        if refresh:
            self.refresh()
        
    def refresh(self):
        self.renderer.present()
        self.window.refresh()
        
    def wait(self, ms):
        t0 = sdl2.timer.SDL_GetTicks()
        while sdl2.timer.SDL_GetTicks()-t0 < ms:
            sdl2.ext.get_events()
            
    def waitFPS(self):
        sdl2.sdlgfx.SDL_framerateDelay(self.fps)
        
    def getResponseCandidateRect(self, position):
        cx, cy = self.exp_parameters.window_center
        window_width, window_height = self.exp_parameters.window_size
        if position in [1, 2, 3, 4, 5, 6]:
            rect_center_x = cx
        elif position in [7, 8, 9, 10, 11, 12]:
            rect_center_x = cx - window_width/2 / 2
        else:
            rect_center_x = cx + window_width/2 / 2
        
        rect_center_y = cy + window_height/2 * ((position-1) % 6) / 6
        
        return rect_center_x - self.exp_parameters.candidate_width/2, \
               rect_center_y - self.exp_parameters.candidate_height/2, \
               rect_center_x + self.exp_parameters.candidate_width/2, \
               rect_center_y + self.exp_parameters.candidate_height/2
    
    def getStimulusCoord(self):
        # return the center of stimulus
        # this should be at the center of the screen
        return self.exp_parameters.window_center
    
    def getProbeCoord(self):
        # return the center of probe
        cx, cy = self.exp_parameters.window_center
        _, window_height = self.exp_parameters.window_size
        return cx, cy - int(window_height * 0.133)
        
    def drawThickLine(self, x0, y0, x1, y1, thickness, color):
        x0, y0, x1, y1, thickness = int(x0), int(y0), int(x1), int(y1), int(thickness)
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x0, y0, x1, y1, thickness, color.r, color.g, color.b, color.a)
    
    def drawThickFrame(self, x0, y0, x1, y1, thickness, color = sdl2.ext.Color(0, 0, 0)):
        x0, y0, x1, y1, thickness, mergin = int(x0), int(y0), int(x1), int(y1), int(thickness), int(thickness/2)
        x0, y0, x1, y1 = x0-mergin, y0-mergin, x1+mergin, y1+mergin
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x0, y0, x1, y0, thickness, color.r, color.g, color.b, color.a)
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x0, y0, x0, y1, thickness, color.r, color.g, color.b, color.a)
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x1, y0, x1, y1, thickness, color.r, color.g, color.b, color.a)
        sdl2.sdlgfx.thickLineRGBA(self.renderer.renderer, x0, y1, x1, y1, thickness, color.r, color.g, color.b, color.a)
        
    def drawFilledRect(self, x0, y0, x1, y1, color):
#         w, h = numpy.abs(x1-x0), numpy.abs(y1-y0)
        x0, y0, x1, y1 = int(x0), int(y0), int(x1), int(y1)
        
        sdl2.sdlgfx.boxRGBA(self.renderer.renderer, x0, y0, x1, y1, color.r, color.g, color.b, color.a)

    def drawText(self, text, x = None, y = None, text_color = sdl2.SDL_Color(0, 0, 0), align = 'center-center'):
        if self.font is None:
            self.font = sdl2.sdlttf.TTF_OpenFont(self.RESOURCES.get_path('micross.ttf'), int(self.exp_parameters.font_size))
            
        if x is None:
            x = self.window_surface.w/2
        if y is None:
            y = self.window_surface.h/2
        msg = sdl2.sdlttf.TTF_RenderText_Solid(self.font, text, text_color)
        
        if align == 'center-center':
            msg_rect = sdl2.SDL_Rect(int(x-msg.contents.w/2), int(y-msg.contents.h/2), msg.contents.w, msg.contents.h)
        elif align == 'top-left':
            msg_rect = sdl2.SDL_Rect(x, y, msg.contents.w, msg.contents.h)
        elif align == 'top-right':
            msg_rect = sdl2.SDL_Rect(x-msg.contents.w, y, msg.contents.w, msg.contents.h)
        elif align == 'center-left':
            msg_rect = sdl2.SDL_Rect(x, int(y-msg.contents.h/2), msg.contents.w, msg.contents.h)
        elif align == 'center-right':
            msg_rect = sdl2.SDL_Rect(x-msg.contents.w, int(y-msg.contents.h/2), msg.contents.w, msg.contents.h)
            
        sdl2.surface.SDL_BlitSurface(msg.contents, None, self.window_surface, msg_rect)
        sdl2.SDL_FreeSurface(msg)
        
    def getString(self, recorder, display_text, x = None, y = None, text_color = sdl2.SDL_Color(0, 0, 0)):
        if self.font is None:
            self.font = sdl2.sdlttf.TTF_OpenFont(self.RESOURCES.get_path('micross.ttf'), int(self.exp_parameters.font_size))
            
        if x is None:
            x = self.window_surface.w/2
        if y is None:
            y = self.window_surface.h/2

        entered = False
        input_string = ''
        
        self.clear()
        self.drawText(display_text + input_string, x, y, align = 'top-left')
        self.refresh()
        
        while not entered:
            input_char, _ = recorder.recordKeyboard(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Return'])
            if input_char <= 9:
                input_string += str(input_char)
            elif input_char == 10:
                entered = True
            
            self.clear()
            self.drawText(display_text + input_string, x, y, align = 'top-left')
            self.refresh()
            
        return input_string
    
