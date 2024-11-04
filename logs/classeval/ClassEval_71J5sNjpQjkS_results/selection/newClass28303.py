import threading
import queue
from scipy.stats import ttest_ind

def Func_newFunc0_50_0(new_player_row, self):
    return new_player_row + (new_player_row - self.player_row)