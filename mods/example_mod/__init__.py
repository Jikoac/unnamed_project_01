'''An example mod for testing and reference purposes'''
import sys
import os
sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.join(os.path.dirname(__file__),'data'))
import  data
sys.path.remove(os.path.dirname(__file__))
sys.path.remove(os.path.join(os.path.dirname(__file__),'data'))