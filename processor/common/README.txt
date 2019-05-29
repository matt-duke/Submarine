Common location for shared Python modules

Be sure to include __init__.py in modules

In the python start sequence:
    import sys
    import os
    from os import path
    sys.path.append(path.abspath(path.join(os.getcwd(),'../..','common')))