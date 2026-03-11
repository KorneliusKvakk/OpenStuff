# %% get namo data
from config import *
from NaMo_Data_Getter import NaMo_Data_Getter

data = pd.read_excel('test_NaMo_input.xlsx')
NaMo_Data_Getter = NaMo_Data_Getter(data)
NaMo_Data_Getter.Run()

# %% neuroevolution test
from NEvo_Trainer import NEvo_Trainer

training_data = pd.read_excel('test_NEvo_training_data.xlsx')
normalized_training_data = 