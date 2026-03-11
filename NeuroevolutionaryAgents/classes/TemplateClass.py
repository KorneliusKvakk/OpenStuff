"""
Created on January 1 00:00 202x
@author: Name
This class defines the template class for all other classes
"""
from configTemplateProject import *

import Class as ParentClass

from library import Module

from utilities import *

class TemplateClass(ParentClass):
    def __init__(self,
        inputs=1,
        variables=2,
        outputs=3):

        self.input = inputs
        self.output = 0

        # define the class constants and variables
        self.constant = 0
        self.variable = 1

        # transform input
        self.new_input = self.input * variables

    # define class function
    def CalculateOutput(self, x):
        self.output = self.new_input * 2
        return self.output

    # define class setter
    def SetInput(self, input):
        self.input = input
        
    # define class getter
    def GetOutput(self):
        return self.output