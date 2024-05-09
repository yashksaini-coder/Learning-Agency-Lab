# Importing the basic libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


from src.load import load_train, load_test, load_submission

train = load_train()
test = load_test()

