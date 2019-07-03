import sys
import os


## Initial setup
try:
    import common
    import core
except:
    sys.path.append(os.path.abspath(join(os.getcwd(),'../..','common')))
    import common
    import core