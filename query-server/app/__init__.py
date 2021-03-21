# Load Excel File

import pandas as pd
df = pd.read_csv('data/data.csv')

import app.utils as utils
BANK_DATA_DIR , LEAD_COUNT = utils.main(df)