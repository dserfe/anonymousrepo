import threading
import queue
from scipy.stats import ttest_ind

def Func_newFunc0_14_0(s, newi_1, newcount_1, variable_8_14):
    return s.count(newi_1.lower()) + newcount_1.get(newi_1.lower(), variable_8_14)