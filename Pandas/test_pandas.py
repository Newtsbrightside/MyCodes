import pandas as pd
import torch
import numpy as np
import pytest
friends = ['Wipi','Azy','Acel','Ghazi','Xinxin']
ages = [20, 21, 19, 18, 22]
heights = [170, 180, 175, 160, 168]
weights = [70, 80, 75, 60, 68]
pd.Series(friends)
print(pd.Series(friends))
pd.DataFrame({'Name':friends,'Age':ages,'Height':heights,'Weight':weights})
print(pd.DataFrame({'Name':friends,'Age':ages,'Height':heights,'Weight':weights}))