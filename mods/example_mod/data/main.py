import sys
import os

project_code_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'code'))
sys.path.append(project_code_path)

from base import *