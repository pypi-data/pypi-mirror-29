A productive Jupyter Notebook Utilties 
======================================

These are utilities that can be used with Jupyter notebook for increasing productivity(!!)

I only support Python 3.x - Do not use in 2.x versions. Please support Python 3.X versions to move forward

[ ] pip install Jupytils

( ) Use the following in your Notebook as first line

import sys
import importlib as imp
if ('Jupytils' in sys.modules):
    reloaded = imp.reload(Jupytils)
else:
    import Jupytils

