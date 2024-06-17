<<<<<<< HEAD
class footie:
    
=======
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class footie:
    data = 0

    def __init__(self,file):
        df = pd.read_csv(file)
        self.data = df
        print(self.data)


f = footie('PL 23-24 Data.csv')
>>>>>>> 2f200fb (start outcome method)
