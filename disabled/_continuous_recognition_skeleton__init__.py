__author__ = 'parkerh'

# This __init__.py was meant to work with _continuous_recognition_skeleton.py, so that you could just drop a
# rule into the /ccr folder, and _continuous_recognition_skeleton would pick it up, without having to explicitly
# import it. Ended up seeming hacky and overkill.

# https://stackoverflow.com/questions/1057431/how-to-load-all-modules-in-a-folder
# Dynamically set '__all__' so that i can do 'from package import *' to load all modules in the package
from os.path import dirname, basename, isfile, join
import glob
modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [ basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]