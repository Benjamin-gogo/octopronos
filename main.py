import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as pl
import pickle
from scipy.stats import poisson
import json

import matplotlib.pyplot as plt
import numpy as np
import pickle
import os
from math import *




if __name__ == "__main__":
    matches_from_1930 = pd.read_csv('csv/filtered_international_matches.csv', delimiter=',')

