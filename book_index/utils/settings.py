import os

# -----------------------------
# file path
def get_working_dr():
    return os.getcwd()

BOOK_LEVEL_MODEL_PATH = '../../model/lgb_regressor.pkl'
SCLAER_PATH = '../../model/standard_scaler.pkl'
TOP_WORD_PATH = '../../data/output2/top_word.json'

SIF_W2V_MODEL_PATH = '../../data/output2/sif_w2v.model'
SIF_WORD_FREQ_DICT = '../../data/output2/sif_dict.json'